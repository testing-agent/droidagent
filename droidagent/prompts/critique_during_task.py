from ..config import agent_config
from ..model import get_next_assistant_message, zip_messages
from ..utils import *


def prompt_critique(memory, prompt_recorder=None):
    system_message = f'''
You are a helpful inspector who can review the GUI actions performed on an Android mobile app named {agent_config.app_name}. The actions are done by a person named "{agent_config.persona_name}" to accomplish the target task: {add_period(memory.task)} {add_period(memory.task_end_condition)}

{agent_config.persona_name} has the following profile:
{agent_config.persona_profile}

You are going to provide helpful feedback and suggest a revised plan to help {agent_config.persona_name} successfully accomplish the task.
    '''.strip()

    assistant_messages = []
    user_messages = []

    user_messages.append(f'''
Critique the actions done by {agent_config.persona_name} with respect to the current task, and give a helpful workaround if {agent_config.persona_name} is struggling to accomplish the task.

Task execution history so far (listed in chronological order):
===
{memory.describe_working_memory()}
===

Current page: {memory.current_activity} 
Widgets in current page:
```json
{memory.current_gui_state.describe_screen_w_memory(memory, show_id=False, during_task=True, prompt_recorder=prompt_recorder)}
```
Guideline for criticizing the actions:
- Note that `num_prev_actions` property means the number of times the widget has been interacted with so far.
- Note that `widget_role_inference` property means the role of the widget inferred by previous actions. Use this property to infer what the widget is used for. If `widget_role_inference` property is not included in the widget dictionary, the widget has not been interacted yet.
- When I am stuck, you might guide me to explore the new widgets that have not been used and doesn't know the role yet.
- I don't want to do the same actions repeatedly except it is clearly needed for the task (e.g., navigating back to the first page of the app), so guide me to perform effective actions to complete the task.

I am going to provide a template for your output to reason about your choice step by step. Fill out the <...> parts in the template with your own words. Do not include anything else in your answer except the text to fill out the template. Preserve the formatting and overall template.

=== Below is the template for your answer ===
Critique of task execution so far: <1~2 sentences in one line, say "okay" if everything seems fine.>
Need a workaround plan?: <yes/no, do not include any other word except "yes" or "no">
Workaround plan for {agent_config.persona_name}: <Start with "{agent_config.persona_name} needs to", and describe in one line. Say just "none" if {agent_config.persona_name} is doing well and no workaround is needed.>
    '''.strip())

    assistant_messages.append(get_next_assistant_message(system_message, user_messages, assistant_messages, model=agent_config.reflector_model))

    def parse_critique(result):
        critique = None
        workaround = None
        need_workaround = False

        for l in result.split('\n'):
            l = l.strip()
            if l.startswith(f"Critique of task execution so far:"):
                critique = l.split(f"Critique of task execution so far:")[1].strip()
                if critique.lower().startswith('okay') or critique.lower().startswith('everything seems okay') or critique.lower().startswith('everything seems fine'):
                    critique = None
            elif l.startswith('Need a workaround plan?:'):
                need_workaround = l.split('Need a workaround plan?:')[1].strip()
                if 'yes' in need_workaround.lower():
                    need_workaround = True
            elif l.startswith(f'Workaround plan for {agent_config.persona_name}:'):
                workaround = l.split(f'Workaround plan for {agent_config.persona_name}:')[1].strip()
                if workaround.lower().startswith('none'):
                    workaround = None

        if need_workaround == False:
            critique = None
            workaround = None
            
        return critique, workaround

    critique, workaround = parse_critique(assistant_messages[-1])

    prompt = zip_messages(system_message, user_messages, assistant_messages)
    if prompt_recorder is not None:
        prompt_recorder.record(prompt, 'action_critique')

    return critique, workaround