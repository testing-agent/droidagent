import openai
from openai import OpenAI
from dotenv import load_dotenv 
from .config import agent_config
import time

load_dotenv()
client = OpenAI()

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
        cls.usage[model]['prompt_tokens'] += usage.prompt_tokens
        cls.usage[model]['completion_tokens'] += usage.completion_tokens
        cls.usage[model]['total_tokens'] += usage.total_tokens

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
    # If model is gpt-3.5-turbo-16k-0613 but the tokens in the prompt are less than 4000 tokens, use gpt-3.5-turbo-0613 instead
    if model == "gpt-3.5-turbo-16k-0613" and len(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages))) < 8000: # approximately 4000 tokens
        model = "gpt-3.5-turbo-0613"
        print(f'Using {model} instead of gpt-3.5-turbo-16k-0613')
    
    if model == "gpt-4-0613" and len(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages))) > 16000:    # approximately 8000 tokens
        model = "gpt-3.5-turbo-16k-0613"
        print(f'Using {model} instead of gpt-4-0613 (context limit exceeded)')

    start_time = time.time()

    messages = [{"role": "system", "content": system_message}]
    if len(user_messages) != len(assistant_messages) + 1:
        with open('errored_prompt.txt', 'w') as f:
            f.write(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages)))

        raise ValueError('Number of user messages should be one more than the number of assistant messages: refer to `errored_prompt.txt`')
    for user_message, assistant_message in zip(user_messages[:-1], assistant_messages):
        if not isinstance(user_message, str):
            messages.append({"role": "tool", "tool_call_id": user_message['tool_call_id'], "name": user_message['name'], "content": user_message['return_value']})
        else:
            messages.append({"role": "user", "content": user_message})

        if not isinstance(assistant_message, str):
            messages.append({"role": "assistant", "content": None, "tool_calls": [assistant_message]})
        else:
            messages.append({"role": "assistant", "content": assistant_message})
    
    function_name = None
    user_message = user_messages[-1]
    if not isinstance(user_messages[-1], str):
        messages.append({"role": "tool", "tool_call_id": user_message['tool_call_id'], "name": user_message['name'], "content": user_message['return_value']})
    else:
        messages.append({"role": "user", "content": user_message})

    response = None
    for _ in range(MAX_RETRY):
        try:
            if len(functions) > 0:
                if function_call_option is not None:
                    response = client.chat.completions.create(
                        model=model,
                        temperature=TEMPERATURE,
                        max_tokens=max_tokens,
                        tools=functions,
                        tool_choice=function_call_option,
                        messages=messages,
                        timeout=TIMEOUT
                    )
                else:
                    response = client.chat.completions.create(
                        model=model,
                        temperature=TEMPERATURE,
                        max_tokens=max_tokens,
                        tools=functions,
                        messages=messages,
                        timeout=TIMEOUT
                    )
            else:
                response = client.chat.completions.create(
                    model=model,
                    temperature=TEMPERATURE,
                    max_tokens=max_tokens,
                    messages=messages,
                    timeout=TIMEOUT
                )
        except (openai.APITimeoutError, openai.APIConnectionError, openai.InternalServerError, openai.RateLimitError):
            print(f'OpenAI API request errored. Retrying...')
            time.sleep(3)
            continue
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            with open('errored_prompt.txt', 'w') as f:
                f.write(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages)))
            raise e

        break

    if response is None:
        raise TimeoutError('OpenAI API request errored multiple times')

    APIUsageManager.record_usage(model, response.usage)
    APIUsageManager.record_response_time(model, time.time() - start_time)

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        return {
            "id": tool_calls[0].id,
            "type": tool_calls[0].type,
            "function": {
                "name": tool_calls[0].function.name,
                "arguments": tool_calls[0].function.arguments
            }
        }

    return response_message.content.strip()

    