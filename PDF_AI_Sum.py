import pathlib
import sys

import pdfplumber
import wget
from GPTCommons import GPTCommons

def download_paper(paper_url, filename):
    """
    Downloads a paper from the provided URL and saves it with the specified filename.

    Args:
    paper_url (str): The URL of the paper to be downloaded.
    filename (str): The desired filename to save the paper as.

    Returns:
    pathlib.Path or None: The path to the downloaded paper file as a pathlib.Path object, or None if the download fails.

    Example:
    >>> paper_url = "https://example.com/paper.pdf"
    >>> downloaded_paper = download_paper(paper_url, "research_paper.pdf")
    >>> print(downloaded_paper)
    '/path/to/research_paper.pdf'

    Note:
    This function uses the 'wget' library to download the paper from the URL. If the download fails, it returns None.
    """
    try:
        # Download the paper from the provided URL, with the provided filename
        print(f"Downloading paper from URL: {paper_url}")
        downloadedPaper = wget.download(paper_url, filename)
        print(f"\nDownload complete. Saved as: {filename}")
        # Convert the downloaded paper path to a pathlib.Path object
        downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    except Exception as e:
        # Print error message if download fails
        print(f"Error: Unable to download paper from provided URL.")
        print(f"{e}")
        return None

    return downloadedPaperFilePath

def show_page_summary(paperContent, output_file=None):
    """
    Generates a summary of a PDF document's pages, removes duplicate or redundant information, and prints the result.
    If an output file is specified, writes the summary to the file instead of printing it.

    Args:
    paperContent (list): A list of pages from the PDF document.
    output_file (str, optional): The path to the file where the summary should be written. Defaults to None.

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
        print("No content found in the PDF to summarize.")
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:" 
        responses = ""
        print(f"Summarizing PDF using OpenAI completion API with model {commons.get_gptmodel()}...")
        for page in paperContent:   
            text = page.extract_text(layout=True) + tldr_tag
            text = commons.clean_text(text)
            prompt = f"""Summarize the following PDF text in an analytical style. Reply in {lang}. Text: ```{text}```"""
            
            # Call the OpenAI API to generate summary
            response = commons.get_chat_completion(prompt)
            responses = responses + response
        
        responses = commons.clean_text(responses)

        # Reduce the text to the maximum number of tokens
        print("Reducing the text to the maximum number of tokens...")
        
        responses = commons.reduce_to_max_tokens(responses)
        print(f"Removing duplicate or redundant information using OpenAI completion API with model {commons.get_gptmodel()}...") 
        prompt = f"""Remove duplicate or redundant information from the text below, keeping the tone consistent. Provide the answer in at most 5 bullet points, with smooth transitions between each point, and a maximum of 500 words.
                    Text: ```{responses}```"""
        response = commons.get_chat_completion(prompt)
        
        if output_file:
            print(f"Writing summary to output file: {output_file}")
            with open(output_file, 'w') as f:
                f.write(response)
            print("Summary written to file successfully.")
        else:
            print("Summary generation complete. Here is the summarized text:")
            print(response)
    except Exception as e:
        print(f"Error: Unable to generate summary for the paper.")
        print(f"{e}")
        return None
    
# Initialize GPT utilities module
print("Initializing GPTCommons utility class...")
commons = GPTCommons.initialize_gpt_commons("openai.toml")

arg_descriptions = {
    "--help": "Help",
    "--lang": "Language (default: English)",
    "--url": "URL",
    "--ofile": "Output file name",
    "--output": "Output file for summary"
}

# Getting max_tokens, PDF URL, local filename, and output file from command line
print("Retrieving command-line arguments...")
lang = commons.get_arg('--lang', arg_descriptions, 'English')
url = commons.get_arg('--url', arg_descriptions, None)
ofile = commons.get_arg('--ofile', arg_descriptions, 'random_paper.pdf')
output_file = commons.get_arg('--output', arg_descriptions, None)

if url is None:
    print("Error: URL not provided. Type '--help' for more information.")
    sys.exit(1)

print(f"Downloading PDF from URL: {url}")
paperFilePath = download_paper(url, ofile)

if paperFilePath is None:
    print("Error: Failed to download the PDF.")
    sys.exit(1)

try:
    print(f"Opening downloaded PDF: {paperFilePath}")
    pdf = pdfplumber.open(paperFilePath)
    paperContent = pdf.pages
    print("PDF opened successfully.")
except Exception as e:
    print("Error: Unable to open the PDF.")
    print(f"{e}")
    sys.exit(1)

print("Generating summary for the PDF content...")
show_page_summary(paperContent, output_file)
pdf.close()