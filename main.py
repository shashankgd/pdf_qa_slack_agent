import logging
import argparse
from src.ai_agent import main as ai_agent_main

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    ai_agent_main(args.pdf_path, args.questions)
