import openai
import wget
import pathlib
import pdfplumber
import numpy as np
import sys
import tomli

def getPaper(paper_url, filename="random_paper.pdf"):
    try:
        # Download the paper from the provided url, with the provided filename or default filename
        downloadedPaper = wget.download(paper_url, filename)    
        # Get the path to the downloaded paper
        downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    except:
        print("Error: Unable to download paper from provided URL.")
        return None

    return downloadedPaperFilePath

def showPaperSummary(paperContent):
    if paperContent is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
        model_list = openai.Model.list() 

        for page in paperContent:    
            text = page.extract_text(layout=True) + tldr_tag
            text = "Analyse and Summarize following text in short sentences: " + text
            # Call the OpenAI API to generate summary
            response = openai.Completion.create(model="text-davinci-003",prompt=text,temperature=0.3,
                max_tokens=maxtoken,
                top_p=0.9,
                frequency_penalty=0.2,
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            # Print the summary
            print(response["choices"][0]["text"])
    except:
        print("Error: Unable to generate summary for the paper.")

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["apikey"]
        openai.organization=data["organization"]
except:
    print("Error: Unable to read openai.toml file.")

# Getting max_tokens and PDF URL from command line
if len(sys.argv) == 1:
    raise Exception("Usage: SummarizePDFOpenAI <maxtokens> <URL to PDF>")

maxtoken=int(sys.argv[1])
url=sys.argv[2]

paperFilePath = getPaper(url)
paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)