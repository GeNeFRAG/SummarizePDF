import openai
import wget
import pathlib
import pdfplumber
import numpy as np
import sys
import tomli

"""
This function downloads a paper from the provided URL and saves it with the provided filename or a default filename of "random_paper.pdf". It then returns the path to the downloaded paper. If an error occurs when downloading the paper, it prints an error message and returns None. 
"""
def getPaper(paper_url, filename):
    try:
        # Download the paper from the provided url, with the provided filename or default filename
        downloadedPaper = wget.download(paper_url, filename)    
        # Get the path to the downloaded paper
        downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    except:
        print("Error: Unable to download paper from provided URL.")
        return None

    return downloadedPaperFilePath


"""
This function takes in a paperContent and prints out a summary of the paper. It first checks if the paperContent is None and returns if it is. It then creates a tldr tag to be added at the end of each summary It then calls the OpenAI API to generate a summary with certain parameters such as temperature, max_tokens, top_p, frequency_penalty, presence_penalty, echo and stop. Finally it prints out the generated summary. 
"""
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
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                temperature=1,
                max_tokens=maxtoken,
                frequency_penalty=0.2,
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            # Print the summary
            print(response["choices"][0]["text"])
    except:
        print("Error: Unable to generate summary for the paper.")
        sys.exit(1)

"""
This code is reading out the OpenAI API keys and organization from a toml file, then getting the max_tokens and URL of a PDF from the command line. It then downloads the PDF and displays a summary of it to std out.
"""
# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting max_tokens, PDF URL and local filename from command line
if len(sys.argv) == 1:
    raise Exception("Usage: SummarizePDFOpenAI <maxtokens> <URL to PDF> <optional: filename>")
    sys.exit(1)
try:
    maxtoken=int(sys.argv[1])
    url=sys.argv[2]
except Exception as e:
    print("Error retrieving commandline arguments")
    print(e)
    sys.exit(1)
try:
    filename=sys.argv[3]
except: 
    filename="random_paper.pdf"

paperFilePath = getPaper(url,filename)
paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)