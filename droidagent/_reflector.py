import os
import logging

from .config import agent_config
from .model import APIUsageManager
from .action import *
from .prompts.reflect_task import reflect_task


class Reflector:
    def __init__(self, memory, prompt_recorder=None):
        self.memory = memory
        self.logger = logging.getLogger('agent')
        self.prompt_recorder = prompt_recorder

    def reflect(self):
        task_result_summary, task_result, reflections = reflect_task(self.memory, self.prompt_recorder)
        self.memory.add_task_result(task_result, task_result_summary)

        working_memory_record = []
        # FIXME: need to clean up
        for desc, record_type, timestamp, page in self.memory.working_memory:
            action_data = None
            events = []
            if isinstance(desc, Action):
                action_data = desc.get_reproducible_record()
            if record_type == 'ACTION':
                events = desc.events
            working_memory_record.append({
                'description': str(desc),
                'type': record_type,
                'timestamp': timestamp,
                'page': page,
                'action_data': action_data,
                'events': events
            })
        self.memory.exp_data['task_results'][self.memory.task] = {
            'result': task_result,
            'summary': task_result_summary,
            'reflections': reflections,
            'num_actions': len([record for record in working_memory_record if record['type'] == 'ACTION']),
            'num_critiques': len([record for record in working_memory_record if record['type'] == 'CRITIQUE']),
            'visited_pages_during_task': self.memory.visited_pages_for_task,
            'task_execution_history': working_memory_record
        }
        self.memory.exp_data['API_usage'] = APIUsageManager.usage
        self.memory.exp_data['API_response_time'] = APIUsageManager.response_time

        for reflection in reflections: # TODO: map information with a specific widget/activity
            # reflections: useful takeaways from the task execution history
            self.memory.update_task_knowledge(self.memory.task_start_state.signature, self.memory.task, reflection)

        return task_result_summary
