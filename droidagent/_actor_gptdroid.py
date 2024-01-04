import os
import random
import logging
import time
import copy

import openai

from .config import agent_config
from .action import *
from .utils import *
from .prompts.act_gptdroid_style import prompt_first_action, prompt_next_action

MODEL = agent_config.actor_model


class GPTDroidActor():
    def __init__(self, memory):
        self.memory = memory
        self.full_prompt = {
            'system_message': None,
            'user_messages': [],
            'assistant_messages': [],
        }
        self.current_prompt = {
            'system_message': None,
            'user_messages': [],
            'assistant_messages': [],
        }
        self.performed_actions = []
        self.logger = logging.getLogger('agent')

    def decide_first_action(self):
        action = prompt_first_action(self.memory, self.current_prompt)
        self.performed_actions.append(action)
        self.memory.update_widget_knowledge(self.memory.current_gui_state.signature, self.memory.current_activity, action.target_widget, action, '', '')

        self.full_prompt['system_message'] = self.current_prompt['system_message']

        return action

    def decide_next_action(self):
        action = None
        original_prompt = None
        contain_feedback = True
        while action is None:
            try:
                original_prompt = copy.deepcopy(self.current_prompt)
                action = prompt_next_action(self.memory, error_message=None, full_prompt=self.current_prompt, contain_feedback=contain_feedback)
            except (openai.BadRequestError) as e:
                # exceed max token limit: initialize prompt
                self.logger.info(f'Exceeded max token limit. Initialize prompt.')

                self.full_prompt['user_messages'].extend(self.current_prompt['user_messages'][:-1])
                self.full_prompt['assistant_messages'].extend(self.current_prompt['assistant_messages'])
                self.current_prompt['user_messages'] = []
                self.current_prompt['assistant_messages'] = []

                contain_feedback = False

 
        assert action is not None
        
        self.performed_actions.append(action)
        if action.target_widget is not None:
            self.memory.update_widget_knowledge(self.memory.current_gui_state.signature, self.memory.current_activity, action.target_widget, action, '', '')



        return action

