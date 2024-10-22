"""
https://platform.openai.com/docs/assistants/quickstart
"""

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'), # do not store your API key in the code!
    default_headers={"OpenAI-Beta": "assistants=v2"},
)

model = "gpt-3.5-turbo"

assistant = client.beta.assistants.create(
    # custom_llm_provider="openai",
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model=model,
)

# a thread is a conversation between a user and 1 or more assistants
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Pamina."
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )
    print(run_steps)
else:
    print(run.status)