import pathlib
import re
import string
import sys

import openai
import pdfplumber
import tomli
import wget

SPECIAL_CHARACTERS = string.punctuation + "“”‘’"
PATTERN = re.compile(r'[\n\s]+')

def clean_text(text):
    """
    Cleans a given text by replacing line breaks, consecutive whitespace, and handling special characters.

    Args:
    text (str): The input text to be cleaned.

    Returns:
    str: The cleaned text.

    Example:
    >>> dirty_text = "This is a\ndirty    text!!"
    >>> clean_text(dirty_text)
    'This is a dirty text  '
    """
   # Replace line breaks and consecutive whitespace with a single space
    text = re.sub(PATTERN, ' ', text).strip()
    
    # Handle special characters (replace with spaces or remove them)
    text = ''.join(char if char not in SPECIAL_CHARACTERS else ' ' for char in text)
    
    return text

def get_completion(prompt, model, temperature=0):
    """
    Retrieves a completion using the OpenAI ChatCompletion API with the specified model and parameters.

    Args:
    prompt (str): The user's input or prompt for generating the completion.
    model (str): The OpenAI model identifier (e.g., "gpt-3.5-turbo").
    temperature (float, optional): The degree of randomness in the model's output (default is 0).
                                   A higher value makes the output more random, while a lower value makes it more deterministic.

    Returns:
    str: The generated completion text.

    Example:
    >>> user_prompt = "Translate the following English text to French: 'Hello, how are you?'"
    >>> model_id = "gpt-3.5-turbo"
    >>> get_completion(user_prompt, model_id, temperature=0.7)
    'Bonjour, comment ça va ?'
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_arg(arg_name, default=None):
    """
    Retrieves the value of a command-line argument by its name from the sys.argv list.

    Args:
    arg_name (str): The name of the command-line argument to retrieve.
    default: The default value to return if the argument is not found (default is None).

    Returns:
    str or default: The value of the specified command-line argument or the default value if not found.

    Example:
    >>> # Assuming the command-line arguments are ['--lang', 'English', '--url', 'example.com']
    >>> get_arg('--lang', 'Spanish')
    'English'
    >>> get_arg('--url', 'localhost')
    'example.com'
    >>> get_arg('--port', 8080)
    8080
    """
    if "--help" in sys.argv:
        print("Usage: python PD_AI_Sum.py [--help] [--lang] [--url] [--ofile]")
        print("Arguments:")
        print("\t--help\t\tHelp\t\tNone")
        print("\t--lang\t\tLanguage\tEnglish")
        print("\t--url\t\tPDF URL\t\tNone")
        print("\t--ofile\t\tOutpout file\trandom_paper.pdf")
        # Add more argument descriptions here as needed
        sys.exit(0)
    try:
        arg_index = sys.argv.index(arg_name)
        arg_value = sys.argv[arg_index + 1]
        return arg_value
    except (IndexError, ValueError):
        return default

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
        print("Error: Unable to download paper from provided URL.")
        print(e)
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
            text = clean_text(text)
            prompt = f"""You will be provided with text from any PDF delimited by triple backtips.\
                        Your task is to summarize the chunks in a distinguished analytical executive summary style. \
                        Reply in Language {lang}.\
                        ```{text}```
                        """
            
            # Call the OpenAI API to generate summary
            response = get_completion(prompt, gptmodel)
            responses = responses + response
        
        responses = clean_text(responses)
        print(f"Remove duplicate or redundant information using OpenAI completion API with model {gptmodel}")
        prompt = f"""Your task is to remove duplicate or redundant information in the provided text delimited by triple backtips. \
                 Provide the answer in at most 5 bulletpoint sentences and keep the tone of the text and at most 100 words. \
                Your task is to create smooth transitions between each bulletpoint.
                ```{responses}```
                """
        response = get_completion(prompt, gptmodel, 0.2)
        print(response)
    except Exception as e:
        print("Error: Unable to generate summary for the paper.")
        print(e)
        return None

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

openai.api_key=data["openai"]["apikey"]
openai.organization=data["openai"]["organization"]
gptmodel = data["openai"]["model"]
maxtokens = int(data["openai"]["maxtokens"])

# Getting max_tokens, PDF URL and local filename from command line
lang=get_arg('--lang', "English")
url=get_arg('--url', None)
ofile=get_arg('--ofile','random_paper.pdf')

if(url == None):
    print("Type “--help\" for more information.")
    sys.exit(1)
print(f"Downloading PDF")
paperFilePath = download_paper(url, ofile)

try:
    pdf = pdfplumber.open(paperFilePath)
    paperContent = pdf.pages
except Exception as e:
    print("Error opening PDF")
    print(e)
    sys.exit(1)
finally:
    pdf.close()

show_page_summary(paperContent)