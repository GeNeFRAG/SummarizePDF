import pathlib
import sys

import openai
import pdfplumber
import tomli
import wget
from GPTCommons import GPTCommons

def download_paper(paper_url, filename):
    """
    Downloads a paper from the provided URL and saves it with the specified filename or a default filename.

    Args:
    paper_url (str): The URL of the paper to be downloaded.
    filename (str, optional): The desired filename to save the paper as (default is None).

    Returns:
    pathlib.Path or None: The path to the downloaded paper file as a pathlib.Path object, or None if download fails.

    Example:
    >>> paper_url = "https://example.com/paper.pdf"
    >>> downloaded_paper = download_paper(paper_url, "research_paper.pdf")
    >>> print(downloaded_paper)
    '/path/to/research_paper.pdf'

    Note:
    This function uses the 'wget' library to download the paper from the URL. If the download fails, it returns None.
    """
    try:
        # Download the paper from the provided url, with the provided filename or default filename
        downloadedPaper = wget.download(paper_url, filename)    
        # Get the path to the downloaded paper
        downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    except Exception as e:
        print(f"Error: Unable to download paper from provided URL.")
        print(f"{e}")
        return None

    return downloadedPaperFilePath

def show_page_summary(paperContent):
    """
    Generates a summary of a PDF document's pages, removes duplicate or redundant information, and prints the result.

    Args:
    paper_content (list): A list of pages from the PDF document.

    Returns:
    None

    Example:
    >>> pdf_pages = [page1, page2, page3, ...]
    >>> show_page_summary(pdf_pages)
    [Summary of the PDF document's pages]
    [Cleaned text with duplicate/redundant information removed]

    Note:
    The function relies on the 'clean_text' and 'get_completion' functions, and it uses a specific model ('gptmodel') and language ('lang') for text generation.
    """
    if paperContent is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:" 
        responses = ""
        print(f"Summarizing PDF using OpenAI completion API with model {gptmodel}")
        for page in paperContent:   
            text = page.extract_text(layout=True) + tldr_tag
            text = commons.clean_text(text)
            prompt = f"""You will be provided with text from any PDF delimited by triple backtips.\
                        Your task is to summarize the chunks in a distinguished analytical summary style. \
                        Reply in Language {lang}.\
                        ```{text}```
                        """
            
            # Call the OpenAI API to generate summary
            response = commons.get_chat_completion(prompt, gptmodel, temperature)
            responses = responses + response
        
        responses = commons.clean_text(responses)
        responses = commons.reduce_to_max_tokens(responses, maxtokens, gptmodel)
        print(f"Remove duplicate or redundant information using OpenAI completion API with model {gptmodel}")
        prompt = f"""Your task is to remove duplicate or redundant information in the provided text delimited by triple backtips. \
                 Provide the answer in at most 5 bulletpoint sentences and keep the tone of the text and at most 500 words. \
                Your task is to create smooth transitions between each bulletpoint.
                ```{responses}```
                """
        response = commons.get_chat_completion(prompt, gptmodel, temperature)
        print(f"{response}")
    except Exception as e:
        print(f"Error: Unable to generate summary for the paper.")
        print(f"{e}")
        return None
    
# Initialize GPT utilities module
commons = GPTCommons()

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
except Exception as e:
    print(f"Error: Unable to read openai.toml file.")
    print(f"{e}")
    sys.exit(1)

openai.api_key=data["openai"]["apikey"]
openai.organization=data["openai"]["organization"]
gptmodel = data["openai"]["model"]
maxtokens = int(data["openai"]["maxtokens"])
temperature = float(data["openai"]["temperature"])
print(f"gptmodel={gptmodel}")
print(f"maxtokens={maxtokens}")
print(f"temperature={temperature}")

# Getting max_tokens, PDF URL and local filename from command line
lang=commons.get_arg('--lang', "English")
url=commons.get_arg('--url', None)
ofile=commons.get_arg('--ofile','random_paper.pdf')

if(url == None):
    print(f"Type “--help\" for more information.")
    sys.exit(1)
print(f"Downloading PDF")
paperFilePath = download_paper(url, ofile)

try:
    pdf = pdfplumber.open(paperFilePath)
    paperContent = pdf.pages
except Exception as e:
    print(f"Error opening PDF")
    print(f"{e}")
    sys.exit(1)
finally:
    pdf.close()

show_page_summary(paperContent)