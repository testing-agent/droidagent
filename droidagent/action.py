from .utils import __safe_dict_get, __get_all_children
from .config import agent_config

from collections import defaultdict
from droidbot.input_event import SetTextEvent, ScrollEvent, TouchEvent, LongTouchEvent, KeyEvent
import json

class Action:
    def __init__(self):
        self.event_type = None
        self.target_widget = None
        self.text = None    # for set_text event
        self.direction = None  # for scroll event
        self.name = None    # for key event
        self.events = []

    def from_props(self, event_type, text=None, direction=None, name=None, target_widget=None):
        self.event_type = event_type
        self.target_widget = target_widget

        if text is not None:
            self.text = text
        if direction is not None:
            self.direction = direction
        if name is not None:
            self.name = name

        return self

    def from_dict(self, action_dict, target_widget=None):
        self.event_type = action_dict['event_type']
        self.target_widget = target_widget
        if 'text' in action_dict:
            self.text = action_dict['text']
        if 'direction' in action_dict:
            self.direction = action_dict['direction'].lower()

        return self

    def to_dict(self):
        return {
            'event_type': self.event_type,
            'target_widget': str(self.target_widget) if self.target_widget is not None else None,
            'text': self.text,
            'direction': self.direction
        }

    @property
    def action_type_signature(self):
        if self.event_type == 'scroll':
            return f'{self.event_type} {self.direction}'
        elif self.event_type == 'set_text':
            return f'{self.event_type} {self.text}'
        else:
            return self.event_type


    def add_event_records(self, event_records):
        self.events = event_records

    def to_droidbot_event(self):
        if self.event_type == 'touch':
            return [TouchEvent(view=self.target_widget.elem_dict)]
        elif self.event_type == 'long_touch':
            return [LongTouchEvent(view=self.target_widget.elem_dict)]
        elif self.event_type == 'scroll':
            return [ScrollEvent(view=self.target_widget.elem_dict if self.target_widget is not None else None, direction=self.direction)]
        elif self.event_type == 'set_text':
            return [SetTextEvent(view=self.target_widget.elem_dict, text=self.text)]
        elif self.event_type == 'key':
            return [KeyEvent(name=self.name)]
        elif self.event_type == 'wait':
            return [None]

    def get_action_type(self):
        if self.event_type == 'scroll':
            return f'{self.event_type} {self.direction}'
        else:
            return self.event_type

    def update_event_type(self, event_type):
        self.event_type = event_type

    def update_input_text(self, input_text):
        assert self.event_type == 'set_text', 'Cannot update input text for non-set_text event'
        self.text = input_text

    def update_direction(self, direction):
        assert self.event_type == 'scroll', 'Cannot update direction for non-scroll event'
        assert direction in ['UP', 'DOWN', 'LEFT', 'RIGHT'], 'Invalid direction for scroll event'
        self.direction = direction

    def get_action_record_str(self):
        action_str = ''
        if self.event_type == 'start_app':
            action_str = f'{agent_config.persona_name} started the app'
        if self.event_type == 'stop_app':
            action_str = f'{agent_config.persona_name} stopped the app'

        if self.event_type == 'key':
            if self.name == 'BACK':
                action_str = f'{agent_config.persona_name} pressed "BACK" button to navigate back'
            if self.name == 'KEYCODE_ENTER':
                action_str = f'{agent_config.persona_name} pressed "ENTER" key'

        if self.event_type == 'wait':
            action_str = f'{agent_config.persona_name} waited for a loading state to finish'

        if self.event_type in ['set_text', 'scroll', 'touch', 'long_touch']:
            if self.target_widget is not None:
                widget_info = str(self.target_widget)
            else:
                widget_info = 'the screen'
            if self.event_type == 'set_text':
                action_str = f'{agent_config.persona_name} filled {widget_info} with the text "{self.text}"'
            elif self.event_type == 'scroll':
                action_str = f'{agent_config.persona_name} scrolled {self.direction.lower()} on {widget_info}'
            elif self.event_type == 'touch':
                action_str = f'{agent_config.persona_name} touched on {widget_info}'
            elif self.event_type == 'long_touch':
                action_str = f'{agent_config.persona_name} long touched on {widget_info}'

        return action_str

    def get_action_str(self):
        action_str = ''
        if self.event_type == 'start_app':
            action_str = f'Start app'
        if self.event_type == 'stop_app':
            action_str = f'Stop app'

        if self.event_type == 'key':
            if self.name == 'BACK':
                action_str = f'Press "BACK" button to navigate back'
            if self.name == 'KEYCODE_ENTER':
                action_str = f'Press "ENTER" key'

        if self.event_type == 'wait':
            action_str = f'Wait for a loading state to finish'

        if self.event_type in ['set_text', 'scroll', 'touch', 'long_touch']:
            if self.target_widget is not None:
                widget_info = str(self.target_widget)
            else:
                widget_info = 'the screen'
            if self.event_type == 'set_text':
                action_str = f'Fill {widget_info} with "{self.text}"'
            elif self.event_type == 'scroll':
                action_str = f'Scroll {self.direction.lower()} on {widget_info}'
            elif self.event_type == 'touch':
                action_str = f'Touch on {widget_info}'
            elif self.event_type == 'long_touch':
                action_str = f'Long touch on {widget_info}'

        return action_str

    def get_reproducible_record(self):
        # FIXME: need to clean up
        record = {
            'action_type': self.event_type,
            'text': self.text,
            'direction': self.direction,
            'name': self.name,
            'target_widget_resource_id': self.target_widget.resource_id if self.target_widget is not None else None,
            'target_widget_content_description': self.target_widget.content_description if self.target_widget is not None else None,
            'target_widget_text': self.target_widget.text if self.target_widget is not None else None,
            'target_widget_bounds': self.target_widget.bounds if self.target_widget is not None else None,
        }
        return record

    def __str__(self):
        return self.get_action_str()


def convert_set_text_event_to_touch_event(event):
    assert isinstance(event, SetTextEvent), 'Cannot convert non-set_text event to touch event'
    return TouchEvent(view=event.view)

def initialize_possible_actions(action_type, target_widget):
    if action_type == 'touch':
        return [Action().from_props("touch", target_widget=target_widget)]
    elif action_type == 'long_touch':
        return [Action().from_props("long_touch", target_widget=target_widget)]
    elif action_type == 'scroll':
        return [Action().from_props("scroll", direction="UP", target_widget=target_widget)]
    elif action_type == 'set_text':
        return [Action().from_props("set_text", text="test", target_widget=target_widget)]
    
    return []

def initialize_screen_scroll_action():
    return Action().from_props("scroll", direction="UP")

def initialize_go_back_action():
    return Action().from_props("key", name="BACK")

def initialize_enter_key_action():
    return Action().from_props("key", name="KEYCODE_ENTER")
