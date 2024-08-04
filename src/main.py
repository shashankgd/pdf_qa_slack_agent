# main.py
import os
import openai
from PyPDF2 import PdfReader
import requests
import json
import logging
import argparse

from config import openai_api_key, slack_webhook_url


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def ask_openai(question, context):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        raise

def post_to_slack(webhook_url, message):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'text': message
        }
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    except Exception as e:
        logging.error(f"Error posting to Slack: {e}")
        raise

def main(pdf_path, questions):
    try:
        context = extract_text_from_pdf(pdf_path)
        results = {}
        formatted_results = "Results:\n"
        for question in questions:
            answer = ask_openai(question, context)
            if not answer or "Data Not Available" in answer:
                answer = "Data Not Available"
            results[question] = answer
            formatted_results += f"Question: {question}\nAnswer:\n{answer}\n\n"

        # Print the message for debugging
        print(formatted_results)

        post_to_slack(slack_webhook_url, formatted_results)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF QA Slack Agent")
    parser.add_argument("--pdf_path", type=str, default="handbook.pdf", help="Path to the PDF file")
    parser.add_argument("--questions", nargs="+", default=[
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ], help="List of questions to ask")

    args = parser.parse_args()

    main(args.pdf_path, args.questions)
