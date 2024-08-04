# AI PDF QA Slack Agent

This project is an AI agent designed to extract answers from a PDF document based on given questions and post the results to Slack. It leverages the capabilities of OpenAI's GPT model and includes functionalities for PDF text extraction and Slack messaging.

## Features

- Extracts text from PDF documents.
- Uses OpenAI's GPT model to answer questions based on the extracted text.
- Posts the results to a Slack channel.
- Configurable via environment variables.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/shashankgd/pdf_qa_slack_agent.git
    cd pdf_qa_slack_agent
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your OpenAI and Slack API keys:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    SLACK_WEBHOOK_URL=your_slack_webhook_url
    ```

## Usage

Run the script from the command line with the path to the PDF and the list of questions:
```bash
python main.py --pdf_path path/to/your/pdf --questions "What is the name of the company?" "Who is the CEO of the company?" "What is their vacation policy?" "What is the termination policy?"
```
