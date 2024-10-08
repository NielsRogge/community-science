# A repo to parse Arxiv papers

This repository allows to automatically extract Github URLs and project page URLs from Arxiv papers.

It leverages the [Gemini API](https://ai.google.dev/gemini-api/docs) for that.

## Installation

```
pip install -r requirements.txt
```

## Usage

```bash
export API_KEY="" # your Gemini API key, create it at https://aistudio.google.com/app/apikey
python main.py
``` 