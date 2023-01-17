import openai
import wget
import pathlib
import pdfplumber
import numpy as np
import sys
import tomli

def getPaper(paper_url, filename="random_paper.pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local pathpip to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)    
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath

def showPaperSummary(paperContent):
    tldr_tag = "\n tl;dr:"
    model_list = openai.Model.list() 
    
    for page in paperContent:    
        text = page.extract_text(layout=True) + tldr_tag
        text = "Analyse and Summarize following text in short sentences: " + text
    
        response = openai.Completion.create(model="text-davinci-003",prompt=text,temperature=0.3,
            max_tokens=maxtoken,
            top_p=0.9,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            echo=False,
            stop=["\n"]
        )
        
        #print(page.page_number)
        print(response["choices"][0]["text"])

#Reading out OpenAI API keys and organisation
with open("openai.toml","rb") as f:
    data = tomli.load(f)
    openai.api_key=data["apikey"]
    openai.organization=data["organization"]

#Getting PDF URl from command line
if len(sys.argv) == 1:
    raise Exception("Usage: SummarizePDFOpenAI <maxtokens> <URL to PDF>")

maxtoken=int(sys.argv[1])
url=sys.argv[2]

paperFilePath = getPaper(url)
paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)