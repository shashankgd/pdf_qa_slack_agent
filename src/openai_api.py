# src/openai_api.py

import openai
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def ask_openai(question, context):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:",
        max_tokens=100,
        temperature=0.2,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    return answer