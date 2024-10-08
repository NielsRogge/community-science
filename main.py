import google.generativeai as genai
import os

from parse_pdf import extract_first_two_pages


genai.configure(api_key=os.environ["API_KEY"])

# read prompt from txt file
with open("prompt.txt", "r") as file:
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

model = genai.GenerativeModel("gemini-1.5-flash-8b")

chat = model.start_chat(
    history=[
        {"role": "user", "parts": [prompt, sample_pdf_1]},
        {"role": "model", "parts": response_1},
        {"role": "user", "parts": [prompt, sample_pdf_2]},
        {"role": "model", "parts": response_2},
    ]
)

# Example usage
input_pdf = "/Users/nielsrogge/Downloads/2410.02115v2.pdf"
sample_pdf_3 = "output.pdf"
extract_first_two_pages(input_pdf, sample_pdf_3)

sample_pdf_3 = genai.upload_file(sample_pdf_3)

response = chat.send_message({"role": "user", "parts": [prompt, sample_pdf_3]})
print(response.text)