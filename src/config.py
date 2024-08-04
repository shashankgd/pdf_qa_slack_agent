# config.py
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

if not openai_api_key or not slack_webhook_url:
    raise ValueError("Missing required environment variables: OPENAI_API_KEY and/or SLACK_WEBHOOK_URL")
