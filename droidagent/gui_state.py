from collections import defaultdict
from .config import agent_config
from .action import initialize_possible_actions, initialize_screen_scroll_action, initialize_go_back_action, initialize_enter_key_action

import json


class GUIStateManager:
    activity_name_restore_map = {}

    @classmethod
    def fix_activity_name(cls, activity):
        original_activity_name = activity
        activity = activity.split('.')[-1]
        # if activity.startswith('.'):
        #     activity = f'{agent_config.package_name}.{activity[1:]}'
        if activity.endswith('}'):
            activity = activity[:-1]
        if activity.endswith('Activity'):
            activity = activity.removesuffix('Activity')
        elif activity.endswith('activity'):
            activity = activity.removesuffix('activity')

        if activity not in cls.activity_name_restore_map:
            cls.activity_name_restore_map[activity] = original_activity_name

        return activity


class GUIState:
    def __init__(self):
        self.tag = None
        self.activity = None
        self.droidbot_state = None
        self.activity_stack = []
        self.possible_actions = []
        self.interactable_widgets = []
        self.non_interactable_widgets = []
        self.actiontype2widgets = defaultdict(dict)

    @property
    def widgets(self):
        return self.interactable_widgets + self.non_interactable_widgets

    def from_droidbot_state(self, droidbot_state):
        """
        Convert the view tree and view list from DroidBot to a GUI state
        :param _view_tree: dict, the view tree from DroidBot
        """
        _view_tree = droidbot_state.to_dict()
        self.droidbot_state = droidbot_state
        self.activity = GUIStateManager.fix_activity_name(droidbot_state.foreground_activity)
        self.activity_stack = droidbot_state.activity_stack
        self.tag = _view_tree['tag']
        _view_list = _view_tree['views']
        visible_widgets = get_visible_widgets(_view_list)
        interactable_widgets = get_interactable_widgets(visible_widgets)
        
        widget_reprs = {}
        has_textfield = False
        used_view_ids = set()

        # Add interactable widgets and their surrounding context, and register possible actions
        for view_id, possible_action_types in interactable_widgets.items():
            view_dict = visible_widgets[view_id]
            assert view_id == view_dict['temp_id'], 'View ID mismatch'

            text_description, visited_ids = get_description_w_context(view_dict, visible_widgets)
            used_view_ids = used_view_ids.union(visited_ids)

            if view_dict['class'].endswith('RecyclerView') or view_dict['class'].endswith('ListView'):
                contained_items = []

                for item in view_dict['children']:
                    if item not in visible_widgets:
                        continue
                    if len(contained_items) > 3:
                        break
                    item_description = get_description(visible_widgets[item], visible_widgets, consider_resource_id=False)
                    if len(item_description) > 0 and 'text' in item_description and len(item_description['text']) > 0:
                        contained_items.append(item_description['text'][0])
                if len(contained_items) > 0:
                    text_description['contained_items'] = contained_items

            w = Widget(view_dict, text_description)
            if str(w) in widget_reprs:
                continue
            
            widget_reprs[str(w)] = True

            self.interactable_widgets.append(w)

            for action_type in possible_action_types:
                possible_actions = w.register_possible_actions(action_type)
                self.possible_actions.extend(possible_actions)
                self.actiontype2widgets[action_type][w.view_id] = w
                if action_type == 'set_text':
                    has_textfield = True
        
        if len(self.possible_actions) > 0:
            # self.possible_actions.append(initialize_screen_scroll_action())
            self.possible_actions.append(initialize_go_back_action())
        if has_textfield:
            self.possible_actions.append(initialize_enter_key_action())

        # Add visible + textually describable widgets that are not contained in interactable widgets
        for view_id in visible_widgets:
            if view_id in used_view_ids:
                continue
            
            view_dict = visible_widgets[view_id]
            text_description = get_description(view_dict, visible_widgets, consider_children=False, consider_resource_id=False)
            
            w = Widget(view_dict, text_description)
            if str(w) in widget_reprs:
                continue
            if len(text_description) > 0:
                self.non_interactable_widgets.append(w)

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
        for widget in self.interactable_widgets:
            if widget.view_id == view_id:
                return widget
        
        for widget in self.non_interactable_widgets:
            if widget.view_id == view_id:
                return widget

        return None

    def __str__(self):
        return self.describe_screen()


    def describe_screen_w_memory(self, memory, length_limit=6000, mode='NL', show_id=True, use_memory=True, prompt_recorder=None): # mode: 'jsonl' or 'NL'
        """
        From a given GUI state, creates a description of the GUI state including the list of interactable widgets and non-interactable widgets
        """
        screen_description = ''

        if mode == 'jsonl':
            interactable_widgets = sorted(self.interactable_widgets, key=lambda x: x.position)
            non_interactable_widgets = sorted(self.non_interactable_widgets, key=lambda x: x.position)
            
            json_str_interactable = ''
            json_str_non_interactable = ''
            for widget in interactable_widgets:
                widget_info = widget.to_dict()
                if not show_id:
                    del widget_info['ID']
                
                if use_memory:
                    performed_action_types = memory.get_performed_action_types_on_widget(widget.signature)
                    if len(performed_action_types) > 0:
                        widget_info['performed_action_type_count'] = performed_action_types

                        widget_knowledge = memory.retrieve_widget_knowledge_by_state(self.activity, widget, prompt_recorder=prompt_recorder)
                        if widget_knowledge is not None:
                            widget_info['widget_role_inference'] = widget_knowledge
                
                json_str_interactable += json.dumps(widget_info, ensure_ascii=False)
                json_str_interactable += '\n'
            
            for widget in non_interactable_widgets:
                widget_info = widget.to_dict()
                del widget_info['ID']

                json_str_non_interactable += json.dumps(widget_info, ensure_ascii=False)
                json_str_non_interactable += '\n'
            
            json_str = f'''
Interactable widgets:
{json_str_interactable.strip()}

Non-interactable widgets:
{json_str_non_interactable.strip()}
            '''.strip()

            screen_description = json_str.strip()

        elif mode == 'NL':
            screen_description = self.describe_screen_NL()

        else:
            raise NotImplementedError(f'Unknown GUI description mode: {mode} (should be either json or NL)')

        if length_limit and len(screen_description) > length_limit:
            screen_description = screen_description[:length_limit] + '[...truncated...]'
            # FIXME: let the model first see the excerpt of the screen description and further call functions to see additional details

        return screen_description
    

    def describe_screen(self, length_limit=6000, mode='NL', show_id=True): # mode: 'jsonl' or 'NL'
        """
        From a given GUI state, creates a description of the GUI state including the list of interactable widgets and non-interactable widgets
        """
        screen_description = ''

        if mode == 'jsonl':
            interactable_widgets = sorted(self.interactable_widgets, key=lambda x: x.position)
            non_interactable_widgets = sorted(self.non_interactable_widgets, key=lambda x: x.position)
            
            json_str_interactable = ''
            json_str_non_interactable = ''
            for widget in interactable_widgets:
                widget_info = widget.to_dict()
                if not show_id:
                    del widget_info['ID']
                
                json_str_interactable += json.dumps(widget_info, ensure_ascii=False)
                json_str_interactable += '\n'
            
            for widget in non_interactable_widgets:
                widget_info = widget.to_dict()
                del widget_info['ID']

                json_str_non_interactable += json.dumps(widget_info, ensure_ascii=False)
                json_str_non_interactable += '\n'
            
            json_str = f'''
Interactable widgets:
{json_str_interactable.strip()}

Non-interactable widgets:
{json_str_non_interactable.strip()}
            '''.strip()

            screen_description = json_str.strip()

        elif mode == 'NL':
            screen_description = self.describe_screen_NL()

        else:
            raise NotImplementedError(f'Unknown GUI description mode: {mode} (should be either json or NL)')

        if length_limit and len(screen_description) > length_limit:
            screen_description = screen_description[:length_limit] + '[...truncated...]'
            # FIXME: let the model first see the excerpt of the screen description and further call functions to see additional details

        return screen_description

    def describe_screen_NL(self):
        """
        natural language representation of the GUI state
        """
        widgets = sorted(self.interactable_widgets + self.non_interactable_widgets, key=lambda x: x.position)
        # gui_state = 'There are following widgets on this screen: '
        gui_state = '{self.activity} page: '
        if len(widgets) == 0:
            return 'There are no widgets on this screen.'
        for widget in widgets:
            gui_state += f'{widget.stringify()}, '
        for widget in self.non_interactable_widgets:
            gui_state += f'{widget.stringify()}, '
        return gui_state[:-2]

    def describe_possible_actions(self, show_widget_id=False):
        description = ''
        for i, possible_action in enumerate(self.possible_actions):
            description += f'[Action ID: {i}] {possible_action.get_possible_action_str(show_widget_id=show_widget_id)}\n'

        return description.strip()


class Widget:
    def __init__(self, view_dict, text_description):
        self.view_id = view_dict['temp_id']
        self._class = view_dict['class']
        self.position = (view_dict['bounds'][0][1], view_dict['bounds'][0][0])
        self.is_password = True if 'is_password' in view_dict and view_dict['is_password'] else False
        self.contained_items = None
        self.view_dict = view_dict

        self.widget_description = None
        self.possible_action_types = []
        self.possible_actions = []

        self.state_properties = []
        
        for state_property in ['focused', 'checked', 'selected']:
            if state_property in view_dict and view_dict[state_property]:
                self.state_properties.append(state_property)
                
        self.load_widget_description(text_description)
        self.signature = f'{self._class}-{self.stringify(include_modifiable_properties=False)}'

    def to_dict(self):
        description = {
            'ID': self.view_id,
            'widget_type': self._class,
        }

        if self.widget_description is not None:
            if 'text' in self.widget_description:
                description['text'] = self.widget_description['text']
            if 'adjacent_text' in self.widget_description:
                description['adjacent_text'] = self.widget_description['adjacent_text']
            if 'content_description' in self.widget_description:
                description['content_description'] = self.widget_description['content_description']
            if 'resource_id' in self.widget_description:
                description['resource_id'] = self.widget_description['resource_id']
                
            # description['description'] = self.widget_description
        
        if self.is_password:
            description['is_password'] = True

        if self.contained_items is not None:
            description['contained_items'] = self.contained_items

        if len(self.state_properties) > 0:
            description['state'] = self.state_properties

        if len(self.possible_action_types) > 0:
            description['possible_action_types'] = self.possible_action_types

        return description

    def register_possible_actions(self, action_type):
        possible_actions = initialize_possible_actions(action_type, self)
        if action_type not in self.possible_action_types:
            self.possible_action_types.append(action_type)
        self.possible_actions.extend(possible_actions)
        return possible_actions

    def load_widget_description(self, text_description):
        content_description = []
        text = []
        adjacent_text = []
        resource_id = []

        if 'content_description' in text_description:
            content_description = text_description['content_description']
        if 'text' in text_description:
            text = text_description['text']
        if 'resource_id' in text_description:
            resource_id = text_description['resource_id']
            resource_id = [rid.split('/')[-1] for rid in resource_id]
        if 'contained_items' in text_description:
            self.contained_items = text_description['contained_items']

        if 'parent' in text_description:
            parent_desc = text_description['parent']
            if len(text) == 0 and 'text' in parent_desc:
                adjacent_text.extend(parent_desc['text'])
            # if content_description is None and 'content_description' in parent_desc:
            #     content_description = parent_desc['content_description']
            # if resource_id is None and 'resource_id' in parent_desc:
            #     resource_id = parent_desc['resource_id']

        if 'siblings' in text_description:
            siblings_desc = text_description['siblings']
            if 'text' in siblings_desc:
                adjacent_text.extend(siblings_desc['text'])
            # if content_description is None and 'content_description' in siblings_desc:
            #     content_description = siblings_desc['content_description']
            # if resource_id is None and 'resource_id' in siblings_desc:
            #     resource_id = siblings_desc['resource_id']

        if len(text) > 0 or len(adjacent_text) > 0 or len(content_description) > 0 or len(resource_id) > 0:
            self.widget_description = {}

        if len(text) > 0:
            if len(text) == 1:
                text = text[0]
            elif len(text) > 5:
                text = text[:5] + ['...']
            self.widget_description['text'] = text

        if len(adjacent_text) > 0:
            if len(adjacent_text) == 1:
                adjacent_text = adjacent_text[0]
            elif len(adjacent_text) > 5:
                adjacent_text = adjacent_text[:5] + ['...']
            self.widget_description['adjacent_text'] = adjacent_text

        if len(content_description) > 0:
            if len(content_description) == 1:
                content_description = content_description[0]
            elif len(content_description) > 5:
                content_description = content_description[:5] + ['...']
            self.widget_description['content_description'] = content_description

        if len(resource_id) > 0:
            if len(resource_id) == 1:
                resource_id = resource_id[0]
            elif len(resource_id) > 5:
                resource_id = resource_id[:5] + ['...']
            self.widget_description['resource_id'] = resource_id

    def __repr__(self):
        """
        From a given widget, creates a (detailed) description of the widget including its type, resource ID, text, and content description, and possible action types
        {
            ID: 1,
            widget_type: "TextView",
            description: {
                text: "hello world",
                content_description: "hello world",
                resource_id: "com.example.app:id/hello_world",
            }
            possible_action_types: "touch, scroll, set_text"
        }
        """
        description = self.to_dict()
        
        return json.dumps(description, indent=2, ensure_ascii=False)

    def __str__(self):
        return self.stringify()

    def stringify(self, include_modifiable_properties=True):
        """
        natural language description of the widget
        """
        # maybe we can use LLM to summarise the widget info as well? 
        widget_type = self._class

        if len(self.state_properties) > 0 and include_modifiable_properties:
            state = ', '.join(self.state_properties)
            widget_type_repr = f'{state} '
        else:
            widget_type_repr = ''

        if self.is_password:
            widget_type_repr += 'password textfield'
        
        elif 'EditText' in widget_type:
            widget_type_repr += 'textfield'
        elif 'Button' in widget_type:
            widget_type_repr += 'button'
        elif 'CheckBox' in widget_type:
            widget_type_repr += 'checkbox'
        elif 'RadioButton' in widget_type:
            widget_type_repr += 'radio button'
        elif 'Spinner' in widget_type:
            widget_type_repr += 'dropdown field'
        elif widget_type.endswith('Tab'):
            widget_type_repr += 'tab'
        
        else:
            if 'touch' in self.possible_action_types:
                widget_type_repr += 'button'
            elif 'scroll' in self.possible_action_types:
                widget_type_repr += 'scrollable area'
            elif 'set_text' in self.possible_action_types:
                widget_type_repr += 'textfield'
            elif 'TextView' in widget_type:
                widget_type_repr += 'textview'
            elif 'ImageView' in widget_type:
                widget_type_repr += 'imageview'
            elif 'LinearLayout' in widget_type:
                widget_type_repr += 'linearlayout'
            elif 'RelativeLayout' in widget_type:
                widget_type_repr += 'relativelayout'
            elif 'FrameLayout' in widget_type:
                widget_type_repr += 'framelayout'
            elif 'GridLayout' in widget_type:
                widget_type_repr += 'gridlayout'
            elif 'RecyclerView' in widget_type:
                widget_type_repr += 'recyclerview'
            elif 'ListView' in widget_type:
                widget_type_repr += 'listview'
            else:
                widget_type_repr += 'widget'
        
        widget_type_repr = 'an ' + widget_type_repr if widget_type_repr[0] in ['a', 'e', 'i', 'o', 'u'] else 'a ' + widget_type_repr

        text = None
        content_description = None
        resource_id = None

        if self.widget_description is not None:
            text = self.widget_description.get('text', None)
            content_description = self.widget_description.get('content_description', None)
            resource_id = self.widget_description.get('resource_id', None)

        text_desc = []
        include_text_property = False
        if 'set_text' not in self.possible_action_types:
            include_text_property = True
        if include_modifiable_properties:
            include_text_property = True
        if text is not None and include_text_property:
            if isinstance(text, list):
                text = [f'"{t}"' for t in text]
                if text[-1] == '"..."':
                    text[-1] = '...'
                text_desc.append(f'texts {", ".join(text)}')
            else:
                text_desc.append(f'text "{text}"')
        if self.contained_items is not None and include_modifiable_properties:
            contained_items = [f'"{i}"' for i in self.contained_items]
            text_desc.append(f'contained items such as {", ".join(contained_items)}')

        if content_description is not None:
            if isinstance(content_description, list):
                content_description = [f'"{t}"' for t in content_description]
                if content_description[-1] == '"..."':
                    content_description[-1] = '...'
                text_desc.append(f'content_descs {", ".join(content_description)}')
            else:
                text_desc.append(f'content_desc "{content_description}"')
        if resource_id is not None:
            if isinstance(resource_id, list):
                resource_id = [f'"{t}"' for t in resource_id]
                if resource_id[-1] == '"..."':
                    resource_id[-1] = '...'
                text_desc.append(f'resource_ids {", ".join(resource_id)}')
            else:
                text_desc.append(f'resource_id "{resource_id}"')

        if len(text_desc) > 0:
            text_desc = ' and '.join(text_desc)
            return f'{widget_type_repr} that has {text_desc}'
        
        return widget_type_repr


def get_visible_widgets(view_list):
    visible_widgets = {}
    for view_id, view_dict in enumerate(view_list):
        if view_dict['visible']:
            visible_widgets[view_id] = view_dict
    return visible_widgets

def get_all_parent_ids(view_dict, visible_widgets):
    parent_ids = []
    cur_view_dict = view_dict
    while 'parent' in cur_view_dict and cur_view_dict['parent'] > 0:
        parent_ids.append(cur_view_dict['parent'])
        if cur_view_dict['parent'] not in visible_widgets:
            break
        cur_view_dict = visible_widgets[cur_view_dict['parent']]
    return parent_ids

def get_interactable_widgets(visible_widgets):
    interactable_widgets = defaultdict(list)
    touch_exclude_view_ids = []
    # Exclude parents of clickable widgets from being interactable

    for view_id, view_dict in visible_widgets.items():
        if 'enabled' not in view_dict:
            continue
        if 'enabled' in view_dict and not view_dict['enabled']:
            continue
        if view_dict['clickable'] or view_dict['checkable']:
            touch_exclude_view_ids.extend(get_all_parent_ids(view_dict, visible_widgets))

    touch_exclude_view_ids = set(touch_exclude_view_ids)

    for view_id, view_dict in visible_widgets.items():
        if 'enabled' in view_dict and not view_dict['enabled']:
            continue
        if view_dict['clickable'] or view_dict['checkable']:
            if not view_id in touch_exclude_view_ids:
                interactable_widgets[view_id].append('touch')
        if view_dict['long_clickable']:
            interactable_widgets[view_id].append('long_touch')
        if view_dict['scrollable']:
            interactable_widgets[view_id].append('scroll')
        if view_dict['editable']:
            if view_dict['class'].endswith('Spinner'):
               pass
            else:
                interactable_widgets[view_id].append('set_text')

    return interactable_widgets


def get_description(view_dict, visible_widgets, consider_children=True, consider_resource_id=True):
    description = defaultdict(list)

    text_content = None
    if 'text' in view_dict and view_dict['text'] is not None:
        text_content = view_dict['text'][:50] + '[...]' if len(view_dict['text']) > 50 else view_dict['text']
        text_content = text_content.replace('\n', '<newline>').replace('\r', ' ').replace('\t', ' ')

    if consider_resource_id and 'resource_id' in view_dict and view_dict['resource_id'] is not None:
        description['resource_id'].append(view_dict['resource_id'])
    if 'text' in view_dict and text_content is not None and len(text_content.strip()) > 0:
        description['text'].append(text_content)
    if 'content_description' in view_dict and view_dict['content_description'] is not None:
        description['content_description'].append(view_dict['content_description'])

    if has_sufficient_description(view_dict, description):
        return description

    if consider_children:
        for child in view_dict['children']:
            if child not in visible_widgets:
                continue
            child_desc = get_description(visible_widgets[child], visible_widgets) 
            # if consider_resource_id and 'resource_id' in child_desc and child_desc['resource_id'] is not None:
            #     description['resource_id'].extend(child_desc['resource_id'])
            if 'text' in child_desc and child_desc['text'] is not None and len(child_desc['text']) > 0:
                description['text'].extend(child_desc['text'])
            if 'content_description' in child_desc and child_desc['content_description'] is not None:
                description['content_description'].extend(child_desc['content_description'])

    return description

def get_all_children_ids(view_dict, visible_widgets):
    children_ids = set()
    if 'children' in view_dict:
        children_ids = children_ids.union(view_dict['children'])
    for child in view_dict['children']:
        if child not in visible_widgets:
            continue
        children_ids = children_ids.union(get_all_children_ids(visible_widgets[child], visible_widgets))
    return children_ids

def has_sufficient_description(view_dict, description):
    if 'ImageButton' in view_dict['class'] or 'ImageView' in view_dict['class']:
        if 'content_description' in description or 'resource_id' in description:
            return True

    if 'text' in description or 'content_description' in description:
        return True
    if 'parent' in description and 'text' in description['parent']:
        return True
    if 'parent' in description and 'content_description' in description['parent']:
        return True
    if 'siblings' in description and 'text' in description['siblings']:
        return True
    if 'siblings' in description and 'content_description' in description['siblings']:
        return True
    
    return False

def get_description_w_context(view_dict, visible_widgets):
    description = get_description(view_dict, visible_widgets)
    visited_ids = {view_dict['temp_id']}
    if 'children' in view_dict:
        visited_ids = visited_ids.union(get_all_children_ids(view_dict, visible_widgets))
    
    if 'is_password' in view_dict and view_dict['is_password']:
        description['is_password'] = True
    if has_sufficient_description(view_dict, description):
        return description, visited_ids
    
    # get parent/sibling descriptions instead
    cur_view_dict = visible_widgets[view_dict['parent']]
    while 'parent' in cur_view_dict and cur_view_dict['parent'] > 0:
        if cur_view_dict['temp_id'] in visited_ids:
            break
        parent_desc = get_description(cur_view_dict, visible_widgets, consider_children=True)
        visited_ids.add(cur_view_dict['temp_id'])
        if has_sufficient_description(view_dict, parent_desc):
            description['parent'] = parent_desc
            break

        siblings_desc = defaultdict(list)
        for sibling in cur_view_dict['children']:
            if sibling == cur_view_dict['temp_id']:
                continue
            if sibling not in visible_widgets:
                continue
            desc = get_description(visible_widgets[sibling], visible_widgets, consider_children=True)
            visited_ids.add(sibling)
            if len(desc) > 0:
                # if 'resource_id' in desc:
                #     siblings_desc['resource_id'].extend(desc['resource_id'])
                if 'text' in desc and len(desc['text']) > 0:
                    siblings_desc['text'].extend(desc['text'])
                if 'content_description' in desc:
                    siblings_desc['content_description'].extend(desc['content_description'])
        if has_sufficient_description(view_dict, siblings_desc):
            description['siblings'] = siblings_desc
            break

        else:
            cur_view_dict = visible_widgets[cur_view_dict['parent']]
    
    return description, visited_ids


def __safe_dict_get(d, key, default=None):
    return d[key] if (key in d) else default


def __get_all_children(view_dict, views):
        """
        Get temp view ids of the given view's children
        :param view_dict: dict, an element of DeviceState.views
        :return: set of int, each int is a child node id
        """
        children = __safe_dict_get(view_dict, 'children')
        if not children:
            return set()
        children = set(children)
        for child in children:
            children_of_child = __get_all_children(views[child], views)
            children.union(children_of_child)
        return children