
setup_scripts = {
    'commons': '../benchmark/Themis/commons/login-2.11.0-#3244.py',
    'collect': './setup_script/collect_start_demo.py',
    'MaterialFB': './setup_script/materialFB.py',
    'infinity-for-reddit': './setup_script/reddit.py',
}

def get_initial_knowledge(app_id, persona_name, app_name):
    _initial_knowledge_map = {
        'AnkiDroid': [f'{persona_name} owns an existing account on AnkiWeb', f'{persona_name} started the {app_name} app'],
        'ActivityDiary': [f'{persona_name} started the {app_name} app'],
        'collect': [f'{persona_name} want to use the demo version of the app', f'{persona_name} started the {app_name} app'],
        'commons': [f'{persona_name} owns an existing account on Wikimedia Commons', f'{persona_name} started the {app_name} app'],
        'geohashdroid': [f'{persona_name} started the {app_name} app'],
        'Omni-Notes': [f'{persona_name} started the {app_name} app'],
        'openlauncher': [f'{persona_name} started the {app_name} app'],
        'osmeditor4android': [f'{persona_name} started the {app_name} app'],
        'Phonograph': [f'{persona_name} started the {app_name} app'],
        'Scarlet-Notes': [f'{persona_name} started the {app_name} app'],
        'AntennaPod': [f'{persona_name} started the {app_name} app'],
        'Markor': [f'{persona_name} started the {app_name} app'],

        'QuickChat': [f'{persona_name} started the {app_name} app', f'The app is in development phase and contains no user data yet. {persona_name} is a tester of the app and is trying to make multiple accounts simulating multiple users to test the app.'],
    }
    if app_id in _initial_knowledge_map:
        return _initial_knowledge_map[app_id]
    else:
        return [f'{persona_name} started the {app_name} app']


initial_knowledge_map = lambda app_id, persona_name, app_name: get_initial_knowledge(app_id, persona_name, app_name)
