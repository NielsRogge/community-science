import typing_extensions as typing
import os
import requests

import google.generativeai as genai


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-8b")


def get_readme(url: str) -> str:
    """
    Given a URL, this function fetches the README content from the GitHub repository.
    """
    owner, repository = url.split("/")[-2:]
    markdown_url = f"https://raw.githubusercontent.com/{owner}/{repository}/refs/heads/main/README.md"

    response = requests.get(markdown_url)
    return response.text


def parse_readme(url: str) -> str:
    markdown_content = get_readme(url)

    # TODO Add few-shots
    chat = model.start_chat()

    # Add query
    # read prompt from txt file
    with open("prompts/parse_github_readme.txt", "r") as file:
        prompt = file.read()

    response = chat.send_message({"role": "user", "parts": [prompt, markdown_content]})
    
    return response.text