# DroidAgent: Intent-Driven Android GUI Testing with LLM Agents

Test with artificial user intents!

DroidAgent produces **high-level testing scenarios** with executable scripts (currently in the format of [uiautomator2](https://github.com/openatx/uiautomator2)) by autonomously exploring a given application under test (AUT). It is built as a modular framework driven by multiple LLM instances.

![droidagent_overview](resources/droidagent.jpg)

## Table of Contents
1. [Setup](#setup)
2. [Running DroidAgent](#run-droidagent)
3. [Replicate evaluation results](#replicate-evaluation-results)
4. [Troubleshooting](#troubleshooting)

## Setup

DroidAgent requires ADB (Android debugging bridge) and several Python libraries installed.

### Prerequisite
* \>=16GB RAM
* \>=Python 3.10
* Android SDK & ADB installed and configured
    1. Install [Android Studio](https://developer.android.com/studio)
    2. Install command line tools: `Android Studio > Tools > SDK Manager > SDK Tools > Android SDK Command-line Tools (latest)`
    3. Setup Environment Variables: [Check official document](https://developer.android.com/studio/command-line?hl=ko#environment-variables)
        ```bash
        export ANDROID_HOME="[YOUR_HOME_DIRECTORY]/Android/sdk"
        export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin"
        ```

* Android device connected or emulator running
* DroidAgent uses the slightly modified version of [DroidBot](https://github.com/testing-agent/droidbot) (included as submodule)
* OpenAI key: rename `.openai_api_key.example` to `.openai_api_key` and add your OpenAI API key


### Clone & Install Dependencies
```bash
$ git clone --recurse-submodule https://github.com/testing-agent/droidagent.git
$ cd droidbot
$ pip install -e . # install droidbot
$ cd ..
$ pip install -r requirements.txt
$ pip install -e . # install droidagent
```

## Run DroidAgent
* Make sure that your Android device is connected or emulator is running.
* Locate the APK file of the application under test (AUT) in the `target_apps` directory, with the name `[APP_NAME].apk`.
* Run the following command in the `script` directory (add `--is_emulator` option if you are using an emulator):
```bash
$ cd script
$ python run_droidagent.py --app [APP_NAME] --output_dir [OUTPUT_DIR] --is_emulator
# example: python run_droidagent.py --app AnkiDroid --output_dir ../evaluation/data_new/AnkiDroid --is_emulator
```


### Custom Persona & User Goals
According to your needs, use DroidAgent with a persona (a set of user characteristics) and a set of intents (a set of user goals) to guide the testing process. 

* You can add a custom persona by adding a new `.txt` file in the `resources/persona` directory, and giving the name of the file as an argument to `--profile_id` option to `run_droidagent.py`.
* You can adjust the goal by modifying the following line in `run_droidagent.py` (we plan to make this easily configurable in the future):
```python
    persona.update({
        'ultimate_goal': 'visit as many pages as possible while trying their core functionalities',
        # 'ultimate_goal': 'check whether the app supports interactions between multiple users', # for QuickChat case study
        'initial_knowledge': initial_knowledge_map(args.app, persona_name, app_name),
    })
```


### Generate Reports
We provide a script to generate a markdown report consisting of the generated tasks during the testing process. Run the following command in the `script` directory:
```bash
$ python make_report.py --result_dir [RESULT_DIR] --project [PROJECT_NAME]
```
Note that the `[RESULT_DIR]` should be the same as the `[OUTPUT_DIR]` you used in the previous step.
The task-by-task markdown report will be generated in the `reports/[PROJECT_NAME]` directory. Each report contains the task description, performed GUI actions, and the observation of the application state after the task execution with screenshots.

[Reports on the evaluation data - published on website (TBD)](https://testing-agent.github.io/droidagent-reports/)

Example of a report:
![report](resources/example_report.png)

## Replicate Evaluation Results
To replicate evaluation results for the paper "Intent-Driven Android GUI Testing with Autonomous Large Language Model Agents", follow the steps: 

* Download evaluation data from the below links (these are linked to Google drive uploads linked to an anonymised account).
    - [droidagent_data](https://drive.google.com/file/d/1J4LFozBcRUWlobRWUGsU6KkzNU3b95J7/view?usp=sharing)
    - [baselines_data](https://drive.google.com/file/d/1pKDOw7J-4aKI21ypoxucB74XtoU63UDL/view?usp=sharing)
    - [ablation_data](https://drive.google.com/file/d/1LbbF7oXOJoZUG0N9sxHTLqeLL60OOhsk/view?usp=sharing)
* Locate the DroidAgent data in the `evaluation/data` directory.
* Locate the baseline data in the `evaluation/baselines` directory.
* Locate the ablation data in the `evaluation/ablation` directory.
* Run the notebooks in the `evaluation/notebooks/` directory to replicate the results for each of our research questions.


## Troubleshooting
### SQLite (ChromaDB dependency) troubleshooting
* If you get a sqlite3 version-related error message from chromaDB dependency, follow the instruction about building pysqlite3 from source: [ChromaDB documentation](https://docs.trychroma.com/troubleshooting#sqlite)

* In short: `pip install pysqlite3-binary`
* Add following lines into `~/.pyenv/versions/testing-agent/lib/python3.10/site-packages/chromadb/__init__.py`:
```python
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```
