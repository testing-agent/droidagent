from droidbot.utg import UTG
from droidbot.input_event import IntentEvent, KeyEvent

from utg import copy_utg_rendering_resources

import time
import json
from datetime import datetime
import os
import subprocess
import re

POST_EVENT_WAIT = 1
MAX_NUM_STEPS_OUTSIDE = 5
MAX_BACKTRACK = 10
MAX_RESTART = 5

num_steps_outside = 0

class ExternalAction:
    def __init__(self, description, events):
        self.description = description
        self.events = events

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description


class DeviceManager:
    """
    - Send to the GUI event to the device
    - Update UTG
    """
    def __init__(self, device, app, output_dir):
        self.device = device
        self.app = app
        self.last_event = None
        self.pre_event_state = None
        self.current_state = device.get_current_state() # might be loading state (need to be updated)

        self.views_dir = os.path.join(output_dir, 'views')
        self.events_dir = os.path.join(output_dir, 'events')
        os.makedirs(self.views_dir, exist_ok=True)
        os.makedirs(self.events_dir, exist_ok=True)

        # Initialize UTG
        self.utg = UTG(device, app, random_input=False)
        copy_utg_rendering_resources(output_dir)

    def fetch_device_state(self):
        self.current_state = self.device.get_current_state()

    def get_app_activity_depth(self):
        return self.current_state.get_app_activity_depth(self.app)

    def add_new_utg_edge(self):
        if self.last_event is None:
            return
        if self.pre_event_state is None:
            return
        self.utg.add_transition(self.last_event, self.pre_event_state, self.current_state)

    @staticmethod
    def parse_event_log(output):
        def extract_text(line):
            # Regular expression to find the content after "Text: "
            pattern = re.compile(r'Text: \[(.*?)\]')
            match = pattern.search(line)
            if match:
                return match.group(1)
            else:
                return None
        texts = set()
        for l in output.split('\n'):
            if 'TYPE_NOTIFICATION_STATE_CHANGED' in l and 'ClassName: android.widget.Toast' in l:
                text = extract_text(l)
                if text:
                    texts.add(text)

        return texts

    def send_event_to_device(self, event, capture_intermediate_state=False, agent=None):
        if capture_intermediate_state:
            assert agent is not None, 'Agent should be provided when capture_intermediate_state is True'

        args = [] + self.device.adb.cmd_prefix + ['shell', 'uiautomator', 'events']
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if event is None:   # "wait" event
            capture_intermediate_state = False
        else:
            self.device.send_event(event)

            self.last_event = event
            self.pre_event_state = self.current_state

        if capture_intermediate_state:
            agent.capture_temporary_message(self.device.get_current_state())

        process.terminate()
        stdout, stderr = process.communicate()

        time.sleep(POST_EVENT_WAIT)

        if capture_intermediate_state:
            toast_messages = self.parse_event_log(stdout.decode('utf-8'))
            agent.capture_toast_message(toast_messages)
        
        self.fetch_device_state()
        
        view_image_dir = None

        if event is not None:
            views = event.get_views()
            if views:
                for view_dict in views:
                    if self.pre_event_state is not None:
                        self.pre_event_state.save_view_img(view_dict=view_dict, output_dir=self.views_dir)
                        view_image_dir = view_file_path = "%s/view_%s.png" % (self.views_dir, view_dict['view_str'])
        
            self.utg.add_transition(event, self.pre_event_state, self.current_state)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        event_dict = {
            'tag': timestamp,
            'event': event.to_dict() if event is not None else "wait",
            'start_state': self.pre_event_state.state_str if self.pre_event_state is not None else None,
            'stop_state': self.current_state.state_str if self.current_state is not None else None,
            'event_str': event.get_event_str(self.pre_event_state) if event is not None else "wait",
            'task': agent.memory.task if agent is not None else None,
            'view_image_dir': view_image_dir
        }
        with open(os.path.join(self.events_dir, f'event_{timestamp}.json'), 'w') as f:
            json.dump(event_dict, f, indent=2)

        return event_dict
        

def recover_activity_stack(device_manager, agent, events=[]):
    global num_steps_outside

    if device_manager.get_app_activity_depth() == 0:
        num_steps_outside = 0
        return
    
    # App is not in the activity stack (e.g., mistakenly closed the app)
    if device_manager.get_app_activity_depth() < 0 or 'leakcanary.internal.activity' in device_manager.current_state.foreground_activity: 
        start_app_intent = device_manager.app.get_start_intent()
        reopen_event = IntentEvent(intent=start_app_intent)

        event_dict = device_manager.send_event_to_device(reopen_event)
        events.append(event_dict)

        if device_manager.get_app_activity_depth() == 0:
            agent.memory.append_to_working_memory(ExternalAction(f'Open the app again because the previous action led to closing the app', events), 'ACTION')
            agent.clear_temporary_message()
            num_steps_outside = 0
            return

    # App is not in the foreground (e.g., file manager app, permission setting screen)
    elif device_manager.get_app_activity_depth() > 0:
        num_steps_outside += 1
        if num_steps_outside <= MAX_NUM_STEPS_OUTSIDE:
            agent.clear_temporary_message()
            return 

        back_button_times = 0
        for _ in range(MAX_BACKTRACK):
            if device_manager.get_app_activity_depth() == 0:
                break
            
            go_back_event = KeyEvent(name='BACK')
            event_dict = device_manager.send_event_to_device(go_back_event)
            events.append(event_dict)

            back_button_times += 1

        if device_manager.get_app_activity_depth() == 0:
            if back_button_times > 1:
                agent.memory.append_to_working_memory(ExternalAction(f'Press the back button {back_button_times} times because you stayed on the pages not belonging to the target app for too long', events), 'ACTION')
            else:
                agent.memory.append_to_working_memory(ExternalAction(f'Press the back button because you stayed on the pages not belonging to the target app for too long', events), 'ACTION')
            
            agent.clear_temporary_message()
            num_steps_outside = 0
            return

    # Try reopen
    start_app_intent = device_manager.app.get_start_intent()
    reopen_event = IntentEvent(intent=start_app_intent)
    event_dict = device_manager.send_event_to_device(reopen_event)
    events.append(event_dict)

    if device_manager.get_app_activity_depth() == 0:
        agent.memory.append_to_working_memory(ExternalAction(f'Open the app again because you stayed on the pages not belonging to the target app for too long', events), 'ACTION')
        agent.clear_temporary_message()
        num_steps_outside = 0
        return

    
    # Try backtrack and reopen
    back_button_times = 0
    for _ in range(MAX_BACKTRACK):
        if device_manager.get_app_activity_depth() == 0:
            break
        
        go_back_event = KeyEvent(name='BACK')
        event_dict = device_manager.send_event_to_device(go_back_event)
        events.append(event_dict)

        back_button_times += 1

    start_app_intent = device_manager.app.get_start_intent()
    reopen_event = IntentEvent(intent=start_app_intent)
    event_dict = device_manager.send_event_to_device(reopen_event)
    events.append(event_dict)

    if device_manager.get_app_activity_depth() == 0:
        agent.memory.append_to_working_memory(ExternalAction(f'Open the app again because you stayed on the pages not belonging to the target app for too long', events), 'ACTION')
        agent.clear_temporary_message()
        num_steps_outside = 0
        return
    
    # If the app is still not in the foreground, restart the app
    if device_manager.get_app_activity_depth() != 0:
        for _ in range(MAX_RESTART):
            if device_manager.get_app_activity_depth() == 0:
                break
        
            stop_app_intent = device_manager.app.get_stop_intent()
            stop_event = IntentEvent(intent=stop_app_intent)
            event_dict = device_manager.send_event_to_device(stop_event)
            events.append(event_dict)
            
            start_app_intent = device_manager.app.get_start_intent()
            restart_event = IntentEvent(intent=start_app_intent)
            event_dict = device_manager.send_event_to_device(restart_event)
            events.append(event_dict)

        if device_manager.get_app_activity_depth() == 0:
            agent.memory.append_to_working_memory(ExternalAction(f'Restart the app because you stayed on the pages not belonging to the target app for too long', events), 'ACTION')
            agent.clear_temporary_message()
            num_steps_outside = 0
            return

    # Fail-safe: just infinitely try again until the app goes back to the foreground
    recover_activity_stack(device_manager, agent, events)
    return