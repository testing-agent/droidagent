from ..config import agent_config
from ..model import get_next_assistant_message, zip_messages

MAX_RETRY = 1


def prompt_summarized_widget_knowledge(memory, widget_description, relevant_widget_observations, prompt_recorder=None):
    system_message = f'''You are a helpful assistant who can infer the role and functionality of Android GUI widget based on previous user interactions on the widget, so that the user can understand the widget better.'''

    user_messages = []
    assistant_messages = []

    user_messages.append(f'''
Infer and describe the role and functionality of the following widget based on the past interaction results: 
> {widget_description}

Past interactions on the widget:
{relevant_widget_observations}

Describe the role and functionality of the widget briefly in one sentence based on the provided interaction history. Your answer should start with "The widget". If it seems that interacting the widget introduces a new page or widgets, try to include the name of the page or widgets in your answer. (e.g., The widget expands new options X, Y, Z, the widget opens a new page P, etc.) Do not include anything else except the description of the widget role in your answer.'''.strip())

    assistant_messages.append(get_next_assistant_message(system_message, user_messages, assistant_messages, model=agent_config.knowledge_summary_model))

    widget_knowledge = assistant_messages[-1].strip()

    if prompt_recorder is not None:
        prompt_recorder.record(zip_messages(system_message, user_messages, assistant_messages), 'widget_knowledge')

    return widget_knowledge
