# Summarize PDFs using OpenAI Completion APIs.
This script uses the OpenAI Chat API to summarize a given PDF document.The script uses the pdfplumber library to extract text from the PDF and the OpenAPI Completion APIs to generate a summary.

# Requirements
* Python 3
* openai API key and organization
* pdfplumber
* wget
* tomli
* numpy
* GPTCommons (as submodule)

# Usage
To use this script, you need to provide the `--lang`, `--url` (download URL of the PDF), `--ofile` (PDF filename) as command line arguments.  
For example:  
`python PDF_AI_Sum.py --lang French --url https://arxiv.org/pdf/1906.01185.pdf --ofile mypaper.pdf`  
The script also requires an `openai.toml` file with the API key, organization details for the OpenAI API, model to be used and the maximum number of tokens per request.  
The config file should contain the following information:  
`[openai]`
- `apikey = "your_api_key"`
- `organization = "your_organization"`
- `model = "gtp-4"`
- `maxtokens = "1000"`

The script will then downlaid the PDF file, stores it locally, convert it to plain text and generate a summary using the OpenAI API. The summary will be printed to the console.
