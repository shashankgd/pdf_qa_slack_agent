# setup.py

from setuptools import setup, find_packages

setup(
    name="pdf_qa_slack_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pytesseract",
        "pdf2image",
        "slack_sdk",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "zania_ai_agent=src.ai_agent:main",
        ],
    },
)