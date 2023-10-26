import sys
import os
import time
import json
import glob
import shutil
import argparse

import pandas as pd
from datetime import datetime

def get_screenshot_by_timestamp(timestamp, screenshot_with_timestamp):
    prev_screenshot = None 
    next_screenshot = None

    screenshot_with_timestamp = sorted(screenshot_with_timestamp, key=lambda x: x[1])

    for screenshot, screenshot_timestamp in screenshot_with_timestamp:
        if screenshot_timestamp <= timestamp:
            prev_screenshot = screenshot
        elif screenshot_timestamp > timestamp:
            next_screenshot = screenshot
            break

    prev_screenshot='file://' + str(os.path.abspath(str(prev_screenshot)))
    next_screenshot='file://' + str(os.path.abspath(str(next_screenshot)))
    
    return prev_screenshot, next_screenshot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make report from experiment data')
    parser.add_argument('--project', type=str, help='Project name')
    parser.add_argument('--result_dir', type=str, default=None, help='Result directory')
    args = parser.parse_args()

    target_project = args.project

    if args.result_dir is not None:
        result_path = args.result_dir
    else:
        result_path = os.path.join('..', 'evaluation', 'data', target_project)

    state_str_to_screenshot_path = {}
    for state_file in glob.glob(os.path.join(result_path, 'states', '*.json')):
        with open(state_file, 'r') as f:
            state_data = json.load(f)
            state_str = state_data['state_str']
            screenshot_path = 'file://' + str(os.path.abspath(os.path.join(result_path, 'states', f'screen_{state_data["tag"]}.png')))
            state_str_to_screenshot_path[state_str] = screenshot_path

    example_exp_data_file = os.path.join(result_path, 'exp_data.json')

    with open(example_exp_data_file, 'r') as f:
        exp_data = json.load(f)

    tasks = list(exp_data['task_results'].keys())

    rows = []

    screenshot_path = os.path.join(result_path, 'states')
    screenshots = glob.glob(os.path.join(screenshot_path, '*.png'))
    screenshot_with_timestamp = []

    for screenshot in screenshots:
        screenshot_file_name = os.path.basename(screenshot).split('.')[0].removeprefix('screen_')
        timestamp_from_filename = datetime.strptime(screenshot_file_name, '%Y-%m-%d_%H%M%S') 

        screenshot_with_timestamp.append((screenshot, timestamp_from_filename))

    start_timestamp = min(screenshot_with_timestamp, key=lambda x: x[1])[1]
    end_timestamp = max(screenshot_with_timestamp, key=lambda x: x[1])[1]

    # remove time, only date from the timestamp
    start_date = start_timestamp.strftime('%Y-%m-%d')
    end_date = end_timestamp.strftime('%Y-%m-%d')

    has_date_changed = start_date != end_date

    if os.path.exists(f'../reports/{target_project}/'):
        shutil.rmtree(f'../reports/{target_project}/')
    os.makedirs(f'../reports/{target_project}/')

    for i, task in enumerate(tasks):
        markdown_content = f'# {task}'
        task_data = exp_data['task_results'][task]

        task_result = task_data['result']
        task_summary = task_data['summary']
        result_color = 'green' if task_result == 'SUCCESS' else 'red'
        markdown_content += f'\n\n* Task Result: **<span style="color:{result_color}">{task_result}</span>**'
        markdown_content += f'\n\n* Task Summary: {task_summary}\n\n'
        history = task_data['task_execution_history']

        midnight_past = False
        
        action_count = 0

        for entry in history:
            if entry['type'] == 'ACTION':
                if 'events' in entry and len(entry['events']) > 0:
                    event_to_show = entry['events'][-1]
                    prev_screenshot = state_str_to_screenshot_path[event_to_show['start_state']]
                    next_screenshot = state_str_to_screenshot_path[event_to_show['stop_state']]
                
                else:
                    # add date to the timestamp (I did not record the date in the timestamp, which is a silly mistake)
                    if has_date_changed and entry['timestamp'].startswith('00:'):
                        action_timestamp = datetime.strptime(f'{end_date}_{entry["timestamp"]}', '%Y-%m-%d_%H:%M:%S')
                        midnight_past = True
                    elif has_date_changed and midnight_past:
                        action_timestamp = datetime.strptime(f'{end_date}_{entry["timestamp"]}', '%Y-%m-%d_%H:%M:%S')
                    else:
                        action_timestamp = datetime.strptime(f'{start_date}_{entry["timestamp"]}', '%Y-%m-%d_%H:%M:%S')

                    prev_screenshot, next_screenshot = get_screenshot_by_timestamp(action_timestamp, screenshot_with_timestamp)

                markdown_content += f'## Action {action_count+1}\n\n'
                markdown_content += f'* Action: {entry["description"]}'
                markdown_content += f'''
```json
{entry["action_data"]}
```
'''
                markdown_content += f'### State Change\n\n<img src="{prev_screenshot}" alt="prev_screenshot" width="200"/> ➡️ <img src="{next_screenshot}" alt="next_screenshot" width="200"/>\n\n'
                action_count += 1
                
            
            elif entry['type'] == 'OBSERVATION':
                markdown_content += f'* <span style="color:blue">Observation: {entry["description"]}</span>\n\n'
            elif entry['type'] == 'CRITIQUE':
                markdown_content += f'* <span style="color:red">Critique: {entry["description"]}</span>\n\n'


        with open(os.path.join('../reports', target_project, f'task_{i+1}.md'), 'w') as f:
            f.write(markdown_content)
