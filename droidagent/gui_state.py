from collections import defaultdict
from .config import agent_config
from .action import initialize_possible_actions, initialize_screen_scroll_action, initialize_go_back_action, initialize_enter_key_action
from .utils import GUIStateManager, remove_quotes

from collections import OrderedDict
from functools import cached_property

import json
import copy
import difflib
import logging

CONTEXT_LENGTH_LIMIT = 15000

def minimize_view_tree(view_tree):
    view_tree = copy.deepcopy(view_tree)
    
    new_root_elems = []
    for root_elem in prune_elements(view_tree):
        new_root_elems.extend(additionally_prune_elements(root_elem))

    return new_root_elems


def is_meaningful_element(elem):
    if not elem.get('visible', False):
        return False

    if not elem.get('enabled', False):
        return False
    
    if elem.get('package') == 'com.android.documentsui': # hotfix for DocumentsUI (removed screenshot files are cached)
        file_picker_elem_text = elem.get('text')
        if file_picker_elem_text is not None:
            file_picker_elem_text = file_picker_elem_text.strip()
            if file_picker_elem_text.startswith('screen_') and file_picker_elem_text.endswith('.png'):
                elem['children'] = []
                del elem['text']
                return False

        file_picker_elem_content_desc = elem.get('content_description')
        if file_picker_elem_content_desc is not None and 'Photo taken on' in file_picker_elem_content_desc:
            elem['children'] = []
            del elem['content_description']
            return False

        if elem.get('resource_id') == 'android:id/title':
            elem['clickable'] = True
            return True

    if any(elem.get(property_name, False) for property_name in ['clickable', 'long_clickable', 'editable', 'scrollable', 'checkable']):
        return True 
    if elem.get('text') is not None and len(elem['text'].strip()) > 0:
        return True

    return False

def traverse_widgets(elem, widget_list, view_list):
    new_elem = OrderedDict()
    possible_action_types = []
    state_properties = []

    if elem.get('clickable', False) or elem.get('checkable', False):
        possible_action_types.append('touch')
    if elem.get('long_clickable', False):
        possible_action_types.append('long_touch')
    if elem.get('editable', False):
        possible_action_types.append('set_text')
    if elem.get('scrollable', False):
        possible_action_types.append('scroll')

    if elem.get('focused', False):
        state_properties.append('focused')
    if elem.get('checked', False):
        state_properties.append('checked')
    if elem.get('selected', False):
        state_properties.append('selected')

    if 'temp_id' in elem and len(possible_action_types) > 0:
        elem_ID = elem['temp_id']
        new_elem['ID'] = elem_ID
        new_elem['view_str'] = view_list[elem_ID]['view_str']
    if 'class' in elem:
        new_elem['widget_type'] = elem['class'].split('.')[-1]
        new_elem['class'] = elem['class']
    if 'text' in elem and elem['text'] is not None and len(elem['text'].strip()) > 0:
        new_elem['text'] = elem['text'] if len(elem['text']) < 100 else elem['text'][:100] + '[...]'
    if 'content_description' in elem and elem['content_description'] is not None:
        new_elem['content_description'] = elem['content_description']
    if 'resource_id' in elem and elem['resource_id'] is not None:
        new_elem['resource_id'] = elem['resource_id'].split('/')[-1]
    if 'is_password' in elem and elem['is_password']:
        new_elem['is_password'] = True
    if len(state_properties) > 0:
        new_elem['state'] = state_properties
    if len(possible_action_types) > 0:
        new_elem['possible_action_types'] = possible_action_types

    if 'view_str' in elem:
        new_elem['view_str'] = elem['view_str']

    new_elem['bounds'] = elem['bounds']

    children_widgets = []
    for child in elem.get('children', []):
        children_widgets.append(traverse_widgets(child, widget_list, view_list))
    
    new_elem['children'] = children_widgets

    widget = Widget().from_dict(new_elem)
    
    widget_list.append(widget)

    return widget

def prune_elements(json_data):
    if is_meaningful_element(json_data):
        # If the current node is interactable or has a text property, recursively prune its children
        if "children" in json_data and isinstance(json_data["children"], list):
            new_children = []
            for child in json_data["children"]:
                new_children.extend(prune_elements(child))
            json_data["children"] = new_children
        return [json_data]
    else:
        # If the current node either is not interactable or doesn't have a text property, recursively prune its children and lift them
        if "children" in json_data:
            lifted_children = []
            for child in json_data["children"]:
                lifted_children.extend(prune_elements(child))
            return lifted_children
        return []

def additionally_prune_elements(json_data):
    # if the current node has only one child that doesn't have any children, lift the child
    if len(json_data.get('children', [])) == 1 and len(json_data['children'][0].get('children', [])) == 0:
        only_child = json_data['children'][0]
        if any(only_child.get(property_name, False) for property_name in ['clickable', 'long_clickable', 'editable', 'scrollable', 'checkable']):
            return [json_data]

        if only_child.get('text') is not None and len(only_child['text'].strip()) > 0 and json_data.get('text') is None:
            json_data['text'] = only_child['text']
            json_data['children'] = []

    return [json_data]

class GUIState:
    def __init__(self):
        self.tag = None
        self.activity = None
        self.droidbot_state = None
        self.activity_stack = []
        self.possible_actions = []
        self.lost_messages = set()
        self.logger = logging.getLogger('agent')

    def from_droidbot_state(self, droidbot_state):
        """
        Convert the view tree and view list from DroidBot to a GUI state
        :param _view_tree: dict, the view tree from DroidBot
        """
        self.droidbot_state = droidbot_state
        self.activity = GUIStateManager.fix_activity_name(droidbot_state.foreground_activity)
        self.activity_stack = droidbot_state.activity_stack
        self.tag = droidbot_state.tag
        view_tree = minimize_view_tree(droidbot_state.view_tree)

        self.root_widgets = []
        self.widgets =[]
        for root_elem in view_tree:
            self.root_widgets.append(traverse_widgets(root_elem, self.widgets, droidbot_state.views))

        return self
    
    def get_app_activity_depth(self):
        package_name = agent_config.package_name
        depth = 0
        for activity_str in self.activity_stack:
            if package_name in activity_str:
                return depth
            depth += 1
        
        return -1

    def get_widget_by_id(self, view_id):
        """
        Get the widget with the given view ID
        :param view_id: int, the view ID
        :return: Widget, the widget with the given view ID
        """
        for widget in self.widgets:
            if widget.view_id == view_id:
                return widget
        
        return None

    def get_widget_by_signature(self, signature):
        """
        Get the widget with the given signature
        :param signature: str, the signature
        :return: Widget, the widget with the given signature
        """
        for widget in self.widgets:
            if widget.signature == signature:
                return widget
        
        return None

    def __str__(self):
        return self.describe_screen()

    def describe_screen_w_memory(self, memory, length_limit=CONTEXT_LENGTH_LIMIT, show_id=True, during_task=False, prompt_recorder=None, include_widget_knowledge=True):
        """
        From a given GUI state, creates a description of the GUI state including the list of interactable widgets and non-interactable widgets
        """
        get_performed_actions_func = memory.get_performed_action_types_on_widget
        action_count_key = 'num_prev_actions'

        def inject_widget_knowledge(widget, show_id):
            widget_info = widget.to_dict(include_id=show_id)

            if ('Main' in memory.current_activity or memory.current_activity == agent_config.main_activity) and 'content_description' in widget_info:
                # If "Navigate up" widget is in the main page, change its name to "Menu"
                if widget_info['content_description'].lower() == 'navigate up':
                    widget_info['content_description'] = 'Menu'

            # merge textview children
            text_only_children = [child for child in widget.children if child.widget_type == 'TextView' and len(child.children) == 0 and len(child.possible_action_types) == 0 and child.text is not None]

            children_merged = len(text_only_children) > 0 and len(text_only_children) == len(widget.children) and widget.text is None

            if children_merged:
                # all children are textviews and it does not have text property
                widget_info['text'] = [child.text for child in text_only_children if child.text is not None]
                if len(widget_info['text']) == 0:
                    del widget_info['text']

            if len(widget.possible_action_types) > 0:
                performed_action_types = get_performed_actions_func(self.activity, widget.signature)
                interaction_count = 0
                for action_type in performed_action_types:
                    interaction_count += performed_action_types[action_type]

                widget_info[action_count_key] = interaction_count

                if include_widget_knowledge and memory.get_widget_knowledge(self.activity, widget.signature) is not None:
                    widget_knowledge = memory.retrieve_widget_knowledge_by_state(self.activity, widget, prompt_recorder=prompt_recorder)
                    if widget_knowledge is not None:
                        widget_info['widget_role_inference'] = widget_knowledge

            children_w_knowledge = []

            if not children_merged:
                for child in widget.children:
                    children_w_knowledge.append(inject_widget_knowledge(child, show_id))

            if 'children' in widget_info:
                del widget_info['children']
            if len(children_w_knowledge) > 0:
                widget_info['children'] = children_w_knowledge
            return widget_info

        page_count_key = 'page_visit_count'
        if self.activity not in agent_config.app_activities:
            page_count = '[current page does not belong to the app; just use the page as an intermediate step to accomplish the task]'
        else:
            page_count = memory.visited_activities[self.activity]
        view_hierarchy = {
            'page_name': self.activity,
            page_count_key: page_count,
            'children': []
        }
        for widget in self.root_widgets:
            view_hierarchy['children'].append(inject_widget_knowledge(widget, show_id))

        screen_description = json.dumps(view_hierarchy, indent=2, ensure_ascii=False)

        if length_limit and len(screen_description) > length_limit:
            screen_description = screen_description[:length_limit] + '[...truncated...]'
            self.logger.warning(f'Screen description is too long ({len(screen_description)} > {length_limit}). Truncated. (state tag: {self.tag}))')
        
        screen_description = remove_quotes(screen_description) # remove all quotes to reduce the number of tokens
        return screen_description
    
    def describe_screen(self, length_limit=CONTEXT_LENGTH_LIMIT, show_id=True):
        view_hierarchy = {
            'page_name': self.activity,
            'children': []
        }

        for widget in self.root_widgets:
            view_hierarchy['children'].append(widget.to_dict(include_id=show_id))

        screen_description = json.dumps(view_hierarchy, indent=2, ensure_ascii=False)

        if length_limit and len(screen_description) > length_limit:
            screen_description = screen_description[:length_limit] + '[...truncated...]'
            self.logger.warning(f'Screen description is too long ({len(screen_description)} > {length_limit}). Truncated. (state tag: {self.tag}))')

        screen_description = remove_quotes(screen_description) # remove all double quotes to reduce the number of tokens
        return screen_description

    def describe_widgets(self, length_limit=CONTEXT_LENGTH_LIMIT, show_id=True):
        desc = ''

        for widget in self.widgets:
            desc += widget.dump(indent=None) + '\n'
        
        desc = desc.strip()

        if length_limit and len(desc) > length_limit:
            desc = desc[:length_limit] + '[...truncated...]'
            self.logger.warning(f'Screen description is too long ({len(screen_description)} > {length_limit}). Truncated. (state tag: {self.tag}))')
        
        return desc

    def describe_widgets_NL(self, length_limit=CONTEXT_LENGTH_LIMIT):
        desc = ''

        for widget in self.widgets:
            desc += widget.stringify(include_children_text=False) + '\n'
        
        desc = desc.strip()

        if length_limit and len(desc) > length_limit:
            desc = desc[:length_limit] + '[...truncated...]'
            self.logger.warning(f'Screen description is too long ({len(desc)} > {length_limit}). Truncated. (state tag: {self.tag}))')
        
        return desc

    def diff(self, other):
        """
        Calculate the difference between two GUI states
        """
        diff = difflib.ndiff(self.describe_widgets().splitlines(keepends=True), other.describe_widgets().splitlines(keepends=True))
        return ''.join(diff)

    def diff_widgets(self, other):
        changed_widgets = []
        appeared_widgets = []
        disappeared_widgets = []

        old_widgets = {}
        new_widgets = {}

        for w in self.widgets:
            if w.signature is None:
                continue
            key = w.signature
            old_widgets[key] = w

        for w in other.widgets:
            if w.signature is None:
                continue
            key = w.signature
            new_widgets[key] = w

            if key not in old_widgets:
                appeared_widgets.append(w)
            else:
                old_w = old_widgets[key]
                if old_w.elem_dict.get('state', []) != w.elem_dict.get('state', []):
                    changed_widgets.append((w, {
                        'old_state': old_w.elem_dict.get('state', []),
                        'new_state': w.elem_dict.get('state', [])
                    }))
                elif old_w.elem_dict.get('text', '') != w.elem_dict.get('text', ''):
                    old_text = old_w.elem_dict.get('text', '')
                    new_text = w.elem_dict.get('text', '')
                    changed_widgets.append((w, {
                        'old_text': old_text,
                        'new_text': new_text
                    }))
                    
        for key in old_widgets:
            if key not in new_widgets:
                disappeared_widgets.append(old_widgets[key])

        return changed_widgets, appeared_widgets, disappeared_widgets


    @cached_property
    def signature(self):
        """
        natural language representation of the GUI state (used as a query for associative memory)
        """
        gui_state = f'{self.activity} page: '
        for widget in self.widgets:
            gui_state += f'{widget.stringify()}, '
        return gui_state[:-2]

    @cached_property
    def actiontype2widgets(self):
        actiontype2widgets = defaultdict(dict)
        for w in self.widgets:
            for action_type in w.possible_action_types:
                assert w.view_id is not None, 'interactable widgets must have view ID'
                actiontype2widgets[action_type][w.view_id] = w
        
        return actiontype2widgets

    @cached_property
    def interactable_widget_ids(self):
        interactable_widget_ids = set()
        for w in self.widgets:
            if len(w.possible_action_types) > 0:
                interactable_widget_ids.add(w.view_id)
        return interactable_widget_ids


class Widget:
    def __init__(self):
        self.view_id = None
        self.widget_type = None
        self.possible_action_types = []

    def from_dict(self, elem_dict):
        self.view_id = elem_dict.get('ID', None)
        self.widget_type = elem_dict['widget_type']
        self.possible_action_types = elem_dict.get('possible_action_types', [])
        self.children = elem_dict.get('children', [])

        if 'children' in elem_dict:
            del elem_dict['children']
        
        self.elem_dict = elem_dict

        return self

    def to_dict(self, include_id=True, only_rep_property=True):
        children = [child.to_dict(include_id=include_id) for child in self.children]
        elem_dict = copy.deepcopy(self.elem_dict)

        del elem_dict['class']
        del elem_dict['bounds']
        if not include_id and 'ID' in elem_dict:
            del elem_dict['ID']

        if only_rep_property:
            if 'text' in elem_dict:
                if 'resource_id' in elem_dict:
                    del elem_dict['resource_id']
                if 'content_description' in elem_dict:
                    del elem_dict['content_description']
            
        if 'view_str' in elem_dict:
            del elem_dict['view_str']

        if len(children) > 0:
            elem_dict['children'] = children

        return elem_dict

    @cached_property
    def bounds(self):
        return self.elem_dict['bounds']
        
    @cached_property
    def text(self):
        return self.elem_dict.get('text', None)

    @cached_property
    def resource_id(self):
        return self.elem_dict.get('resource_id', None)

    @cached_property
    def content_description(self):
        return self.elem_dict.get('content_description', None)

    @cached_property
    def all_text(self):
        texts = []
        if self.text is not None and len(self.text.strip()) > 0:
            if len(self.text) > 50:
                texts.append(self.text[:50] + '[...]')
            else:
                texts.append(self.text)

        for child in self.children:
            texts.extend(child.all_text)
        
        return texts

    @cached_property
    def state(self):
        return self.elem_dict.get('state', [])

    @cached_property
    def signature(self):
        immutable_props = ['content_description', 'resource_id']
        if 'set_text' not in self.possible_action_types:
            immutable_props.append('text')

        ingredients = []
        for prop in immutable_props:
            if prop in self.elem_dict and self.elem_dict[prop] is not None and len(self.elem_dict[prop].strip()) > 0:
                ingredients.append(self.elem_dict[prop])
        
        # also use concatenated children's signature
        ingredients.extend([child.signature for child in self.children])

        if len(ingredients) == 0:
            # non-describable widget...
            ingredients = [str(self.elem_dict['bounds'])]

        ingredients.insert(0, self.widget_type)

        return '-'.join(ingredients)

    def __repr__(self):
        return self.dump()

    def __str__(self):
        return self.stringify()

    def dump(self, indent=2):
        """
        Stringify the widget including its children
        {
            "ID": 10,
            "widget_type": "Spinner",
            "resource_id": "com.ichi2.anki:id/toolbar_spinner",
            "possible_action_types": [
                "touch",
                "long_touch",
                "scroll"
            ],
            "children": [
                {
                "widget_type": "TextView",
                "text": "My Filtered Deck",
                "resource_id": "com.ichi2.anki:id/dropdown_deck_name"
                },
                {
                "widget_type": "TextView",
                "text": "6 cards shown",
                "resource_id": "com.ichi2.anki:id/dropdown_deck_counts"
                }
            ]
        }
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def stringify(self, include_children_text=True):
        """
        natural language description of the widget
        """
        widget_type = self.widget_type
        widget_desc = ''

        if len(self.state) > 0:
            state = ', '.join(self.state)
            widget_desc = f'{state} '

        if self.elem_dict.get('is_password', False):
            widget_desc += 'password textfield'
        
        elif 'EditText' in widget_type:
            widget_desc += 'textfield'
        elif 'Button' in widget_type:
            widget_desc += 'button'
        elif 'CheckBox' in widget_type:
            widget_desc += 'checkbox'
        elif 'RadioButton' in widget_type:
            widget_desc += 'radio button'
        elif 'Spinner' in widget_type:
            widget_desc += 'dropdown field'
        elif widget_type.endswith('Tab'):
            widget_desc += 'tab'
        
        else:
            if 'touch' in self.possible_action_types:
                widget_desc += 'button'
            elif 'scroll' in self.possible_action_types:
                widget_desc += 'scrollable area'
            elif 'set_text' in self.possible_action_types:
                widget_desc += 'textfield'
            elif 'TextView' in widget_type:
                widget_desc += 'textview'
            elif 'ImageView' in widget_type:
                widget_desc += 'imageview'
            elif 'LinearLayout' in widget_type:
                widget_desc += 'linearlayout'
            elif 'RelativeLayout' in widget_type:
                widget_desc += 'relativelayout'
            elif 'FrameLayout' in widget_type:
                widget_desc += 'framelayout'
            elif 'GridLayout' in widget_type:
                widget_desc += 'gridlayout'
            elif 'RecyclerView' in widget_type:
                widget_desc += 'recyclerview'
            elif 'ListView' in widget_type:
                widget_desc += 'listview'
            else:
                widget_desc += 'widget'
        
        widget_desc = 'an ' + widget_desc if widget_desc[0] in ['a', 'e', 'i', 'o', 'u'] else 'a ' + widget_desc

        if include_children_text:
            if len(self.all_text) > 3:
                text = ', '.join(self.all_text[:3]) + f'[...and more]'
            else:
                text = ", ".join(self.all_text) if len(self.all_text) > 0 else None
        else:
            text = self.text
        content_description = self.elem_dict.get('content_description', None)
        resource_id = self.elem_dict.get('resource_id', None)

        text_desc = []
        if text is not None:
            text_desc.append(f'text "{text}"')
        elif content_description is not None:
            text_desc.append(f'content_desc "{content_description}"')
        elif resource_id is not None:
            text_desc.append(f'resource_id "{resource_id}"')

        if len(text_desc) > 0:
            text_desc = ' and '.join(text_desc)
            return f'{widget_desc} that has {text_desc}'
        
        return widget_desc
