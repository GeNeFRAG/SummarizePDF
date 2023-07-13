import pathlib
import sys

import numpy as np
import openai
import pdfplumber
import tomli
import wget

def get_completion(prompt, model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def optimize_text_for_api(text, max_tokens):
    tokenized_text = text.split()  # Tokenize the text by splitting on spaces
    if len(tokenized_text) > max_tokens:
        tokenized_text = tokenized_text[:max_tokens]  # Truncate the text to fit within the token limit
        optimized_text = ' '.join(tokenized_text)  # Join the tokens back into a string
        print("Text has been optimized to fit within the token limit.")
        return optimized_text
    else:
        return text

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
def getPaper(paper_url, filename):
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
def showPaperSummary(paperContent):
    if paperContent is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
        #model_list = openai.Model.list() 
        responses = ""
        for page in paperContent:   
            text = page.extract_text(layout=True) + tldr_tag
            prompt = f"""You will be provided with text from any PDF delimited by triple backtips.\
                        Your task is to summarize the chunks in an executive summary style. \
                        Provide the answer in at most 5 bulletpoint sentences and at most 100 words. \
                        Respond \"Unsure about answer\" if not sure about the answer. \
                        Reply in Language {lang}.\
                        ```{text}```
                        """
            
            # Call the OpenAI API to generate summary
            response = get_completion(prompt, gptmodel)

            # Store the summary
            responses = responses + response
        
        responses = optimize_text_for_api(responses, maxtokens)

        prompt = f"""Your task is to remove duplicate or similar information in provided text delimited by triple backtips. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{responses}```
                """
        response = get_completion(prompt, gptmodel)
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

paperFilePath = getPaper(url,ofile)

try:
    paperContent = pdfplumber.open(paperFilePath).pages
except Exception as e:
    print("Error opening PDF")
    print(e)
    sys.exit(1)

showPaperSummary(paperContent)