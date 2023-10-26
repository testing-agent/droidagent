import time
import os
import shutil
import json
import argparse
import subprocess
import shlex

from timeout_decorator import timeout

from droidbot.device import Device
from droidbot.app import App
from droidbot.input_event import IntentEvent, KeyEvent

from droidagent import TaskBasedAgent

from device_manager import DeviceManager, recover_activity_stack, ExternalAction
from collections import defaultdict, OrderedDict
from targets import initial_knowledge_map


SCRIPT_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(SCRIPT_DIR, '..', 'resources/personas')

POST_EVENT_WAIT = 1
MAX_STEP = 8000


def load_profile(profile_id):
    if not os.path.exists(os.path.join(PROFILE_DIR, f'{profile_id}.txt')):
        raise FileNotFoundError(f'Profile {profile_id} does not exist')

    with open(os.path.join(PROFILE_DIR, f'{profile_id}.txt'), 'r') as f:
        profile_content = f.read().strip()
    
    profile = OrderedDict()
    for l in profile_content.split('\n'):
        l = l.strip()
        if l.startswith('-'):
            l = l.removeprefix('-').strip()
            prop = l.split(':')[0].strip()
            val = l.split(':')[1].strip()
            profile[prop] = val
    
    return profile


@timeout(7200)
def main(device, app, persona, debug=False):
    start_time = time.time()
    agent = TaskBasedAgent(output_dir, app=app, persona=persona, debug_mode=debug)
    device_manager = DeviceManager(device, app, output_dir=output_dir)
    agent.set_current_gui_state(device_manager.current_state)
    is_loading_state = False
    need_state_update = False

    max_loading_wait = 3
    loading_wait_count = 0

    while True:
        if agent.step_count > MAX_STEP:
            print(f'Maximum number of steps reached ({agent.step_count})')
            device.uninstall_app(app)
            device.disconnect()
            device.tear_down()
            exit(0)

        if agent.step_count % 10 == 0:
            print(f'Time left: {round(((7200 - (time.time() - start_time)) / 60), 2)} min')

        if agent.is_loading_state(device_manager.current_state):
            loading_wait_count += 1

            if loading_wait_count > max_loading_wait:
                print('Loading state persisted for too long. Pressing the back button to go back to the previous state...')
                go_back_event = KeyEvent(name='BACK')
                event_dict = device_manager.send_event_to_device(go_back_event)
                agent.memory.append_to_working_memory(ExternalAction(f'{agent.persona_name} pressed the back button because there was no interactable widgets', [event_dict]), 'ACTION')
                loading_wait_count = 0
                continue
                
            else:
                print('Loading state detected. Waiting for the app to be ready...')
                time.sleep(POST_EVENT_WAIT)
                device_manager.fetch_device_state()
                need_state_update = True
                continue

        if need_state_update:   
            # seems that the loading is done and need to update the state captured right after the action to the recent state
            agent.set_current_gui_state(device_manager.current_state)
            device_manager.add_new_utg_edge()
            need_state_update = False
        
        action = agent.step()
        agent.save_memory_snapshot()
        
        if action is not None:
            event_records = []
            events = action.to_droidbot_event()
            for event in events:
                event_dict = device_manager.send_event_to_device(event, capture_intermediate_state=True, agent=agent)
                event_records.append(event_dict)
            
            action.add_event_records(event_records)

            recover_activity_stack(device_manager, agent)
            agent.set_current_gui_state(device_manager.current_state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a task-based exploration')
    parser.add_argument('--app', type=str, help='name of the app to be tested', default='AnkiDroid')
    parser.add_argument('--output_dir', type=str, help='path to the output directory', default=None)
    parser.add_argument('--profile_id', type=str, help='name of the persona profile to be used', default='jade')
    parser.add_argument('--is_emulator', action='store_true', help='whether the device is an emulator or not', default=False)
    parser.add_argument('--debug', action='store_true', help='whether to run the agent in the debug mode or not', default=False)
    args = parser.parse_args()
    
    timestamp = time.strftime("%Y%m%d%H%M%S")

    if args.debug:
        output_dir = os.path.join(SCRIPT_DIR, f'../evaluation/data_new/{args.app}/agent_run_debug_{args.profile_id}')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
    elif args.output_dir is None:
        output_dir = os.path.join(SCRIPT_DIR, f'../evaluation/data_new/{args.app}/agent_run_{args.profile_id}_{timestamp}')
    else:
        output_dir = args.output_dir

    device = Device(device_serial='emulator-5554', output_dir=output_dir, grant_perm=True, is_emulator=args.is_emulator)
    device.set_up()
    device.connect()

    app_path = os.path.join(SCRIPT_DIR, '../target_apps/' + args.app + '.apk')
    app = App(app_path, output_dir=output_dir)
    app_name = app.apk.get_app_name()

    persona = OrderedDict()
    persona.update(load_profile(args.profile_id))
    assert 'name' in persona, f'The persona profile {args.profile_id} does not have a name'
    persona_name = persona['name']

    persona.update({
        'ultimate_goal': 'visit as many pages as possible while trying their core functionalities',
        # 'ultimate_goal': 'check whether the app supports interactions between multiple users', # for QuickChat case study
        'initial_knowledge': initial_knowledge_map(args.app, persona_name, app_name),
    })

    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/exp_info.json', 'w') as f:
        json.dump({
            'app_name': app_name,
            'app_path': os.path.abspath(app_path),
            'device_serial': device.serial,
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }, f, indent=4)
    
    device.install_app(app)
    device.start_app(app)

    print('Waiting 10 secs for the app to be ready...')
    print('Output directory:', os.path.abspath(output_dir))
    time.sleep(10)
    
    try:
        main(device, app, persona, debug=args.debug)
    except (KeyboardInterrupt, TimeoutError) as e:
        print("Ending the exploration due to a user request or timeout.")
        print(e)
        device.uninstall_app(app)
        device.disconnect()
        device.tear_down()
        exit(0)

    except Exception as e:
        print("Ending the exploration due to an unexpected error.")
        print(e)
        device.uninstall_app(app)
        device.disconnect()
        device.tear_down()

        raise e
    
    device.uninstall_app(app)
    device.disconnect()
    device.tear_down()