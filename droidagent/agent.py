import os
import json
import time
import random
import requests

import logging
import friendlywords as fw

from datetime import datetime
from pathlib import Path

from .gui_state import GUIState
from .memory import Memory
from .model import stringify_prompt, zip_messages
from ._observer import Observer
from ._planner import Planner
from ._actor import Actor
from ._reflector import Reflector
from .config import agent_config

from ._actor_gptdroid import GPTDroidActor
from ._actor_nocritique_noknowledge import NoCritiqueActor
from ._actor_noknowledge import NoKnowledgeActor
from ._planner_noknowledge import NoKnowledgePlanner


os.environ['TOKENIZERS_PARALLELISM'] = 'false'

MODE_PLAN = 'plan'
MODE_ACT = 'act'
MODE_REFLECT = 'reflect'
MODE_OBSERVE = 'observe'

MAX_ACTIONS = 13


class PromptRecorder:
    def __init__(self, exp_id):
        self.state_tag = 'initial'
        self.exp_id = exp_id

    def set_state_tag(self, state_tag):
        self.state_tag = state_tag
    
    def record(self, prompt, mode):
        prompt_str = stringify_prompt(prompt)
        with open(os.path.join(agent_config.agent_output_dir, 'prompts', f'prompt_{self.state_tag}_{datetime.now().strftime("%H%M%S")}_{mode}.txt'), 'w') as f:
            f.write(prompt_str)

    
class Agent:
    def __init__(self, output_dir, app=None):
        if app is None:
            raise NotImplementedError # TODO: load agent snapshot from output_dir
        
        else:
            agent_config.set_app(app)
            agent_config.set_output_dir(output_dir)
            agent_config.save()

            exp_id = fw.generate('po', separator='-')

            self.exp_id = exp_id
            self.prompt_recorder = PromptRecorder(exp_id)
            self.memory = Memory(name=self.exp_id)

        self.logger = logging.getLogger('agent')
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(os.path.join(agent_config.agent_output_dir, f'agent_{exp_id}.log'), mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s - %(asctime)s: %(message)s'))
        self.logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s - %(message)s'))
        self.logger.addHandler(stream_handler)
        self.logger.info(f'Agent ID: {exp_id}')

    def save_memory_snapshot(self):
        memory_snapshot_dir = os.path.join(agent_config.agent_output_dir, 'memory_snapshots', f'step_{self.step_count}')
        os.makedirs(memory_snapshot_dir, exist_ok=True)
        self.memory.save_snapshot(memory_snapshot_dir)

    def step(self, droidbot_state=None):
        raise NotImplementedError
    
    @property
    def current_gui_state(self):
        return self.memory.current_gui_state

    def set_current_gui_state(self, droidbot_state):
        self.memory.set_current_gui_state(GUIState().from_droidbot_state(droidbot_state))
        app_activity_depth = self.memory.current_gui_state.get_app_activity_depth()
        if app_activity_depth != 0:
            self.logger.warning(f'App is not in the foreground. Current activity stack: {self.memory.current_gui_state.activity_stack}')

        self.memory.add_visited_activity(self.memory.current_gui_state.activity)
        self.prompt_recorder.set_state_tag(self.memory.current_gui_state.tag)
        
        # Check immediately captured temp messages are still visible
        for widget in self.memory.temp_messages:
            w = self.memory.current_gui_state.get_widget_by_signature(widget.signature)
            if w is None:
                self.current_gui_state.lost_messages.add(widget.text)

        for message in self.memory.toasts:
            self.current_gui_state.lost_messages.add(message)
        
        self.memory.temp_messages = []
        self.memory.toasts = []

    def capture_temporary_message(self, droidbot_state):
        gui_state = GUIState().from_droidbot_state(droidbot_state)

        _, appeared_widgets, _ = self.current_gui_state.diff_widgets(gui_state)

        temp_message_count = 0
        for widget in appeared_widgets:
            if widget.text is not None and len(widget.text) > 0:
                self.memory.temp_messages.append(widget)
                temp_message_count += 1

                # we don't want to capture too many messages
                if temp_message_count > 3:
                    break

        return gui_state

    def clear_temporary_message(self):
        self.memory.temp_messages = []

    def capture_toast_message(self, captured_toast_messages):
        self.memory.toasts = captured_toast_messages

    @staticmethod
    def is_loading_state(droidbot_state):
        gui_state = GUIState().from_droidbot_state(droidbot_state)
        if len(gui_state.interactable_widget_ids) == 0:
            return True

        return False

    def inject_memory(self, description, entry_type):
        self.memory.add_entry(description, entry_type)


class TaskBasedAgent(Agent):
    """
    Task-based Agent
    """
    def __init__(self, output_dir, app=None, persona=None, debug_mode=False):
        super().__init__(output_dir, app=app)

        if app is None:
            raise NotImplementedError # TODO: load agent snapshot from output_dir
        else:
            self.initialize(app, persona, debug_mode=debug_mode)

        self.logger.info(f'Target App: {agent_config.app_name} ({agent_config.package_name})')
        self.logger.info(f'Ultimate Goal: {agent_config.ultimate_goal}')

    def initialize(self, app, persona, debug_mode=False):
        for initial_knowledge in persona['initial_knowledge']:
            self.inject_memory(initial_knowledge, 'INITIAL_KNOWLEDGE')
            # FIXME: add to knowledge memory?
        
        if debug_mode:
            agent_config.set_debug_mode()
            
        agent_config.set_persona(persona)
        agent_config.save()

        self.observer = Observer(self.memory, self.prompt_recorder)
        self.planner = Planner(self.memory, self.prompt_recorder)
        self.actor = Actor(self.memory, self.prompt_recorder)
        self.reflector = Reflector(self.memory, self.prompt_recorder)
        self.mode = MODE_PLAN
        self.step_count = 0

    @property
    def task(self):
        return self.memory.task

    @property
    def persona_name(self):
        return agent_config.persona_name

    def record_test_script(self, task, task_result, interaction_log):
        # TODO
        with open(os.path.join(agent_config.agent_output_dir, 'recorded_scripts', f'script_{self.exp_id}.py'), 'a') as f:
            f.write(f'# {task}\n')
            f.write(f'# LLM-determined task result: {task_result}\n')
            for interaction, mode in interaction_log:
                if mode == 'ACTION':
                    f.write(f'{interaction}\n')
                elif mode == 'OBSERVATION':
                    f.write(f'# {interaction}\n\n')
            f.write('\n')

    def step(self, droidbot_state=None):
        self.step_count += 1
        self.logger.info(f'Step {self.step_count}, Mode: {self.mode}')
        self.logger.info(f'Current Activity Coverage: {len(self.memory.visited_activities)} / {len(agent_config.app_activities)}')

        if droidbot_state is not None:
            self.set_current_gui_state(droidbot_state)

        with open(os.path.join(agent_config.agent_output_dir, 'exp_data.json'), 'w') as f:
            json.dump(self.memory.exp_data, f, indent=2)

        if self.mode == MODE_PLAN:
            """
            * Plan
            """
            self.actor.reset()
            first_action = self.planner.plan_task()

            if first_action is not None:
                self.mode = MODE_OBSERVE
                self.actor.action_count += 1
                self.actor.critique_countdown -= 1
                self.logger.info(f'* New task: {self.task}')
                self.logger.info(f'* First action: {first_action}')

                return first_action

            return None
        
        elif self.mode == MODE_REFLECT:
            """
            * Reflect
            """
            task_result = self.reflector.reflect()

            self.logger.info(f'* Task Reflection: {task_result}')

            self.mode = MODE_PLAN

            return None

        elif self.mode == MODE_ACT:
            """
            * Action
            """
            self.logger.info(f'[Current Task] {self.task}')

            if self.actor.action_count >= MAX_ACTIONS:
                # If task does not end after MAX_ACTIONS actions, reflect
                self.mode = MODE_REFLECT
                self.memory.append_to_working_memory('The task gets too long, so I am going to put off the task and start a new task that could be easily achievable instead.', 'TASK_ABORTED')
                self.logger.info(f'Task not completed with max actions, aborting...')
                return None

            next_action = self.actor.act()

            if next_action is None:
                self.mode = MODE_REFLECT
                return None
            else:
                self.logger.info(f'* Next action: {next_action}')
                self.mode = MODE_OBSERVE
                return next_action

        elif self.mode == MODE_OBSERVE:
            """
            * Observe
            """
            action_result = self.observer.observe_action_result()
            if action_result is not None:
                self.logger.info(f'* Observation: """\n{action_result}\n"""')
            else:
                self.logger.info(f'* Observation: No detectable change.')

            self.mode = MODE_ACT
            return None

# Ablation 1: Actor-only, GPTDroid replication
class ActorOnlyAgent(Agent):
    def __init__(self, output_dir, app=None):
        super().__init__(output_dir, app=app)

        self.actor = GPTDroidActor(self.memory)
        self.step_count = 0

        assert app is not None

    @property
    def persona_name(self):
        return agent_config.persona_name

    def step(self, droidbot_state=None):
        self.step_count += 1
        self.logger.info(f'Step {self.step_count}')
        self.logger.info(f'Current Activity Coverage: {len(self.memory.visited_activities)} / {len(agent_config.app_activities)}')

        if droidbot_state is not None:
            self.set_current_gui_state(droidbot_state)

        action = None
        if self.step_count == 1:
            action = self.actor.decide_first_action()
        else:
            action = self.actor.decide_next_action()

        self.logger.info(f'* Next action: {action}')

        full_prompt = {
            'system_message': self.actor.current_prompt['system_message'],
            'user_messages': self.actor.full_prompt['user_messages'] + self.actor.current_prompt['user_messages'],
            'assistant_messages': self.actor.full_prompt['assistant_messages'] + self.actor.current_prompt['assistant_messages'],
        }
        with open(os.path.join(agent_config.agent_output_dir, 'conversation.json'), 'w') as f:
            json.dump(full_prompt, f, indent=2)

        with open(os.path.join(agent_config.agent_output_dir, 'conversation.txt'), 'w') as f:
            f.write(stringify_prompt(zip_messages(full_prompt['system_message'], full_prompt['user_messages'], full_prompt['assistant_messages'])))
    
        return action

# Ablation 2: Task-based, w/o critique, w/o knowledge
class TaskBasedAgentNoCritiqueNoKnowledge(Agent):
    """
    Task-based Agent
    """
    def __init__(self, output_dir, app=None, persona=None, debug_mode=False):
        super().__init__(output_dir, app=app)

        if app is None:
            raise NotImplementedError # TODO: load agent snapshot from output_dir
        else:
            self.initialize(app, persona, debug_mode=debug_mode)

        self.logger.info(f'Target App: {agent_config.app_name} ({agent_config.package_name})')
        self.logger.info(f'Ultimate Goal: {agent_config.ultimate_goal}')

    def initialize(self, app, persona, debug_mode=False):
        for initial_knowledge in persona['initial_knowledge']:
            self.inject_memory(initial_knowledge, 'INITIAL_KNOWLEDGE')
            # FIXME: add to knowledge memory?
        
        if debug_mode:
            agent_config.set_debug_mode()
            
        agent_config.set_persona(persona)
        agent_config.save()

        self.observer = Observer(self.memory, self.prompt_recorder)
        self.planner = NoKnowledgePlanner(self.memory, self.prompt_recorder)
        self.actor = NoCritiqueActor(self.memory, self.prompt_recorder)
        self.reflector = Reflector(self.memory, self.prompt_recorder)
        self.mode = MODE_PLAN
        self.step_count = 0

    @property
    def task(self):
        return self.memory.task

    @property
    def persona_name(self):
        return agent_config.persona_name

    def record_test_script(self, task, task_result, interaction_log):
        # TODO
        with open(os.path.join(agent_config.agent_output_dir, 'recorded_scripts', f'script_{self.exp_id}.py'), 'a') as f:
            f.write(f'# {task}\n')
            f.write(f'# LLM-determined task result: {task_result}\n')
            for interaction, mode in interaction_log:
                if mode == 'ACTION':
                    f.write(f'{interaction}\n')
                elif mode == 'OBSERVATION':
                    f.write(f'# {interaction}\n\n')
            f.write('\n')

    def step(self, droidbot_state=None):
        self.step_count += 1
        self.logger.info(f'Step {self.step_count}, Mode: {self.mode}')
        self.logger.info(f'Current Activity Coverage: {len(self.memory.visited_activities)} / {len(agent_config.app_activities)}')

        if droidbot_state is not None:
            self.set_current_gui_state(droidbot_state)

        with open(os.path.join(agent_config.agent_output_dir, 'exp_data.json'), 'w') as f:
            json.dump(self.memory.exp_data, f, indent=2)

        if self.mode == MODE_PLAN:
            """
            * Plan
            """
            self.actor.reset()
            first_action = self.planner.plan_task()

            if first_action is not None:
                self.mode = MODE_OBSERVE
                self.actor.action_count += 1
                self.logger.info(f'* New task: {self.task}')
                self.logger.info(f'* First action: {first_action}')

                return first_action

            return None
        
        elif self.mode == MODE_REFLECT:
            """
            * Reflect
            """
            task_result = self.reflector.reflect()

            self.logger.info(f'* Task Reflection: {task_result}')

            self.mode = MODE_PLAN

            return None

        elif self.mode == MODE_ACT:
            """
            * Action
            """
            self.logger.info(f'[Current Task] {self.task}')

            if self.actor.action_count >= MAX_ACTIONS:
                # If task does not end after MAX_ACTIONS actions, reflect
                self.mode = MODE_REFLECT
                self.memory.append_to_working_memory('The task gets too long, so I am going to put off the task and start a new task that could be easily achievable instead.', 'TASK_ABORTED')
                self.logger.info(f'Task not completed with max actions, aborting...')
                return None

            next_action = self.actor.act()

            if next_action is None:
                self.mode = MODE_REFLECT
                return None
            else:
                self.logger.info(f'* Next action: {next_action}')
                self.mode = MODE_OBSERVE
                return next_action

        elif self.mode == MODE_OBSERVE:
            """
            * Observe
            """
            action_result = self.observer.observe_action_result()
            if action_result is not None:
                self.logger.info(f'* Observation: """\n{action_result}\n"""')
            else:
                self.logger.info(f'* Observation: No detectable change.')

            self.mode = MODE_ACT
            return None


# Ablation 3: Task-based, w/o knowledge
class TaskBasedAgentNoKnowledge(Agent):
    """
    Task-based Agent
    """
    def __init__(self, output_dir, app=None, persona=None, debug_mode=False):
        super().__init__(output_dir, app=app)

        if app is None:
            raise NotImplementedError # TODO: load agent snapshot from output_dir
        else:
            self.initialize(app, persona, debug_mode=debug_mode)

        self.logger.info(f'Target App: {agent_config.app_name} ({agent_config.package_name})')
        self.logger.info(f'Ultimate Goal: {agent_config.ultimate_goal}')

    def initialize(self, app, persona, debug_mode=False):
        for initial_knowledge in persona['initial_knowledge']:
            self.inject_memory(initial_knowledge, 'INITIAL_KNOWLEDGE')
            # FIXME: add to knowledge memory?
        
        if debug_mode:
            agent_config.set_debug_mode()
            
        agent_config.set_persona(persona)
        agent_config.save()

        self.observer = Observer(self.memory, self.prompt_recorder)
        self.planner = NoKnowledgePlanner(self.memory, self.prompt_recorder)
        self.actor = NoKnowledgeActor(self.memory, self.prompt_recorder)
        self.reflector = Reflector(self.memory, self.prompt_recorder)
        self.mode = MODE_PLAN
        self.step_count = 0

    @property
    def task(self):
        return self.memory.task

    @property
    def persona_name(self):
        return agent_config.persona_name

    def record_test_script(self, task, task_result, interaction_log):
        # TODO
        with open(os.path.join(agent_config.agent_output_dir, 'recorded_scripts', f'script_{self.exp_id}.py'), 'a') as f:
            f.write(f'# {task}\n')
            f.write(f'# LLM-determined task result: {task_result}\n')
            for interaction, mode in interaction_log:
                if mode == 'ACTION':
                    f.write(f'{interaction}\n')
                elif mode == 'OBSERVATION':
                    f.write(f'# {interaction}\n\n')
            f.write('\n')

    def step(self, droidbot_state=None):
        self.step_count += 1
        self.logger.info(f'Step {self.step_count}, Mode: {self.mode}')
        self.logger.info(f'Current Activity Coverage: {len(self.memory.visited_activities)} / {len(agent_config.app_activities)}')

        if droidbot_state is not None:
            self.set_current_gui_state(droidbot_state)

        with open(os.path.join(agent_config.agent_output_dir, 'exp_data.json'), 'w') as f:
            json.dump(self.memory.exp_data, f, indent=2)

        if self.mode == MODE_PLAN:
            """
            * Plan
            """
            self.actor.reset()
            first_action = self.planner.plan_task()

            if first_action is not None:
                self.mode = MODE_OBSERVE
                self.actor.action_count += 1
                self.actor.critique_countdown -= 1
                self.logger.info(f'* New task: {self.task}')
                self.logger.info(f'* First action: {first_action}')

                return first_action

            return None
        
        elif self.mode == MODE_REFLECT:
            """
            * Reflect
            """
            task_result = self.reflector.reflect()

            self.logger.info(f'* Task Reflection: {task_result}')

            self.mode = MODE_PLAN

            return None

        elif self.mode == MODE_ACT:
            """
            * Action
            """
            self.logger.info(f'[Current Task] {self.task}')

            if self.actor.action_count >= MAX_ACTIONS:
                # If task does not end after MAX_ACTIONS actions, reflect
                self.mode = MODE_REFLECT
                self.memory.append_to_working_memory('The task gets too long, so I am going to put off the task and start a new task that could be easily achievable instead.', 'TASK_ABORTED')
                self.logger.info(f'Task not completed with max actions, aborting...')
                return None

            next_action = self.actor.act()

            if next_action is None:
                self.mode = MODE_REFLECT
                return None
            else:
                self.logger.info(f'* Next action: {next_action}')
                self.mode = MODE_OBSERVE
                return next_action

        elif self.mode == MODE_OBSERVE:
            """
            * Observe
            """
            action_result = self.observer.observe_action_result()
            if action_result is not None:
                self.logger.info(f'* Observation: """\n{action_result}\n"""')
            else:
                self.logger.info(f'* Observation: No detectable change.')

            self.mode = MODE_ACT
            return None