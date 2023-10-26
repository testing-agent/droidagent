import os
import logging
import time

from .config import agent_config
from .action import *
from .prompts.plan_v3 import *

from collections import defaultdict

RETRY_COUNT = 3


class Planner:
    def __init__(self, memory, prompt_recorder=None):
        self.memory = memory
        self.logger = logging.getLogger('agent')
        self.prompt_recorder = prompt_recorder

    """
    Task-based planning (independence between planner and actor)
    """
    def plan_task(self):
        task, task_end_condition, plan, first_action = prompt_new_task(self.memory, self.prompt_recorder)

        if task is None or first_action is None:
            return None

        self.memory.task = task
        self.memory.task_end_condition = task_end_condition
        self.memory.initial_task_plan = plan
        self.memory.task_start_state = self.memory.current_gui_state
        self.memory.previous_action = first_action
        self.memory.working_memory = []
        self.memory.visited_pages_for_task = defaultdict(lambda: 0)
        self.memory.visited_pages_for_task[self.memory.current_activity] += 1
        self.memory.performed_action_types_for_task = defaultdict(dict)

        self.memory.task_memory_entry_id = self.memory.add_task(f'{agent_config.persona_name} planned a new task: {self.memory.task}')
        
        self.memory.append_to_working_memory(first_action, 'ACTION')
        
        return first_action
