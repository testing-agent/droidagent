import os
import shlex
import time
import json
import argparse
import subprocess
import shutil

from datetime import datetime


SCRIPT_DIR = os.path.dirname(__file__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run DroidAgent')
    # accept multiple apps 
    parser.add_argument('app', nargs='+', help='app names')
    args = parser.parse_args()
    
    with open(os.path.join(SCRIPT_DIR, '../evaluation/package_name_map.json')) as f:
        package_name_map = json.load(f)

    for app_name in args.app:
        apk_path = os.path.join(SCRIPT_DIR, f'../apps/{app_name}.apk')
        package_name = package_name_map[app_name]
        
        print(f'Running DroidAgent on {app_name} ({package_name})')
        subprocess.run(shlex.split(f'./run_droidagent_w_coverage.sh {app_name} {apk_path} {package_name}'), check=True)
