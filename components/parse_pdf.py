from ast import literal_eval
import typing_extensions as typing
import os

import google.generativeai as genai

from components.utils.parse_pdf import extract_first_two_pages


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-8b")


# read prompt from txt file
with open("prompts/prompt.txt", "r") as file:
    prompt = file.read()

# add few-shots
sample_pdf_1  = genai.upload_file("/Users/nielsrogge/Downloads/2409.18313v3.pdf")
response_1 = """
```json
{'project_page_url': 'https://quanting-xie.github.io/Embodied-RAG-web/', 'github_url': ''}
```
"""

sample_pdf_2 = genai.upload_file("/Users/nielsrogge/Downloads/2410.00337v1.pdf")
response_2 = """
```json
{'project_page_url': 'https://len-li.github.io/syntheocc-web/', 'github_url': ''}
```
"""


def get_project_github_urls(pdf_path: str) -> str:    
    # Add few-shots
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": [prompt, sample_pdf_1]},
            {"role": "model", "parts": response_1},
            {"role": "user", "parts": [prompt, sample_pdf_2]},
            {"role": "model", "parts": response_2},
        ]
    )

    # Add query
    sample_pdf_3 = "output.pdf"
    extract_first_two_pages(pdf_path, sample_pdf_3)

    sample_pdf_3 = genai.upload_file(sample_pdf_3)

    class Parsing(typing.TypedDict):
        github_url: str
        project_page_url: str

    response = chat.send_message({"role": "user", "parts": [prompt, sample_pdf_3]},
                                 generation_config=genai.GenerationConfig(
                                    response_mime_type="application/json", response_schema=Parsing
    ))

    # parse as dict
    response = literal_eval(response.text)
    
    return response