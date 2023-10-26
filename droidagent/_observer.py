import os
import time
import random
import logging

from .config import agent_config

from .prompts.summarize_state import summarize_state_change

class Observer:
    def __init__(self, memory, prompt_recorder=None):
        self.logger = logging.getLogger('agent')
        self.memory = memory
        self.prompt_recorder = prompt_recorder

    def observe_action_result(self):
        previous_action = self.memory.previous_action
        assert previous_action is not None # only observe after an action is taken
        
        state_change = summarize_state_change(self.memory, self.prompt_recorder)

        if self.memory.previous_activity != self.memory.current_activity:
            if state_change is None:
                state_change = f'The page changed from {self.memory.previous_activity} to {self.memory.current_activity}'
            state_change += f' (page changed from {self.memory.previous_activity} to {self.memory.current_activity})'

        if state_change is None:
            if previous_action.target_widget is not None and previous_action.target_widget.signature is not None:
                self.memory.update_widget_knowledge_with_none_observation(self.memory.previous_gui_state.signature, self.memory.previous_activity, previous_action.target_widget, previous_action, self.memory.task)
            return None

        self.memory.append_to_working_memory(state_change, 'OBSERVATION')
        
        if previous_action.target_widget is not None and previous_action.target_widget.signature is not None:
            self.memory.update_widget_knowledge(self.memory.previous_gui_state.signature, self.memory.previous_activity, previous_action.target_widget, previous_action, state_change, self.memory.task)

        return state_change

    def detect_state_change(self, old_state, new_state):
        # Fine-grained observation of the state change, avoiding hallucination
        changed_widgets = []
        new_widgets = []
        disappeared_widgets = []

        old_widgets = {}

        for w in old_state.widgets:
            if w.widget_description is None:
                continue
            key = w.signature
            old_widgets[key] = w

        existing_widgets = []
        for w in new_state.widgets:
            if w.widget_description is None:
                continue
            key = w.signature
            existing_widgets.append(key)

            if key not in old_widgets:
                new_widgets.append((f'New widget appeared: {w.stringify()}', key, new_state.activity))
            else:
                old_w = old_widgets[key]
                if old_w.state_properties != w.state_properties:
                    changed_widgets.append((f'The state of {old_w.stringify(include_modifiable_properties=False)} changed from {old_w.state_properties} to {w.state_properties}', key, new_state.activity))
                elif old_w.widget_description.get('text', None) != w.widget_description.get('text', None):
                    old_text = old_w.widget_description.get('text', "[empty]")
                    new_text = w.widget_description.get('text', "[empty]")
                    if old_text == "[empty]":
                        changed_widgets.append((f'The text "{new_text}" inputted in {old_w.stringify(include_modifiable_properties=False)}', key, new_state.activity))
                    elif new_text == "[empty]":
                        changed_widgets.append((f'The text of {old_w.stringify(include_modifiable_properties=False)} was "{old_text}", but now it is empty', key, new_state.activity))
                    else:
                        changed_widgets.append((f'The text of {old_w.stringify(include_modifiable_properties=False)} changed from "{old_text}" to "{new_text}"'), key, new_state.activity)

        for w in old_widgets:
            if w not in existing_widgets:
                disappeared_widgets.append((f'The widget disappeared: {old_widgets[w].stringify()}', key, old_state.activity))

        return new_widgets + changed_widgets + disappeared_widgets
