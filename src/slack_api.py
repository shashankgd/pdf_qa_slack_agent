# src/slack_api.py

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .config import SLACK_BOT_TOKEN

client = WebClient(token=SLACK_BOT_TOKEN)

def post_to_slack(channel, message):
    try:
        print(message)
        # response = client.chat_postMessage(channel=channel, text=message)
        # assert response["ok"]
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")