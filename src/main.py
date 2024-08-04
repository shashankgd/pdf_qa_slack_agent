# main.py
import os
import openai
from PyPDF2 import PdfReader
import requests
import json
import logging
import argparse
import faiss
import numpy as np

from config import openai_api_key, slack_webhook_url

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set OpenAI API key
openai.api_key = openai_api_key

# Initialize FAISS index
dimension = 1536  # Adjust according to the model's embedding dimension
index = faiss.IndexFlatL2(dimension)
questions_answers = {}  # Store the actual question-answer pairs

def extract_text_from_pdf(pdf_path):
    try:
        logging.info(f"Extracting text from PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        logging.info("Successfully extracted text from PDF.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def get_openai_embedding(text):
    try:
        logging.info("Generating embedding for text.")
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=[text]
        )
        embedding = np.array(response['data'][0]['embedding'], dtype=np.float32)
        logging.info("Successfully generated embedding.")
        return embedding
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        raise

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
        answer = response['choices'][0]['message']['content'].strip()
        logging.info("Successfully received answer from OpenAI.")
        return answer
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        raise

def summarize_text(text):
    try:
        logging.info("Summarizing text.")
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ],
            max_tokens=1000  # Adjust the max tokens as needed
        )
        summary = response.choices[0].message.content.strip()
        logging.info("Successfully summarized text.")
        return summary
    except Exception as e:
        logging.error(f"Error summarizing text with OpenAI API: {e}")
        raise

def split_text(text, max_tokens):
    logging.info("Splitting text into chunks.")
    words = text.split()
    current_chunk = []
    current_length = 0
    chunks = []

    for word in words:
        current_length += len(word) + 1  # Add 1 for the space
        if current_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    logging.info(f"Split text into {len(chunks)} chunks.")
    return chunks

def post_to_slack(webhook_url, message):
    try:
        logging.info("Posting message to Slack.")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'text': message
        }
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        logging.info("Successfully posted message to Slack.")
    except Exception as e:
        logging.error(f"Error posting to Slack: {e}")
        raise

def main(pdf_path, questions):
    try:
        context = extract_text_from_pdf(pdf_path)
        context_chunks = split_text(context, 1000)  # Split the context into chunks of 1000 tokens each

        logging.info("Generating summarized context.")
        summarized_contexts = [summarize_text(chunk) for chunk in context_chunks]
        combined_summary = " ".join(summarized_contexts)

        results = {}
        formatted_results = "Results:\n"
        for question in questions:
            logging.info(f"Processing question: {question}")
            question_embedding = get_openai_embedding(question)

            if index.ntotal > 0:
                _, I = index.search(np.array([question_embedding]), k=1)
                if I[0][0] < len(questions_answers):
                    answer = questions_answers[I[0][0]]
                    logging.info("Answer found in cache.")
                else:
                    answer = ask_openai(question, combined_summary)
                    index.add(np.array([question_embedding]))
                    questions_answers[index.ntotal - 1] = answer
                    logging.info("New Q&A added to cache.")
            else:
                answer = ask_openai(question, combined_summary)
                index.add(np.array([question_embedding]))
                questions_answers[index.ntotal - 1] = answer
                logging.info("First Q&A added to cache.")

            if not answer or "Data Not Available" in answer:
                answer = "Data Not Available"

            results[question] = answer
            formatted_results += f"Question: {question}\nAnswer:\n{answer}\n\n"

        # Print the message for debugging
        logging.info("Formatted results:\n" + formatted_results)

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