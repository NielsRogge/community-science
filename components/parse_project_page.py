from ast import literal_eval
import typing_extensions as typing

import google.generativeai as genai
import os
import requests


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# read prompt from txt file
with open("prompts/find_github_url.txt", "r") as file:
    prompt = file.read()


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def search_github_url_within_project_url(url: str) -> str:
    # Given the project page URL, we fetch the HTML content
    # and extract the GitHub URL from it.
    html_content = get_html(url)
    
    # TODO Add few-shots
    chat = model.start_chat()

    class Parsing(typing.TypedDict):
        github_url: str

    response = chat.send_message({"role": "user", "parts": [prompt, html_content]},
                                 generation_config=genai.GenerationConfig(
                                    response_mime_type="application/json", response_schema=Parsing
    ))

    # parse as dict
    response = literal_eval(response.text)
    
    return response