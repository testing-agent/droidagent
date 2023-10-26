import os
import shutil
import json

def copy_utg_rendering_resources(output_dir):
    if os.path.exists(os.path.join(output_dir, 'stylesheets')):
        shutil.rmtree(os.path.join(output_dir, 'stylesheets'))

    shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'resources/droidbot', 'index.html'), output_dir)
    shutil.copytree(os.path.join(os.path.dirname(__file__), '..', 'resources/droidbot', 'stylesheets'), os.path.join(output_dir, 'stylesheets'))