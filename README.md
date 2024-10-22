# Summarize PDFs using OpenAI Completion APIs.

This script summarizes the text content of a webpage using the OpenAI Completion API.

# Requirements

* Python 3
* pdfplumber
* wget
* openai
* tomli
* tiktoken
* GPTCommons (a custom utility module)

### Usage

To use this script, provide the following command-line arguments:

### Arguments

- `--url`: PDF URL.
- `--ofile`: (Optional) Filename of the downloaded PDF (default: random_paper.pdf)
- `--lang`: (Optional) Language of the summary (default: English).
- `--output`: (Optional) Output file name (default: STDOUT).
- `--html`: (Optional) Convert output to HTML (default: False).
- `--detail_level`: (Optional) Detail level of the summary (default: analytical).
- `--max_words`: (Optional) Maximum number of words for the summary (default: 200).

## OpenAI Configuration

The script requires an `openai.toml` file with API key, organization details, model, and maximum tokens per request. The config file should have the following format:

`[openai]`
- `apikey = "your_api_key"`
- `organization = "your_organization"`
- `model = "gpt-4"`
- `maxtokens = "1000"`

### Example

`$ python PDF_AI_Sum.py --lang English --url https://www.yourpdf.com/yourpdf.pdf --ofile mypdf.pdf --output yourfile.html --html True --detail_level high --max_words 500`