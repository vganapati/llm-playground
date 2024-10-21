"""
https://platform.openai.com/docs/guides/function-calling
https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
"""
import os
import argparse
from typing import Annotated, Literal
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored


parser = argparse.ArgumentParser()
parser.add_argument('--internal', action='store_true', help='Running internal to LBNL')
args = parser.parse_args()

if args.internal:
    base_url = "https://api-local.cborg.lbl.gov"
else:
    base_url = "https://api.cborg.lbl.gov"
client = OpenAI(
    api_key=os.environ.get('CBORG_API_KEY'), # do not store your API key in the code!
    base_url=base_url
)
model = "openai/gpt-4o"


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        raise

def get_msg_attributes(message):
    if isinstance(message, dict):
        return message["role"], message["content"]
    else:
        return message.role, message.content

    
def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }

    for message in messages:
        role, content = get_msg_attributes(message)
        if role == "system":
            print(colored(f"system: {content}\n", role_to_color[role]))
        elif role == "user":
            print(colored(f"user: {content}\n", role_to_color[role]))
        elif role == "assistant":
            if content:
                print(colored(f"assistant: {content}\n", role_to_color[role]))
            if message.tool_calls:
                print(colored(f"assistant: {message.tool_calls}\n", role_to_color[role]))
        elif role == "tool":
            print(colored(f"function ({message['name']}): result {content}\n", role_to_color[role]))

Operator = Literal["+", "-", "*", "/"]

def calculator(a: float, b: float, operator: Annotated[Operator, "operator"]) -> float:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        raise ValueError("Invalid operator")
    
def make_tool_calls(tool_calls):
    messages = []
    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        tool_function_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)

        if tool_function_name == "calculator":
            results = calculator(**tool_arguments)
        else:
            raise ValueError(f"Unknown function name: {tool_function_name}") 
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_function_name,
            "content": str(results)
        })
    return messages

function_description = {
  "name": "calculator",
#   "strict": True,
  "description": "A simple calculator that can add, subtract, multiply, or divide two numbers.",
  "parameters": {
    "type": "object",
    "properties": {
      "a": {
        "type": "number",
        "description": "The first number for the calculation."
      },
      "b": {
        "type": "number",
        "description": "The second number for the calculation."
      },
      "operator": {
        "type": "string",
        "enum": ["+", "-", "*", "/"],
        "description": "The arithmetic operator to use for the calculation. One of '+', '-', '*', '/'"
      }
    },
    "required": ["a", "b", "operator"]
  }
}


tools = [
    {
        "type": "function",
        "function": function_description
    }
]

messages = []
messages.append({"role": "system", "content": "Use calculator tool if possible. Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "What is 3+3*4?"})

for i in range(5):
    chat_response = chat_completion_request(
        messages, tools=tools, 
        # tool_choice={"type": "function", "function": {"name": "calculator"}},
    )
    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)

    tool_calls = assistant_message.tool_calls
    if tool_calls:
        messages += make_tool_calls(tool_calls)

    # messages.append({"role": "system", "content": "Use the information thus far to decide what to do next."})

pretty_print_conversation(messages)