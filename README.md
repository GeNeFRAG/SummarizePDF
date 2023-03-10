<!DOCTYPE html>
<html>
<body>
<h1>Summary of PDF using OpenAI</h1>

<p>This script uses the OpenAI API to summarize a given PDF document. The script uses the <code>pdfplumber</code> and <code>wget</code> libraries to download and read the PDF, and the <code>openai</code> library to generate summaries.</p>

<h2>Requirements</h2>

<ul>
  <li>Python 3</li>
  <li>openai API key and organization</li>
  <li>pdfplumber</li>
  <li>wget</li>
  <li>tomli</li>
  <li>numpy</li>
</ul>

<h2>Usage</h2>

<p>To use the script, you need to provide the OpenAI API key and organization in the <code>openai.toml</code> file. The script takes three command line arguments:</p>
<ol>
  <li><code>maxtokens</code> : maximum number of tokens to be generated in the summary</li>
  <li><code>URL to PDF</code>: URL of the PDF that needs to be summarized</li>
  <li><code>filename (optional)</code>: Optional local filename under which the PDF is stored</li>
</ol>

<h2>Example</h2>
<pre>
<code>python PDF_AI_Sum.py 200 https://arxiv.org/pdf/1906.01185.pdf mypaper.pdf</code>
</pre>
<p>This will generate summary of the paper with 200 tokens</p>

<h2>Notes</h2>
<ul>
  <li>It will use the OpenAI's <code>text-davinci-003</code> model to generate summary</li>
  <li>The script uses default parameter value of temperature, max_tokens, top_p, frequency_penalty, presence_penalty and echo.</li>
</ul>

<h2>Limitations</h2>
<ul>
  <li>This script uses OpenAI API to generate summary which has usage limit based on the plan you have subscribed to.</li>
  <li>It will only work for PDF documents.</li>
</ul>
</body>
</html>