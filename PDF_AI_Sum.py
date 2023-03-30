import pathlib
import sys

import numpy as np
import openai
import pdfplumber
import tomli
import wget


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
        model_list = openai.Model.list() 

        for page in paperContent:    
            text = page.extract_text(layout=True) + tldr_tag
            prompt = "Analyse and Summarize following text in short sentences and reply in " + lang + ": " + text
            # Call the OpenAI API to generate summary
            '''
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                temperature=1,
                max_tokens=maxtoken,
                frequency_penalty=0.2
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            # Print the summary
            print(response["choices"][0]["text"])
            '''
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a super smart academic researcher looking for truth"},
                    {"role": "user", "content": prompt}, 
                ]
            )

            # Print the summary
            print(response['choices'][0]['message']['content'])

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
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting max_tokens, PDF URL and local filename from command line
if len(sys.argv) < 3:
    print("Usage: PDF_AI_Sum.py <language> <URL to PDF> <optional: filename>")
    sys.exit(1)
try:
    lang=sys.argv[1]
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
if(paperFilePath == None): sys.exit(1)

try:
    paperContent = pdfplumber.open(paperFilePath).pages
except Exception as e:
    print("Error opening PDF")
    print(e)
    sys.exit(1)

showPaperSummary(paperContent)