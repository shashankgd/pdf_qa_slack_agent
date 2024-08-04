# main.py
import os
import openai
from PyPDF2 import PdfReader
import requests
import json
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_openai(question, context):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

def post_to_slack(webhook_url, message):
    print(message)
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'text': message
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

def main(pdf_path, questions):
    context = extract_text_from_pdf(pdf_path)
    results = {}
    for question in questions:
        answer = ask_openai(question, context)
        if not answer or "Data Not Available" in answer:
            answer = "Data Not Available"
        results[question] = answer

    results_json = json.dumps(results, indent=4)
    post_to_slack(slack_webhook_url, f"Results:\n```{results_json}```")

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
