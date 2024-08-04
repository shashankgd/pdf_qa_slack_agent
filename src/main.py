# main.py
import os
import openai
from pdf2image import convert_from_path
import pytesseract
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

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

def post_to_slack(channel, message):
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        assert response["ok"]
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")

def main(pdf_path, questions, slack_channel):
    context = extract_text_from_pdf(pdf_path)
    results = {}
    for question in questions:
        answer = ask_openai(question, context)
        if not answer or "Data Not Available" in answer:
            answer = "Data Not Available"
        results[question] = answer

    results_json = json.dumps(results, indent=4)
    post_to_slack(slack_channel, f"Results:\n```{results_json}```")

if __name__ == "__main__":
    pdf_path = "handbook.pdf"  # Path to the PDF file
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]  # Example questions
    slack_channel = "#general"  # Slack channel to post the results

    main(pdf_path, questions, slack_channel)