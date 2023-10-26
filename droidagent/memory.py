from .config import agent_config
from .utils import add_period, remove_period
from .action import *
from .prompts.summarize_widget_knowledge import prompt_summarized_widget_knowledge
from collections import defaultdict
import chromadb
import time
import os
import re
import json


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# chroma_client = chromadb.PersistentClient(path=os.path.join(PROJECT_PATH, 'chroma_db'))
chroma_client = chromadb.Client()
# TODO: split into different memory classes

class Memory:
    def __init__(self, name):
        try:
            chroma_client.delete_collection(name=name)
        except ValueError:
            pass

        try:
            chroma_client.delete_collection(name=f'{name}_knowledge')
        except ValueError:
            pass

        # permanent memory
        self.memory = chroma_client.create_collection(name=name)
        self.memory_entry_id = 0
        self.visited_activities = defaultdict(lambda: 0)
        self.exp_data = {
            'app_activities': agent_config.app_activities,
            'visited_activities': self.visited_activities,
            'task_results': {},
        }
        
        # working memory (volatile)
        self.task = None
        self.initial_task_plan = None
        self.task_memory_entry_id = None
        self.task_end_condition = None
        self.task_start_state = None
        self.working_memory = []
        self.visited_pages_for_task = defaultdict(lambda: 0)
        self.performed_action_types_for_task = defaultdict(dict)
        self.previous_gui_state = None
        self.current_gui_state = None
        self.previous_activity = None
        self.current_activity = None
        self.temp_messages = []
        self.toasts = []

        # spatial memory
        self.knowledge_map = {} # page name -> knowledge of all widget in that page
        self.knowledge = chroma_client.create_collection(name=f'{name}_knowledge')
        self.knowledge_entry_id = 0

    def add_knowledge(self, state, type, page='', widget='', action='', task='', observation='', reflection=''):
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.knowledge_entry_id += 1
        
        self.knowledge.add(
            documents=[state.strip()],
            metadatas=[{"type": type, "timestamp": timestamp, "page": page, "widget": widget, "action": action, "task": task, "observation": observation, "reflection": reflection}],
            ids=[str(self.knowledge_entry_id)]
        )
        return str(self.knowledge_entry_id)

    def get_widget_knowledge(self, page_name, widget_signature):
        if page_name not in self.knowledge_map:
            return None
        if widget_signature not in self.knowledge_map[page_name]:
            return None

        return self.knowledge_map[page_name][widget_signature]

    def get_performed_action_types_on_widget(self, page_name, widget_signature):
        widget_knowledge = self.get_widget_knowledge(page_name, widget_signature)
        if widget_knowledge is None:
            return {}
        return widget_knowledge['action_count']

    def get_performed_action_types_on_widget_during_task(self, page_name, widget_signature):
        return self.performed_action_types_for_task[(page_name, widget_signature)]

    def update_task_knowledge(self, task_start_state, task, reflection):
        self.add_knowledge(task_start_state, 'TASK', task=task, reflection=reflection)

    def update_widget_knowledge(self, state, page_name, widget, performed_action, observation, task):
        widget_signature = widget.signature
        assert widget_signature is not None, f'widget signature is None: {widget}'
        assert page_name is not None, f'page name is None'
        if page_name not in self.knowledge_map:
            self.knowledge_map[page_name] = {}
        if widget_signature not in self.knowledge_map[page_name]:
            self.knowledge_map[page_name][widget_signature] = {
                'action_count': defaultdict(lambda: 0),
                'recent_role_inference': None
            }
        
        widget_knowledge = self.knowledge_map[page_name][widget_signature]['action_count']
        widget_knowledge[performed_action.event_type] += 1

        if performed_action.event_type == 'scroll':
            event_type = f'{performed_action.event_type} {performed_action.direction}'
        else:
            event_type = performed_action.event_type
        if event_type not in self.performed_action_types_for_task[(page_name, widget_signature)]:
            self.performed_action_types_for_task[(page_name, widget_signature)][event_type] = 0
        self.performed_action_types_for_task[(page_name, widget_signature)][event_type] += 1

        self.add_knowledge(state, 'WIDGET', page=page_name, widget=widget_signature, action=performed_action.action_type_signature, observation=observation, task=task)


    def update_widget_knowledge_with_none_observation(self, state, page_name, widget, performed_action, task):
        widget_signature = widget.signature
        assert widget_signature is not None, f'widget signature is None: {widget}'
        assert page_name is not None, f'page name is None'
        if page_name not in self.knowledge_map:
            self.knowledge_map[page_name] = {}
        if widget_signature not in self.knowledge_map[page_name]:
            self.knowledge_map[page_name][widget_signature] = {
                'action_count': defaultdict(lambda: 0),
                'recent_role_inference': None
            }
        
        widget_knowledge = self.knowledge_map[page_name][widget_signature]['action_count']
        widget_knowledge[performed_action.event_type] += 1

        if performed_action.event_type == 'scroll':
            event_type = f'{performed_action.event_type} {performed_action.direction}'
        else:
            event_type = performed_action.event_type
        if event_type not in self.performed_action_types_for_task[(page_name, widget_signature)]:
            self.performed_action_types_for_task[(page_name, widget_signature)][event_type] = 0
        self.performed_action_types_for_task[(page_name, widget_signature)][event_type] += 1


    def update_widget_knowledge_summary(self, page_name, widget, summary):
        widget_signature = widget.signature
        assert widget_signature is not None, f'widget signature is None: {widget}'
        assert page_name is not None, f'page name is None'
        if page_name not in self.knowledge_map:
            self.knowledge_map[page_name] = {}
        if widget_signature not in self.knowledge_map[page_name]:
            self.knowledge_map[page_name][widget_signature] = {
                'action_count': defaultdict(lambda: 0),
                'recent_role_inference': None
            }
        
        self.knowledge_map[page_name][widget_signature]['recent_role_inference'] = summary

    def retrieve_task_knowledge_by_state(self, N=5):
        # TODO: prioritize recent task knowledge
        query = self.current_gui_state.signature

        relevant_entries = self.knowledge.query(
            query_texts=[query],
            n_results=N,
            where={'type': 'TASK'}
        )

        relevant_entries = {
            'ids': relevant_entries['ids'][0],
            'metadatas': relevant_entries['metadatas'][0],
            'documents': relevant_entries['documents'][0]
        }

        return self.__stringify_knowledge(relevant_entries, prop_to_show='reflection')

    
    def retrieve_widget_knowledge_by_state(self, page_name, widget, N=5, prompt_recorder=None):
        query = self.current_gui_state.signature
        widget_signature = widget.signature

        relevant_entries = self.knowledge.query(
            query_texts=[query],
            n_results=N,
            where={'$and': [{'type': 'WIDGET'}, {'page': page_name}, {'widget': widget_signature}]}
        )

        relevant_entries = {
            'ids': relevant_entries['ids'][0],
            'metadatas': relevant_entries['metadatas'][0],
            'documents': relevant_entries['documents'][0]
        }

        relevant_widget_observations = self.__stringify_knowledge(relevant_entries, prop_to_show='observation')

        if len(relevant_widget_observations) == 0:
            return None

        summary = prompt_summarized_widget_knowledge(self, widget.stringify(), relevant_widget_observations, prompt_recorder=prompt_recorder)

        self.update_widget_knowledge_summary(page_name, widget, summary)

        return summary

    
    def __stringify_knowledge(self, raw_entries, max_len=None, prop_to_show='reflection'):
        entries = []
        for memory_id, metadata, state in zip(raw_entries['ids'], raw_entries['metadatas'], raw_entries['documents']):
            
            knowledge = metadata[prop_to_show]
            if len(knowledge) == 0:
                continue
            if prop_to_show == 'observation':
                action_type = metadata['action']
                entries.append((int(memory_id), f'- result of {action_type}: {knowledge}\n'))
            else:
                entries.append((int(memory_id), f'- {knowledge}\n'))

        if len(entries) == 0:
            return ''
            
        entries.sort(key=lambda x: x[0])
        if max_len is not None and isinstance(max_len, int):
            entries = entries[max(-max_len, -len(entries)):]
        
        memory_str = ''
        for memory_id, entry in entries:
            memory_str += entry

        return memory_str.strip()

    def collect_knowledge(self):
        raw_entries = self.knowledge.get()
        
        task_knowledge = []
        widget_knowledge = defaultdict(lambda: defaultdict(list))

        for memory_id, metadata, state in zip(raw_entries['ids'], raw_entries['metadatas'], raw_entries['documents']):
            prop_to_show = 'reflection'
            if metadata['type'] == 'WIDGET':
                prop_to_show = 'observation'
            
            knowledge = metadata[prop_to_show]
            if len(knowledge) == 0:
                continue
            if prop_to_show == 'observation':
                action_type = metadata['action']
                widget_knowledge[metadata['page']][metadata['widget']].append((int(memory_id), (action_type, knowledge)))
            else:
                task_knowledge.append((int(memory_id), (metadata['task'], knowledge)))

        widget_knowledge_with_summary = defaultdict(lambda: defaultdict(dict))

        for page_name, widgets in widget_knowledge.items():
            for widget_signature, entries in widgets.items():
                entries.sort(key=lambda x: x[0])
                widget_knowledge_with_summary[page_name][widget_signature] = {
                    'summary': None,
                    'entries': [entry[1] for entry in entries],
                }

        for page_name in self.knowledge_map:
            for widget_signature in self.knowledge_map[page_name]:
                if widget_signature in widget_knowledge_with_summary[page_name]:
                    widget_knowledge_with_summary[page_name][widget_signature]['summary'] = self.knowledge_map[page_name][widget_signature]
                else:
                    widget_knowledge_with_summary[page_name][widget_signature] = {
                        'summary': self.knowledge_map[page_name][widget_signature],
                    }

        task_knowledge.sort(key=lambda x: x[0])
        task_knowledge = [entry[1] for entry in task_knowledge]

        return task_knowledge, widget_knowledge_with_summary
            
    def save_snapshot(self, output_dir):
        working_memory_record = []
        for desc, record_type, timestamp, page in self.working_memory:
            working_memory_record.append({
                'description': str(desc),
                'type': record_type,
                'timestamp': timestamp,
                'page': page
            })

        scratch = {
            'task': self.task,
            'task_end_condition': self.task_end_condition,
            'previous_activity': self.previous_activity,
            'current_activity': self.current_activity,
            'visited_activities': self.visited_activities,
            'all_activities': agent_config.app_activities,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            'current_activity_coverage': len(self.visited_activities) / len(agent_config.app_activities),
            'working_memory': working_memory_record,
        }

        with open(os.path.join(output_dir, 'scratch.json'), 'w') as f:
            json.dump(scratch, f, indent=2)

        with open(os.path.join(output_dir, 'long_term_memory.txt'), 'w') as f:
            long_term_memory_str = self.__str__()
            f.write(long_term_memory_str)

        task_knowledge, widget_knowledge = self.collect_knowledge()

        with open(os.path.join(output_dir, 'task_knowledge.json'), 'w') as f:
            json.dump(task_knowledge, f, indent=2)
        
        with open(os.path.join(output_dir, 'widget_knowledge.json'), 'w') as f:
            json.dump(widget_knowledge, f, indent=2)

    def describe_current_plan(self):
        assert self.current_plan is not None

        plan_steps = ''
        for i, step in enumerate(self.current_plan):
            plan_steps += f'({i+1}) {remove_period(step)} '

        return plan_steps.strip()

    def query_relevant_entries(self, mode):
        # FIXME: retrieval scheme (importance, relevance, recency, etc.)
        if mode == 'plan':
            entries = self.memory.get()
            return self.__stringify(entries, show_timestamps=True, show_type=False, max_len=100)

        elif mode == 'act':
            entries = self.memory.get()
            return self.__stringify(entries, show_timestamps=True, show_type=False, max_len=100)

        elif mode == 'reflect':
            entries = self.memory.get()
            return self.__stringify(entries, show_timestamps=True, show_type=False, max_len=100)
    
    def set_current_gui_state(self, gui_state):
        self.previous_gui_state = self.current_gui_state
        self.current_gui_state = gui_state

    def add_visited_activity(self, activity):
        if activity in agent_config.app_activities: # internal page
            self.visited_activities[activity] += 1

            if self.task is not None:
                self.visited_pages_for_task[activity] += 1

        self.previous_activity = self.current_activity if self.current_activity is not None else activity
        self.current_activity = activity

    def retrieve_task_history(self):
        entries = self.memory.get(where={'$or': [
            # {'$and': [{'type': 'TASK'}, {'task_result': 'SUCCESS'}]}, 
            # {'$and': [{'type': 'TASK_RESULT'}, {'task_result': 'SUCCESS'}]}, 
            {'type': 'TASK_RESULT'}, 
            {'type': 'INITIAL_KNOWLEDGE'}
        ]})

        return self.__stringify(entries, show_timestamps=True, show_type=False, max_len=20)

    def get_entry(self, entry_id):
        entry = self.memory.get(ids=[str(entry_id)])
        if len(entry['documents']) == 0:
            return None
        return entry

    def update_task_result(self, task_result):
        self.memory.upsert(
            new_entry
        )

    def add_task_result(self, task_result, task_result_summary):
        # Update task information
        task_entry = self.get_entry(self.task_memory_entry_id)
        assert task_entry is not None, f'Task {self.memory.task} does not exist in the memory'
        task_entry['metadatas'][0]['task_result'] = task_result
        self.memory.upsert(**task_entry)

        # Add separate entry for the task result
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.memory_entry_id += 1
        self.memory.add(
            documents=[task_result_summary.strip()],
            metadatas=[{"type": "TASK_RESULT", "timestamp": timestamp, "task": self.task, "task_result": task_result}],
            ids=[str(self.memory_entry_id)]
        )
        return str(self.memory_entry_id)

    def add_task(self, task):
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.memory_entry_id += 1
        
        self.memory.add(
            documents=[task.strip()],
            metadatas=[{"type": "TASK", "timestamp": timestamp, "task_result": ''}],
            ids=[str(self.memory_entry_id)]
        )
        return str(self.memory_entry_id)

    def add_entry(self, description, type):
        timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.memory_entry_id += 1
        
        self.memory.add(
            documents=[description.strip()],
            metadatas=[{"type": type, "timestamp": timestamp}],
            ids=[str(self.memory_entry_id)]
        )
        return str(self.memory_entry_id)

    def get_entries_after(self, entry_id):
        entry_id = int(entry_id)
        raw_entries = self.memory.get()
        entries = []
        for memory_id, metadata, doc in zip(raw_entries['ids'], raw_entries['metadatas'], raw_entries['documents']):
            if int(memory_id) > entry_id:
                entries.append(self.__stringify_entry(memory_id, metadata, doc, show_timestamps=False))
        entries.sort(key=lambda x: x[0])
        memory_str = ''
        for memory_id, entry in entries:
            memory_str += entry

        return memory_str.strip()

    def get_entries_before(self, entry_id):
        entry_id = int(entry_id)
        raw_entries = self.memory.get()
        entries = []
        for memory_id, metadata, doc in zip(raw_entries['ids'], raw_entries['metadatas'], raw_entries['documents']):
            if int(memory_id) < entry_id:
                entries.append(self.__stringify_entry(memory_id, metadata, doc, show_timestamps=False))
        entries.sort(key=lambda x: x[0])
        memory_str = ''
        for memory_id, entry in entries:
            memory_str += entry

        return memory_str.strip()

    def __str__(self):
        raw_entries = self.memory.get()
        
        return self.__stringify(raw_entries)

    def __stringify_entry(self, memory_id, metadata, doc, show_timestamps=True, show_type=True):
        if show_type:
            doc = f'[{metadata["type"]}] {doc}\n'
        else:
            doc = f'{doc}\n'

        if show_timestamps:
            return (int(memory_id), f'{metadata["timestamp"]}: {doc}')
        else:
            return (int(memory_id), f'{memory_id}. {doc}')


    def __stringify(self, raw_entries, show_timestamps=True, show_type=True, max_len=None):
        entries = []
        for memory_id, metadata, doc in zip(raw_entries['ids'], raw_entries['metadatas'], raw_entries['documents']):
            if len(doc) == 0:
                continue
            entries.append(self.__stringify_entry(memory_id, metadata, doc, show_timestamps=show_timestamps, show_type=show_type))

        if len(entries) == 0:
            return '<no interactions performed yet>'
            
        entries.sort(key=lambda x: x[0])
        if max_len is not None and isinstance(max_len, int):
            entries = entries[max(-max_len, -len(entries)):]
        
        memory_str = ''
        for memory_id, entry in entries:
            memory_str += entry

        return memory_str.strip()

    def append_to_working_memory(self, description, record_type):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        page = self.current_gui_state.activity
        self.working_memory.append((description, record_type, timestamp, page))

    def describe_working_memory(self): # task execution log (for critique and reflection)
        if len(self.working_memory) == 0:
            return '<no interactions performed>'
        memory_str = ''
        for i, (entry, item_type, timestamp, page) in enumerate(self.working_memory):
            if isinstance(entry, Action):
                entry = entry.get_action_record_str()
            if item_type == 'CRITIQUE':
                continue # hide previous critiques to avoid bias
            
            memory_str += f'{timestamp}:{page}: [{item_type}] {entry}\n'
        
        return memory_str.strip()
        
    def make_thread_from_working_memory(self):
        # This should be called when we need a next action from the LLM
        WM = list(enumerate(self.working_memory))
        
        user_messages_draft = []
        user_messages = []
        assistant_messages = []

        BASIC_FEEDBACK_MESSAGE = lambda page_change: f'I performed the action you suggested. What should be the next action?' if page_change is None else f'I performed the action you suggested. The page changed from {page_change[0]} to {page_change[1]}. What should be the next action?'

        prev_critique = None
        previous_item_type = None
        has_critique = False

        need_feedback_message = False

        for i, (entry, item_type, timestamp, page) in WM:
            if item_type == 'ACTION':
                if need_feedback_message:
                    user_messages_draft.append((BASIC_FEEDBACK_MESSAGE(None), prev_critique, page))
                    prev_critique = None
                if isinstance(entry, Action):
                    assistant_messages.append(entry.get_action_str())
                else:
                    assistant_messages.append(str(entry))
                need_feedback_message = True

            elif item_type == 'CRITIQUE':
                # append to the last observation
                if previous_item_type == 'OBSERVATION':
                    user_messages_draft[-1] = (user_messages_draft[-1][0], entry, user_messages_draft[-1][2])
                elif previous_item_type == 'ACTION':
                    prev_critique = entry
                has_critique = True
                
            elif item_type == 'OBSERVATION':
                assert previous_item_type == 'ACTION'
                user_messages_draft.append((f'''
I performed the action, and as a result, {entry[0].lower() + add_period(entry[1:])} What should be the next action?'''.strip(), None, page))

                need_feedback_message = False

            previous_item_type = item_type

        if need_feedback_message:
            user_messages_draft.append((BASIC_FEEDBACK_MESSAGE(None), prev_critique, WM[-1][1][3]))

        # Final conversation generation: only include the last observation and last critique (if there is not critique, mention the initial plan made by planner)
        ignore_observations = False
        ignore_critiques = False

        for feedback_message, critique, page in user_messages_draft[::-1]:
            if ignore_observations:
                page_change = None
                m = re.search(r'(\(page changed from (.+) to (.+)\))', feedback_message)
                if m is not None:
                    page_change = (m.group(2), m.group(3))

                feedback_message = BASIC_FEEDBACK_MESSAGE(page_change)

            else:
                ignore_observations = True

            if not ignore_critiques and critique is not None:
                feedback_message = feedback_message.replace('What should be the next action?', f'''
However, I got the following critique for my actions so far: 
> Criticizer: "{add_period(critique)}" 
Considering the critique, what should be the next action?'''.strip())
                
                ignore_critiques = True

            user_messages.insert(0, feedback_message)

        initial_plan = f'{add_period(self.initial_task_plan)} ' if not has_critique else ''

        first_user_message = f'''
My name is {agent_config.persona_name} and I am using an application named {agent_config.app_name} to accomplish the following task: 
* Task: {self.task} ({remove_period(self.task_end_condition)})

I'm currently on the {self.task_start_state.activity} page. {initial_plan}What should be the first action?
        '''.strip()

        user_messages.insert(0, first_user_message)

        return user_messages, assistant_messages
