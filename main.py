from components.parse_pdf import get_project_github_urls
from components.parse_project_page import search_github_url_within_project_url
from components.parse_github_readme import parse_readme


def main(pdf_path: str) -> str:

    # step 1: get Github and project page URL from first 2 pages of PDF
    result = get_project_github_urls(pdf_path)

    print("Result step 1:", result)

    # step 2: if Github URL is not found, search for it in the project page
    if result["github_url"] == "" and result["project_page_url"] != "":
        project_page_url = result["project_page_url"]
        github_url = search_github_url_within_project_url(project_page_url)["github_url"]
        result["github_url"] = github_url

    print("Result step 2:", result)

    # step 3: if Github URL is present, parse the README
    if result["github_url"] != "":
        result = parse_readme(result["github_url"])

    print("Result step 3:", result)

if __name__ == "__main__":
    pdf_path = "/Users/nielsrogge/Downloads/2406.02842v2.pdf"
    result = main(pdf_path)