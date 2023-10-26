import openai
from openai.error import Timeout, ServiceUnavailableError, APIError

from .config import agent_config
import time

openai.api_key = agent_config.openai_api_key

TIMEOUT = 60
MAX_TOKENS = 500
MAX_RETRY = 1000
TEMPERATURE = 0.6

class APIUsageManager:
    usage = {}
    response_time = {}

    @classmethod
    def record_usage(cls, model, usage):
        if model not in cls.usage:
            cls.usage[model] = {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0,
            }
        cls.usage[model]['prompt_tokens'] += usage['prompt_tokens']
        cls.usage[model]['completion_tokens'] += usage['completion_tokens']
        cls.usage[model]['total_tokens'] += usage['total_tokens']

    @classmethod
    def record_response_time(cls, model, response_time):
        if model not in cls.response_time:
            cls.response_time[model] = []
        cls.response_time[model].append(response_time)


def stringify_prompt(prompt):
    prompt_str = ''

    prompt_str += f'\n*** System:\n{prompt["system_message"]}\n'
    
    for user_message, assistant_message in prompt['conversation']:
        prompt_str += f'\n*** User:\n{user_message}\n'
        if assistant_message is not None:
            prompt_str += f'\n*** Assistant:\n{assistant_message}\n'

    return prompt_str

def zip_messages(system_message, user_messages, assistant_messages):
    conversation = list(zip(user_messages, assistant_messages))
    if len(user_messages) == len(assistant_messages) + 1:
        conversation.append((user_messages[-1], None))
    return {
        "system_message": system_message,
        "conversation": conversation
    }

def get_next_assistant_message(system_message, user_messages, assistant_messages=[], functions=[], model="gpt-3.5-turbo-16k-0613", max_tokens=MAX_TOKENS, function_call_option=None):
    # If model is gpt-3.5-turbo-16k-0613 but the length sum of the prompt is lesser than 6k (approximately 4000 tokens), use gpt-3.5-turbo-0613 instead
    # if model == "gpt-3.5-turbo-16k-0613" and len(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages))) < 8000:
    #     model = "gpt-3.5-turbo-0613"
    #     print(f'Using {model} instead of gpt-3.5-turbo-16k-0613')
    # If model is gpt-4-0613 but the length sum of the prompt is larger than 16000 (approximately 8000 tokens), use gpt-4-32k-0613 instead
    # print(model)
    # print(len(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages))))
    # if model == "gpt-4-0613" and len(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages))) > 16000:
    #     model = "gpt-3.5-turbo-16k-0613"
    #     print(f'Using {model} instead of gpt-4-0613')

    start_time = time.time()

    messages = [{"role": "system", "content": system_message}]
    if len(user_messages) != len(assistant_messages) + 1:
        with open('errored_prompt.txt', 'w') as f:
            f.write(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages)))

        raise ValueError('Number of user messages should be one more than the number of assistant messages: refer to errored_prompt.txt')
    for user_message, assistant_message in zip(user_messages[:-1], assistant_messages):
        if isinstance(user_message, dict):
            messages.append({"role": "function", "name": user_message['name'], "content": user_message['return_value']})
        else:
            messages.append({"role": "user", "content": user_message})

        if isinstance(assistant_message, dict):
            messages.append({"role": "assistant", "content": None, "function_call": assistant_message})
        else:
            messages.append({"role": "assistant", "content": assistant_message})
    
    function_name = None
    if isinstance(user_messages[-1], dict):
        messages.append({"role": "function", "name": user_messages[-1]['name'], "content": user_messages[-1]['return_value']})
    else:
        messages.append({"role": "user", "content": user_messages[-1]})

    response = None
    for _ in range(MAX_RETRY):
        try:
            if len(functions) > 0:
                if function_call_option is not None:
                    response = openai.ChatCompletion.create(
                        model=model,
                        temperature=TEMPERATURE,
                        max_tokens=max_tokens,
                        functions=functions,
                        function_call=function_call_option,
                        messages=messages,
                        request_timeout=TIMEOUT
                    )
                else:
                    response = openai.ChatCompletion.create(
                        model=model,
                        temperature=TEMPERATURE,
                        max_tokens=max_tokens,
                        functions=functions,
                        messages=messages,
                        request_timeout=TIMEOUT
                    )
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    temperature=TEMPERATURE,
                    max_tokens=max_tokens,
                    messages=messages,
                    request_timeout=TIMEOUT
                )
        except (Timeout, ServiceUnavailableError, APIError):
            print(f'OpenAI API request timed out. Retrying...')
            time.sleep(3)
            continue
        except KeyboardInterrupt as e:
            raise e

        break

    if response is None:
        raise TimeoutError('OpenAI API request timed out multiple times')

    APIUsageManager.record_usage(model, response['usage'])
    APIUsageManager.record_response_time(model, time.time() - start_time)

    if response['choices'][0]['message']['content'] is None and 'function_call' in response['choices'][0]['message']:
        # function call
        return response['choices'][0]['message']['function_call']

    return response['choices'][0]['message']['content'].strip()

    