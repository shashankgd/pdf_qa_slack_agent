# tests/test_ai_agent.py

import unittest
from src.ai_agent import AIAgent

class TestAIAgent(unittest.TestCase):
    def test_run(self):
        pdf_path = "handbook.pdf"
        questions = [
            "What is the name of the company?",
            "Who is the CEO of the company?",
            "What is their vacation policy?",
            "What is the termination policy?"
        ]
        slack_channel = "#general"
        agent = AIAgent(pdf_path, questions, slack_channel)
        agent.run()

if __name__ == "__main__":
    unittest.main()