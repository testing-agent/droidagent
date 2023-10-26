from ..config import agent_config
from ..model import get_next_assistant_message, zip_messages
from ..functions.possible_actions import *
from ..utils import *

import json

QUERY_COUNT = 3


def initialize_possible_actions(memory):
    possible_action_functions = {}
    function_map = {}
    current_context.set_widgets(memory.current_gui_state.actiontype2widgets)
    function_creators = [create_touch_action_definition, create_set_text_self_contained_action_definition, create_scroll_action_definition, create_long_touch_action_definition]

    for function_creator in function_creators:
        function_def, func = function_creator()
        possible_action_functions[function_def['name']] = function_def
        function_map[function_def['name']] = func

    return possible_action_functions, function_map


def prompt_first_action(memory, full_prompt):
    possible_action_functions, function_map = initialize_possible_actions(memory)

    full_prompt['system_message'] = f'''
You are a smart GUI testing assistant for an Android mobile application. The user want to test {agent_config.app_name} app. It has the following pages, including {", ".join(agent_config.app_activities)}. When a user requests, select an action by calling one of the given functions that corresponds to a GUI action.
    '''.strip()

    full_prompt['user_messages'].append(f'''
What GUI action is required? Select one action that is the most effective to test the app.

Current page:
```json
{memory.current_gui_state.describe_screen()}
```

Following types of actions can be performed:

- Scroll on a scrollable widget
- Touch on a clickable widget
- Long touch on a long-clickable widget
- Fill in an editable widget
- Navigate back by pressing the back button
    '''.strip())

    full_prompt['assistant_messages'].append(get_next_assistant_message(full_prompt['system_message'], full_prompt['user_messages'], full_prompt['assistant_messages'], model="gpt-3.5-turbo-16k-0613", functions=list(possible_action_functions.values())))
    response = full_prompt['assistant_messages'][-1]

    if not isinstance(response, dict): # retry if model doesn't do function call
        error_message = f'You need to call a function to select the next action.'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    if response['name'] not in function_map:
        error_message = f'You need to call one of the given functions to select the next GUI action.'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    function_to_call = function_map[response['name']]
    function_params = []
    for param_name in possible_action_functions[response['name']]['parameters']['properties']:
        function_params.append(param_name)

    try:
        function_args = json.loads(response['arguments'])
    except json.decoder.JSONDecodeError:
        error_message = f'You did not provide the required parameters for the function call. Please provide the following parameters: {function_params}'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    processed_function_args = {}
    error_message = None
    for param_name in function_params:
        arg_value = function_args.get(param_name)
        if arg_value is None:
            error_message = f'You did not provide the required parameter "{param_name}".'
            break
        if param_name == 'target_widget_id':
            try:
                arg_value = int(arg_value)
            except ValueError:
                error_message = f'The value of the parameter "{param_name}" should be an integer.'
                break
        processed_function_args[param_name] = arg_value

    if error_message is not None: # retry if model doesn't make correct arguments
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    action, error_message = function_to_call(**processed_function_args)

    if error_message is not None: # retry if target widget ID is not valid
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    return action


def prompt_next_action(memory, error_message=None, full_prompt=None, contain_feedback=True):
    possible_action_functions, function_map = initialize_possible_actions(memory)

    if error_message is None:
        if contain_feedback:
            action_function_query = 'Good. we successfully did the above action. '
        else:
            action_function_query = ''
        action_function_query += f'''
What GUI action is required next? Select one action that is the most effective to test the app.

We have tested following pages with the visit count: {remove_quotes(json.dumps(memory.visited_activities))}

Current page:
```json
{memory.current_gui_state.describe_screen_w_memory(memory, include_widget_knowledge=False)}
```
Note that `num_prev_actions` for each widget means the number of times the widget was tested.

Following types of actions can be performed:

- Scroll on a scrollable widget
- Touch on a clickable widget
- Long touch on a long-clickable widget
- Fill in an editable widget
- Navigate back by pressing the back button
    '''.strip()

        full_prompt['user_messages'].append(action_function_query)

    else:
        full_prompt['user_messages'].append(error_message)

    full_prompt['assistant_messages'].append(get_next_assistant_message(full_prompt['system_message'], full_prompt['user_messages'], full_prompt['assistant_messages'], model="gpt-3.5-turbo-16k-0613", functions=list(possible_action_functions.values())))
    response = full_prompt['assistant_messages'][-1]

    if not isinstance(response, dict): # retry if model doesn't do function call
        error_message = f'You need to call a function to select the next action.'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    if response['name'] not in function_map:
        error_message = f'You need to call one of the given functions to select the next GUI action.'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    function_to_call = function_map[response['name']]
    function_params = []
    for param_name in possible_action_functions[response['name']]['parameters']['properties']:
        function_params.append(param_name)

    try:
        function_args = json.loads(response['arguments'])
    except json.decoder.JSONDecodeError:
        error_message = f'You did not provide the required parameters for the function call. Please provide the following parameters: {function_params}'
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    processed_function_args = {}
    error_message = None
    for param_name in function_params:
        arg_value = function_args.get(param_name)
        if arg_value is None:
            error_message = f'You did not provide the required parameter "{param_name}".'
            break
        if param_name == 'target_widget_id':
            try:
                arg_value = int(arg_value)
            except ValueError:
                error_message = f'The value of the parameter "{param_name}" should be an integer.'
                break
        processed_function_args[param_name] = arg_value

    if error_message is not None: # retry if model doesn't make correct arguments
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    action, error_message = function_to_call(**processed_function_args)

    if error_message is not None: # retry if target widget ID is not valid
        return prompt_next_action(memory, error_message=error_message, full_prompt=full_prompt)

    return action
