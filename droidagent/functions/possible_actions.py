from ..action import *
from ..config import agent_config

class Context:
    def __init__(self):
        self.actiontype2widgets = {}

    def set_widgets(self, actiontype2widgets):
        self.actiontype2widgets = actiontype2widgets
        
        self.scrollable_widget_ids = list(self.actiontype2widgets['scroll'].keys())
        self.scrollable_widget_ids.sort()
        self.clickable_widget_ids = list(self.actiontype2widgets['touch'].keys())
        self.clickable_widget_ids.sort()
        self.long_clickable_widget_ids = list(self.actiontype2widgets['long_touch'].keys())
        self.long_clickable_widget_ids.sort()
        self.editable_widget_ids = list(self.actiontype2widgets['set_text'].keys())
        self.editable_widget_ids.sort()

        self.widget_ids = self.scrollable_widget_ids + self.clickable_widget_ids + self.long_clickable_widget_ids + self.editable_widget_ids
        self.widget_ids.sort()

    def get_widget_ids(self):
        return self.widget_ids

    def get_scrollable_widget_ids(self):
        return self.scrollable_widget_ids

    def get_scrollable_widget(self, widget_id):
        return self.actiontype2widgets['scroll'].get(widget_id, None)

    def get_clickable_widget_ids(self):
        return self.clickable_widget_ids

    def get_clickable_widget(self, widget_id):
        return self.actiontype2widgets['touch'].get(widget_id, None)

    def get_long_clickable_widget_ids(self):
        return self.long_clickable_widget_ids
    
    def get_long_clickable_widget(self, widget_id):
        return self.actiontype2widgets['long_touch'].get(widget_id, None)

    def get_editable_widget_ids(self):
        return self.editable_widget_ids

    def get_editable_widget(self, widget_id):
        return self.actiontype2widgets['set_text'].get(widget_id, None)


current_context = Context()

def end_task():
    return None, None

def create_end_task_definition():
    return {
        "type": "function",
        "function": {
            "name": "end_task",
            "description": "Use this function to end the current task.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }, end_task


def go_back():
    return initialize_go_back_action(), None

def create_go_back_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "go_back",
            "description": "Use this function to navigate back to the previous screen.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }, go_back


# def press_enter():
#     return initialize_enter_key_action(), None

# def create_press_enter_action_definition():
#     return {
#         "name": "press_enter",
#         "description": "Use this function to press the \"ENTER\" key to confirm your previous text input.",
#         "parameters": {
#             "type": "object",
#             "properties": {}
#         }
#     }, press_enter


def press_search_key():
    return initialize_search_key_action(), None

def create_press_search_key_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "press_search_key",
            "description": "Use this function to press the \"SEARCH\" key submit a search query when the search bar is focused and you finished typing your query.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }, press_search_key

def wait():
    return Action().from_props('wait'), None

def create_wait_definition():
    return {
        "type": "function",
        "function": {
            "name": "wait",
            "description": "Use this function not to perform any action and wait for a loading process to finish.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }, wait


def scroll(direction, target_widget_ID):
    target_widget = current_context.get_scrollable_widget(target_widget_ID)

    if target_widget is None:
        # return None, f'The widget with ID {target_widget_ID} is not scrollable. Please select other scrollable widget (Possible widget IDs: {current_context.get_scrollable_widget_ids()})'
        return None, f'The widget with ID {target_widget_ID} does not support "scroll" action type. Please select other scrollable widget or other possible action type on the widget.'

    return Action().from_props("scroll", direction=direction, target_widget=target_widget), None

def create_scroll_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "scroll",
            "description": "Use this function to scroll on the target widget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["UP", "DOWN", "LEFT", "RIGHT"],
                        "description": "The direction to scroll the target scrollable widget",
                    },
                    "target_widget_ID": {
                        "type": "integer",
                        "enum": current_context.get_scrollable_widget_ids(),
                        "description": "The \"ID\" property of the target widget in the current GUI state. The target widget must have \"scroll\" in its possible_action_types property.",
                    }
                },
                "required": ["direction", "target_widget_ID"]
            }
        }
    }, scroll


def touch(target_widget_ID):
    target_widget = current_context.get_clickable_widget(target_widget_ID)

    if target_widget is None:
        return None, f'The widget with ID {target_widget_ID} does not support "touch" action type. Please select other touchable widget or other possible action type on the widget.'

    return Action().from_props("touch", target_widget=target_widget), None

def create_touch_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "touch",
            "description": "Use this function to touch on the target widget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_widget_ID": {
                        "type": "integer",
                        "enum": current_context.get_clickable_widget_ids(),
                        "description": "The \"ID\" property of the target widget in the current GUI state. The target widget must have \"touch\" in its possible_action_types property.",
                    }
                },
                "required": ["target_widget_ID"]
            }
        }
    }, touch


def long_touch(target_widget_ID):
    target_widget = current_context.get_long_clickable_widget(target_widget_ID)

    if target_widget is None:
        return None, f'The widget with ID {target_widget_ID} does not support "long_touch" action type. Please select other long-touchable widget or other possible action type on the widget.'

    return Action().from_props("long_touch", target_widget=target_widget), None

def create_long_touch_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "long_touch",
            "description": "Use this function to long touch on the target widget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_widget_ID": {
                        "type": "integer",
                        "enum": current_context.get_long_clickable_widget_ids(),
                        "description": "The \"ID\" property of the target widget in the current GUI state. The target widget must have \"long_touch\" in its possible_action_types property.",
                    }
                },
                "required": ["target_widget_ID"]
            }
        }
    }, long_touch


def set_text(target_widget_ID):
    target_widget = current_context.get_editable_widget(target_widget_ID)

    if target_widget is None:
        return None, f'The widget with ID {target_widget_ID} does not support "set_text" action type. Please select other widget that has "set_text" in its possible_action_types property or other possible action type on the widget.'

    return Action().from_props("set_text", target_widget=target_widget), None

def create_set_text_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "set_text",
            "description": f"Use this function to fill in the target textfield.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_widget_ID": {
                        "type": "integer",
                        "enum": current_context.get_editable_widget_ids(),
                        "description": "The \"ID\" property of the target widget in the current GUI state. The target widget must have \"set_text\" in its possible_action_types property.",
                    }
                },
                "required": ["target_widget_ID"]
            }
        }
    }, set_text


def set_text_self_contained(target_widget_ID, text):
    target_widget = current_context.get_editable_widget(target_widget_ID)

    if target_widget is None:
        return None, f'The widget with ID {target_widget_ID} does not support "set_text" action type. Please select other widget that has "set_text" in its possible_action_types property or other possible action type on the widget.'

    return Action().from_props("set_text", target_widget=target_widget, text=text), None

def create_set_text_self_contained_action_definition():
    return {
        "type": "function",
        "function": {
            "name": "set_text",
            "description": f"Use this function to fill in the target textfield.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_widget_ID": {
                        "type": "integer",
                        "enum": current_context.get_editable_widget_ids(),
                        "description": "The \"ID\" property of the target widget in the current GUI state. The target widget must have \"set_text\" in its possible_action_types property.",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to fill in the target textfield.",
                    }
                },
                "required": ["target_widget_ID", "text"]
            }
        }
    }, set_text_self_contained
