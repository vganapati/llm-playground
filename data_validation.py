"""
https://cookbook.openai.com/examples/o1/using_reasoning_for_data_validation
"""

from openai import OpenAI
import json
from sklearn.metrics import precision_score, recall_score, f1_score
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import pandas as pd

client = OpenAI()
MODEL = 'o1-preview'

# TODO