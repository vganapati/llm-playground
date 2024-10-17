import os
import argparse

from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument('--cborg', action='store_true', help='Running with LBNL credentials')
parser.add_argument('--internal', action='store_true', help='Running internal to LBNL')
args = parser.parse_args()

if args.cborg:
    if args.internal:
        base_url = "https://api-local.cborg.lbl.gov"
    else:
        base_url = "https://api.cborg.lbl.gov"
    client = OpenAI(
        api_key=os.environ.get('CBORG_API_KEY'), # Please do not store your API key in the code
        base_url=base_url
    )
    model = "lbl/llama"
    model_embeddings = "lbl/nomic-embed-text"
else:
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'), # Please do not store your API key in the code
        base_url="https://api.openai.com/v1" # Local clients can also use https://api-local.cborg.lbl.gov
    )
    model = "gpt-4o-mini"
    model_embeddings = "text-embedding-3-large"

# Create a human-like response to a prompt

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about DOE BER."
        }
    ]
)

print(completion.choices[0].message.content)

# generate an image based on a textual prompt (does not work with cborg)

if not(args.cborg):
    response = client.images.generate(
        prompt="A cute baby sea otter",
        n=2,
        size="1024x1024"
    )

    print(response.data[0].url)


# create vector embeddings for a string of text

response = client.embeddings.create(
    model=model_embeddings,
    input="The kramers kronigs relationships describe a physical phenomenon..."
)

print(response)