"""
https://cookbook.openai.com/examples/sdg1
"""

from openai import OpenAI
import os
import re
import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json
import matplotlib

client = OpenAI()

datagen_model = "gpt-4o-mini"
question = """
Create a CSV file with 10 rows of housing data.
Each row should include the following fields:
 - id (incrementing integer starting at 1)
 - house size (m^2)
 - house price
 - location
 - number of bedrooms

Make sure that the numbers make sense (i.e. more rooms is usually bigger size, more expensive locations increase price. more size is usually higher price etc. make sure all the numbers make sense). Also only respond with the CSV.
"""

response = client.chat.completions.create(
    model=datagen_model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to generate synthetic data."},
        {"role": "user", "content": question}
    ]
)

res = response.choices[0].message.content
print(res)