import openai
import wget
import pathlib
import pdfplumber
import numpy as np
"""test"""
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
    openai.organization = 'Enter your organisation'
    openai.api_key = "Enter your API Key"
    model_list = openai.Model.list() 
    
    for page in paperContent:    
        text = page.extract_text() + tldr_tag
        response = openai.Completion.create(model="text-davinci-003",prompt=text,temperature=0.3,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            stop=["\n"]
        )
        print(page.page_number)
        print(response["choices"][0]["text"])

paperFilePath = getPaper("https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52020PC0595&from=EN")
paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)
