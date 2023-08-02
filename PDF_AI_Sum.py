import pathlib
import re
import string
import sys

import openai
import pdfplumber
import tomli
import wget


def clean_text(text):
    # Remove line breaks and replace with spaces
    text = text.replace('\n', ' ')
    
    # Normalize whitespace (remove extra spaces, tabs, etc.)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Handle special characters (replace with spaces or remove them)
    special_characters = string.punctuation + "“”‘’"
    text = ''.join(char if char not in special_characters else ' ' for char in text)
    
    # Remove consecutive spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_completion(prompt, model, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_arg(arg_name, default=None):
    """
    Safely reads a command line argument by name.
    :param arg_name: the name of the argument to read.
    :param default: the default value to return if the argument is not found.
    :return: the value of the argument if found, or the default value.
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
        arg_value = sys.argv[sys.argv.index(arg_name) + 1]
        return arg_value
    except (IndexError, ValueError):
        return default

# This function downloads a paper from the provided URL and saves it with the provided filename or a default filename of "random_paper.pdf". It then returns the path to the downloaded paper. If an error occurs when downloading the paper, it prints an error message and returns None. 
def download_paper(paper_url, filename):
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

# This function takes in a paperContent and prints out a summary of the paper. It first checks if the paperContent is None and returns if it is. It then creates a tldr tag to be added at the end of each summary It then calls the OpenAI API to generate a summary with certain parameters such as temperature, max_tokens, top_p, frequency_penalty, presence_penalty, echo and stop. Finally it prints out the generated summary. 
def show_page_summary(paperContent):
    if paperContent is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
        #model_list = openai.Model.list() 
        responses = ""
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

            # Store the summary
            responses = responses + response
        
        responses = clean_text(responses)

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
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
        gptmodel = data["openai"]["model"]
        maxtokens = int(data["openai"]["maxtokens"])
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting max_tokens, PDF URL and local filename from command line
lang=get_arg('--lang', "English")
url=get_arg('--url', None)
ofile=get_arg('--ofile','random_paper.pdf')

if(url == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

paperFilePath = download_paper(url, ofile)

try:
    paperContent = pdfplumber.open(paperFilePath).pages
except Exception as e:
    print("Error opening PDF")
    print(e)
    sys.exit(1)

show_page_summary(paperContent)