import logging
from src.ocr import extract_text_from_pdf
from src.openai_api import ask_openai
from src.slack_api import post_to_slack
from src.config import slack_webhook_url

def main(pdf_path, questions):
    try:
        context = extract_text_from_pdf(pdf_path)

        results = {}
        formatted_results = "Results:\n"
        for question in questions:
            logging.info(f"Processing question: {question}")
            answer = ask_openai(question, context)
            if not answer or "Data Not Available" in answer:
                answer = "Data Not Available"

            results[question] = answer
            formatted_results += f"Question: {question}\nAnswer:\n{answer}\n\n"

        # Print the message for debugging
        logging.info("Formatted results:\n" + formatted_results)

        post_to_slack(slack_webhook_url, formatted_results)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
