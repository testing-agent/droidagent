import os
import json
from pathlib import Path
from functools import cached_property

from .utils import GUIStateManager

file_dir = os.path.dirname(os.path.realpath(__file__))

GPT_4 = 'gpt-4-0613'
GPT_3_5 = 'gpt-3.5-turbo-0613'
GPT_3_5_16k = 'gpt-3.5-turbo-16k-0613'

class Persona:
    def __init__(self, persona_dict):
        self.name = persona_dict['name']
        self.ultimate_goal = persona_dict['ultimate_goal']
        self.initial_knowledge = persona_dict['initial_knowledge']
        
        del persona_dict['ultimate_goal']
        del persona_dict['initial_knowledge']

        self.profile_dict = persona_dict
        
        profile_str = ''
        for k, v in self.profile_dict.items():
            profile_str += f'- {k}: {v}\n'

        self.profile = f'''
(The username and password is what {self.name} generally uses for their accounts.)
{profile_str.strip()}
'''.strip()

    def to_dict(self):
        return {
            'name': self.name,
            'ultimate_goal': self.ultimate_goal,
            'initial_knowledge': self.initial_knowledge,
            'profile': self.profile,
            'profile_dict': self.profile_dict
        }
    
    def from_dict(self, saved_dict):
        self.name = saved_dict['name']
        self.ultimate_goal = saved_dict['ultimate_goal']
        self.initial_knowledge = saved_dict['initial_knowledge']
        self.profile_dict = saved_dict['profile_dict']
        self.profile = saved_dict['profile']


class AgentConfig:
    # collection of "immutable" information of the agent
    def __init__(self):
        self.agent_output_dir = None

        # app info
        self.app_name = None
        self.package_name = None
        self.app_activities = None

        # persona info
        self.persona = None

        self.actor_model = GPT_3_5_16k
        self.observer_model = GPT_3_5_16k
        self.planner_model = GPT_4
        self.reflector_model = GPT_4
        self.knowledge_summary_model = GPT_3_5

    @cached_property
    def persona_name(self):
        if self.persona is None:
            return 'user X'
        
        return self.persona.name

    @cached_property
    def ultimate_goal(self):
        return self.persona.ultimate_goal

    @cached_property
    def persona_profile(self):
        return self.persona.profile

    @cached_property
    def persona_profile_dict(self):
        return self.persona.profile_dict

    def save(self):
        config_dict = {
            'agent_output_dir': str(self.agent_output_dir),
            'app_name': self.app_name,
            'package_name': self.package_name,
            'app_activities': self.app_activities,
            'actor_model': self.actor_model,
            'observer_model': self.observer_model,
            'planner_model': self.planner_model,
            'reflector_model': self.reflector_model,
            'activity_name_map': GUIStateManager.activity_name_restore_map
        }
        if self.persona is not None:
            config_dict['persona'] = self.persona.to_dict()

        with open(os.path.join(self.agent_output_dir, 'agent_config.json'), 'w') as f:
            json.dump(config_dict, f, indent=2)

    def load(self, saved_dict):
        self.agent_output_dir = Path(saved_dict['agent_output_dir'])
        self.app_name = saved_dict['app_name']
        self.package_name = saved_dict['package_name']
        self.app_activities = saved_dict['app_activities']
        self.actor_model = saved_dict['actor_model']
        self.observer_model = saved_dict['observer_model']
        self.planner_model = saved_dict['planner_model']
        self.reflector_model = saved_dict['reflector_model']
        self.persona = Persona(saved_dict['persona'])
    
    def set_debug_mode(self):
        self.actor_model = GPT_3_5_16k
        self.observer_model = GPT_3_5_16k
        self.planner_model = GPT_3_5_16k
        self.reflector_model = GPT_3_5_16k

    def set_app(self, app):
        self.app_name = app.apk.get_app_name()
        self.package_name = app.get_package_name()
        self.main_activity = GUIStateManager.fix_activity_name(app.get_main_activity().split('/')[-1])

        package_name_tokens = self.package_name.split('.')
        if len(package_name_tokens) > 2:
            package_name_prefix = '.'.join(package_name_tokens[:2])
        else:
            package_name_prefix = self.package_name

        if package_name_prefix not in app.get_main_activity():
            # use main activity as the prefix
            tokens = self.main_activity.split('/')[-1].split('.')
            if len(tokens) > 2:
                package_name_prefix = '.'.join(tokens[:2])
            else:
                package_name_prefix = ''
        
        app_activities = [GUIStateManager.fix_activity_name(a.split('/')[-1]) for a in app.activities if 'leakcanary' not in a and 'CrashReportDialog' not in a and package_name_prefix in a]
        self.app_activities = app_activities

    def set_output_dir(self, output_dir):
        output_dir = Path(os.path.abspath(output_dir))
        self.agent_output_dir = output_dir
        os.makedirs(self.agent_output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.agent_output_dir, 'prompts'), exist_ok=True)

    def set_persona(self, persona_dict):
        assert 'name' in persona_dict, 'Missing required properties of a persona: name'
        assert 'ultimate_goal' in persona_dict, 'Missing required properties of a persona: ultimate_goal'

        self.persona = Persona(persona_dict)

agent_config = AgentConfig()