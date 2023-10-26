import os
import random
import logging
import time

from .config import agent_config
from .action import *
from .utils import *
from .prompts.act_noknowledge import prompt_action


MAX_RETRY = 5
CRITIQUE_COUNTDOWN = 4


class NoCritiqueActor:
    def __init__(self, memory, prompt_recorder=None):
        self.memory = memory
        self.logger = logging.getLogger('agent')
        self.prompt_recorder = prompt_recorder
        self.action_count = 0

    def reset(self):
        self.action_count = 0
    
    def act(self): # use function call for selecting the action
        assert self.memory.task is not None, 'No task is registered'

        action = prompt_action(self.memory, self.prompt_recorder)

        if action is not None:
            self.action_count += 1
            self.memory.append_to_working_memory(action, 'ACTION')
            self.memory.previous_action = action

        return action
