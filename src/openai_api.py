import logging
import openai
from src.config import openai_api_key

# Set OpenAI API key
openai.api_key = openai_api_key

def ask_openai(question, context):
    try:
        logging.info(f"Asking OpenAI: {question}")
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        answer = response.choices[0].message.content.strip()
        logging.info("Successfully received answer from OpenAI.")
        return answer
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        raise
