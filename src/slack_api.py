import logging
import requests
import json

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
