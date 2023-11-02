import sys
import os
import time
import json
import glob
import shutil
import argparse

import pandas as pd
from datetime import datetime

def get_widget_identifier(action_data):
    text = None
    content_desc = None
    resource_id = None
    bounds = None

    selector_str = 'd('

    if action_data['target_widget_text'] is not None and len(action_data['target_widget_text']) > 0:
        text = action_data['target_widget_text'].removesuffix('[...]').split('"')[0].split('\n')[0]
        selector_str += f'textStartsWith="{text}"'

    if action_data['target_widget_content_description'] is not None and len(action_data['target_widget_content_description']) > 0:
        content_desc = action_data['target_widget_content_description']
        if selector_str != 'd(':
            selector_str += ', '
        selector_str += f'descriptionMatches=".*{content_desc}"'

    if action_data['target_widget_resource_id'] is not None and len(action_data['target_widget_resource_id']) > 0:
        resource_id = action_data['target_widget_resource_id']
        if selector_str != 'd(':
            selector_str += ', '
        selector_str += f'resourceIdMatches=".*{resource_id}"'

    if selector_str == 'd(' and action_data['target_widget_bounds'] is not None:
    # FIXME: position-based replay is very unstable (will not work with different screen size)
        bounds = action_data['target_widget_bounds']
        center_x = (bounds[0][0] + bounds[1][0]) // 2
        center_y = (bounds[0][1] + bounds[1][1]) // 2
        return None, (center_x, center_y)

    return selector_str + ')', None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make GUI testing scripts from experiment data')
    parser.add_argument('--result_dir', type=str, help='Result directory')
    parser.add_argument('--package_name', type=str, help='App package name (ex. org.odk.collect.android)')
    parser.add_argument('--project', type=str, help='Project name')
    args = parser.parse_args()

    result_path = args.result_dir
    target_project = args.project
    package_name = args.package_name

    state_str_to_screenshot_path = {}
    for state_file in glob.glob(os.path.join(result_path, 'states', '*.json')):
        with open(state_file, 'r') as f:
            state_data = json.load(f)
            state_str = state_data['state_str']
            screenshot_path = 'file://' + str(os.path.abspath(os.path.join(result_path, 'states', f'screen_{state_data["tag"]}.png')))
            state_str_to_screenshot_path[state_str] = screenshot_path

    exp_data_file = os.path.join(result_path, 'exp_data.json')

    with open(exp_data_file, 'r') as f:
        exp_data = json.load(f)

    task_results = list(exp_data['task_results'].items())

    if len(task_results) == 0:
        print('No task results...')
        exit(0)
    
    if os.path.exists(f'../gen_tests/{target_project}/'):
        shutil.rmtree(f'../gen_tests/{target_project}/')
    os.makedirs(f'../gen_tests/{target_project}/')

    state_files = sorted(glob.glob(os.path.join(result_path, 'states', '*.json')))
    with open(state_files[0]) as f:
        first_state = json.load(f)

    original_width = first_state['width']
    original_height = first_state['height']
    
    script_content = f'''
import sys
import time
import uiautomator2 as u2

def wait(seconds=3):
    for i in range(0, seconds):
        print("wait 1 second ..")
        time.sleep(1)

def wait_until_activity(d, activity_name, max_wait=30):
    for i in range(0, max_wait):
        current_app = d.app_current()
        if current_app['package'] == "{package_name}" and activity_name in current_app['activity']:
            break
        time.sleep(1)
    
    # if the target activity is not launched, raise exception
    current_app = d.app_current()
    if current_app['package'] != "{package_name}" or activity_name not in current_app['activity']:
        raise Exception(f"Action precondition cannot be satisfied: %s is not launched" % activity_name)

def go_back_until_inside_app(d, max_backtrack=10):
    for i in range(0, max_backtrack):
        current_app = d.app_current()
        if current_app['package'] == "{package_name}":
            break
        d.press("back")
    
    raise Exception(f"Backtrack failed: {package_name} is not launched")


avd_serial = sys.argv[1]
d = u2.connect(avd_serial)
assert d.device_info['display']['width'] == {original_width} and d.device_info['display']['height'] == {original_height}, "Screen size is different from the original screen size"

d.app_start("{package_name}")
wait()

'''

    for i, (task, task_result) in enumerate(task_results):
        script_content += f'''"""
{i+1}. {task}
"""
'''
        for entry in task_result['task_execution_history']:
            if entry['type'] == 'ACTION':
                script_content += f'''wait_until_activity(d, "{entry["page"]}")'''
                script_content += '\n'
                # case 1: user action
                if entry['action_data'] is not None:
                    selector_str, position = get_widget_identifier(entry['action_data'])
                        
                    if entry['action_data']['action_type'] == 'touch':
                        if selector_str is None:
                            script_content += f'''d.click({position[0]}, {position[1]})'''
                        else:
                            script_content += f'''{selector_str}.click()'''
                    elif entry['action_data']['action_type'] == 'long_touch':
                        if selector_str is None:
                            script_content += f'''d.long_click({position[0]}, {position[1]})'''
                        else:
                            script_content += f'''{selector_str}.long_click()'''
                    elif entry['action_data']['action_type'] == 'set_text':
                        if selector_str is None:
                            script_content += f'''d.click({position[0]}, {position[1]})'''
                            script_content += '\n'
                            script_content += f'''d.send_keys("{entry['action_data']['text']}")'''
                        else:
                            script_content += f'''{selector_str}.set_text("{entry['action_data']['text'].replace('"', '')}")'''
                    elif entry['action_data']['action_type'] == 'scroll':
                        if selector_str is None:
                            if entry['action_data']['direction'] == 'UP':
                                script_content += f'''d.swipe({position[0]}, {position[1]}, {position[0]}, {position[1] + 100})'''
                            elif entry['action_data']['direction'] == 'DOWN':
                                script_content += f'''d.swipe({position[0]}, {position[1]}, {position[0]}, {position[1] - 100})'''
                            elif entry['action_data']['direction'] == 'LEFT':
                                script_content += f'''d.swipe({position[0]}, {position[1]}, {position[0] + 100}, {position[1]})'''
                            elif entry['action_data']['direction'] == 'RIGHT':
                                script_content += f'''d.swipe({position[0]}, {position[1]}, {position[0] - 100}, {position[1]})'''
                        else:
                            script_content += f'''{selector_str}.swipe({entry['action_data']['direction'].lower()})'''
                    elif entry['action_data']['action_type'] == 'key':
                        if entry['action_data']['name'] == 'BACK':
                            script_content += f'''d.press("back")'''

                    # case 2: wait action (wait until activity is launched, etc.)
                    elif entry['action_data']['action_type'] == 'wait':
                        script_content += f'''wait()'''

                # case 3: recovery action (send open intent, press back multiple times, etc.)
                else:
                    if entry['description'].startswith('Open the app again'):
                        script_content += f'''d.app_start("{package_name}")'''
                    elif entry['description'].startswith('Press the back button'):
                        script_content += f'''go_back_until_inside_app(d)'''

                cleaned_description = entry['description'].replace('"', "'").replace('\n', ' ').encode('ascii', 'ignore').decode('ascii')
                script_content += f'\nprint("{cleaned_description}: SUCCESS")\nwait()\n'

            elif entry['type'] == 'OBSERVATION':
                script_content += f'''# Expected behaviour: {entry['description']}'''
                script_content += '\n\n'


    with open(os.path.join('../gen_tests', target_project, f'replay.py'), 'w') as f:
        f.write(script_content)