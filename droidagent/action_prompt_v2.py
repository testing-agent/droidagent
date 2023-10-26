from .model import get_next_assistant_message, zip_messages
from .config import agent_config

ACTOR_MODEL = agent_config.actor_model
MAX_RETRY = 5

def prompt_action_v2(task_memory, screen_description, task, task_end_condition, previous_conversation=None):
    system_message = None
    user_messages = []
    assistant_messages = []

    if previous_conversation is None:
        system_message = f'''
Act as a person using an android mobile application named {agent_config.app_name} with the given profile:
{agent_config.persona_profile}

You are going to choose the next GUI action to accomplish the task. You can end the task if it is completed or no longer feasible to accomplish.
'''.strip()

        user_messages.append(f'''
Your current task is "{task}". {task_end_condition if task_end_condition.endswith(".") else task_end_condition + "."}
Decide a next GUI action to accomplish the task. To end the task, say "none".

Your memory about the task (listed in chronological order):
{task_memory}

Current screen description:
{screen_description}

I am going to provide a template for your output to reason about your choice step by step. Fill out the <...> parts in the template with your own words. Do not include anything else in your answer except the text to fill out the template. Preserve the formatting and overall template.

=== Below is the template for your answer ===
Current progress for the task: <1~2 sentences according to your memory and the current screen description>
Remaining actions to finish the task: <1~2 sentences according to your memory, current screen description, and the task end condition>
End the task?: <yes/no, do not include anything else in your answer>
Next action: <1 sentence, start with "I will", or just say "none" to end the task>
Reasoning for the next action choice: <1 short sentence, start with "Because I need to", not required if next action is none>
        '''.strip())

    else:
        system_message = previous_conversation['system_message']
        user_messages = [q for q, a in previous_conversation['conversation']]
        assistant_messages = [a for q, a in previous_conversation['conversation']]
        user_messages.append(f'''
Your provided action is not possible on the current screen. Generate the valid action again following the provided template.
        '''.strip())

    assistant_messages.append(get_next_assistant_message(system_message, user_messages, assistant_messages, model=ACTOR_MODEL))

    answer = assistant_messages[-1].strip()
    
    end_task = False
    next_action = None
    reasoning = None

    for l in answer.split('\n'):
        l = l.strip()
        if l.startswith('End the task?:'):
            if 'yes' in l.split(':')[1].strip().lower():
                end_task = True
                break
        if l.startswith('Reasoning for the next action choice:'):
            reasoning = l.split('Reasoning for the next action choice:')[1].strip()

        if l.startswith('Next action:'):
            next_action = l.split('Next action:')[1].strip()

    if end_task or next_action == 'none':
        next_action = None

    if next_action is not None and reasoning is not None:
        next_action = next_action + f' ({reasoning})'

    return next_action, zip_messages(system_message, user_messages, assistant_messages)


def match_action_id(gui_state, action_desc):
    """
    Action description from user => match with the actual possible action ID
    """
    system_message = f'''
You are a helpful assistant who can select the concrete GUI action ID from the given action description.
    '''.strip()

    assistant_messages = []
    user_messages = []
    user_messages.append(f'''
Select the action ID that best matches the given action description.
{action_desc}

Choose one of the following action IDs:
{gui_state.describe_possible_actions()}

I am going to provide a template for your output to reason about your choice step by step. Fill out the <...> parts in the template with your own words. Do not include anything else in your answer except the text to fill out the template. Preserve the formatting and overall template.

=== Below is the template for your answer ===
Action type: <event type (string), e.g., "click", "scroll", "set_text", "key_event">
Target widget <properties of the target widget (string), e.g., "the button with the text "OK", "the text field with the resource_id "username_field">
Action ID: <action_id (integer), -1 if no match>
    '''.strip())

    assistant_messages.append(get_next_assistant_message(system_message, user_messages, assistant_messages, model=ACTOR_MODEL))

    next_action_id = parse_action_id(assistant_messages[-1])
    valid_action_id = False
    num_possible_actions = len(gui_state.possible_actions)

    for i in range(MAX_RETRY):
        try:
            next_action_id = int(next_action_id)
        except ValueError:
            next_action_id = None
        except TypeError:
            next_action_id = None
        
        if next_action_id == -1 or next_action_id in range(num_possible_actions):
            valid_action_id = True
            break
        else:
            retry_question = f'You did not provide a valid ID. Please provide a valid integer ID (0~{num_possible_actions-1}) or -1 (if none of the action IDs are matched with the given description). Generate the answer again following the provided template.'
            user_messages.append(retry_question)

            assistant_messages.append(get_next_assistant_message(system_message, user_messages, assistant_messages, model=ACTOR_MODEL))
            next_action_id = parse_action_id(assistant_messages[-1])
            
    if not valid_action_id:
        return None, zip_messages(system_message, user_messages, assistant_messages)

    return next_action_id, zip_messages(system_message, user_messages, assistant_messages)


def parse_action_id(result):
    if result.strip().isdigit() or result.strip() == '-1':
        return result.strip()
    
    next_action_id = None

    for l in result.split('\n'):
        l = l.strip()
        if l.startswith('End the task?:'):
            end_task = l.split(':')[1].strip().lower()
            if end_task == 'yes':
                next_action_id = '-1'
                break
        if l.startswith('Action ID:') or l.startswith('action ID:') or l.startswith('action id:'):
            next_action_id = l.split(':')[1].strip()

    return next_action_id


"""
(As an experimental way)

    def decide_action_v2(self, gui_state):
        assert self.task is not None, 'No task is registered'
        self.logger.debug(f'Current task: {self.task}')
        self.logger.debug(f'Current task end condition: {self.task_end_condition}')
        self.logger.debug(f'Current working memory: {self.stringify_working_memory()}')

        if self.previous_gui_state is None:
            state_summary = self.observer.summarize_state(gui_state)
            self.memory.working_memory.append((state_summary, 'OBSERVATION'))
        else:
            state_change = self.observer.summarize_state_change(self.previous_gui_state, gui_state)
            self.memory.working_memory.append((state_change, 'OBSERVATION'))

        self.previous_gui_state = gui_state

        if self.critique_countdown == 0:
            self.critique_countdown = CRITIQUE_COUNTDOWN
            critique, suggestion = self.critique(gui_state)
            if critique is not None:
                self.memory.working_memory.append((critique, 'CRITIQUE'))
            if suggestion is not None:
                self.memory.working_memory.append((suggestion, 'SUGGESTION'))
        else:
            self.critique_countdown -= 1

        screen_description = gui_state.describe_screen(list_possible_actions=False, observer=self.observer)
        action_desc, action_desc_prompt = prompt_action_v2(self.stringify_working_memory(), screen_description, self.task, self.task_end_condition)
        if action_desc == None:
            self.prompt_recorder.record(action_desc_prompt, 'action_NL')
            return None

        action_id, action_id_prompt = match_action_id(gui_state, action_desc)
        
        for _ in range(MAX_RETRY):
            if action_id is not None and action_id != -1:
                break

            # matched action ID is not found, retry with feedback 
            action_desc, action_desc_prompt = prompt_action_v2(self.stringify_working_memory(), screen_description, self.task, self.task_end_condition, previous_conversation=action_desc_prompt)
            if action_desc == None:
                self.prompt_recorder.record(action_desc_prompt, 'action_NL')
                return None
            
            action_id, action_id_prompt = match_action_id(gui_state, action_desc)

        if action_id is None or action_id == -1: 
            self.logger.error(f'Failed to match the action ID for the given action description: {action_desc} - aborting the task...')
            self.prompt_recorder.record(action_desc_prompt, 'action_NL')
            self.prompt_recorder.record(action_id_prompt, 'action_id')
            return None

        self.prompt_recorder.record(action_desc_prompt, 'action_NL')
        self.prompt_recorder.record(action_id_prompt, 'action_id')

        next_action = gui_state.possible_actions[action_id]

        if next_action.event_type in ['scroll', 'set_text']:
            next_action_data = self.prompt_action_data(next_action_type=next_action.event_type, 
            target_widget=next_action.target_widget, previous_prompt=action_desc_prompt)
            if next_action_data is None:
                next_action_data = 'DOWN'

            if next_action.event_type == 'scroll':
                next_action.update_direction(next_action_data)
            elif next_action.event_type == 'set_text':
                next_action.update_input_text(next_action_data)
        
        return next_action
            
# 5. Refer to the following guidelines to avoid common mistakes:
#   * Do not repeat the same action that you have already done.
#   * Do not perform unnecessary actions that do not make any changes to the app state.
#   * Make sure that you filled out all the required field. (Take a look at your previous actions and observations to see if you missed anything)
#   * Make sure that you submitted the form at the end of the task, if there is any button to submit the form.
#   * You can make a mistake like missing some steps, but you should try to correct it by going back and performing the necessary actions again.
"""