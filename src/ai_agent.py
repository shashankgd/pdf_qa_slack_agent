# src/ai_agent.py

from .ocr import extract_text_from_pdf
from .openai_api import ask_openai
from .slack_api import post_to_slack
import json

class AIAgent:
    def __init__(self, pdf_path, questions, slack_channel):
        self.pdf_path = pdf_path
        self.questions = questions
        self.slack_channel = slack_channel

    def run(self):
        context = extract_text_from_pdf(self.pdf_path)
        results = {}
        for question in self.questions:
            answer = ask_openai(question, context)
            if not answer or "Data Not Available" in answer:
                answer = "Data Not Available"
            results[question] = answer

        results_json = json.dumps(results, indent=4)
        post_to_slack(self.slack_channel, f"Results:\n```{results_json}```")