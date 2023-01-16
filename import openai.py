import openai
import wget
import pathlib
import pdfplumber
import numpy as np
import sys

def getPaper(paper_url, filename="random_paper.pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local path to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)    
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath

def showPaperSummary(paperContent):
    tldr_tag = "\n tl;dr:"
    openai.organization = ''
    openai.api_key = "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"
    model_list = openai.Model.list() 
    
    for page in paperContent:    
        text = page.extract_text() + tldr_tag
        text = "Analyse and Summarize following text in short sentences: " + text
    
        response = openai.Completion.create(model="text-davinci-003",prompt=text,temperature=0.3,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            echo=False,
            stop=["\n"]
        )
        
        #print(page.page_number)
        print(response["choices"][0]["text"])



if len(sys.argv) == 1:
    raise Exception("URL to PDF missing")
url=sys.argv[1]

paperFilePath = getPaper(url)
paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)