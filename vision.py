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


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/2/23/AlphaFold_2.png"
                    }
                },
                {"type": "text", "text": "What are some similar objects to those in the image?"},
            ]
        }
    ],
    max_tokens=300,
)

print(response.choices[0].message.content)