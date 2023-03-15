<!DOCTYPE html>
<html>
<body>
<h1>Summary of PDF using OpenAI</h1>

<p>This script uses the OpenAI Chat API to summarize a given PDF document using the GPT-3.5 model. The script uses the <code>pdfplumber</code> and <code>wget</code> libraries to download and read the PDF, and the <code>openai</code> library to generate summaries.</p>

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
  <li><code>Language</code> : Language of the Chat API response</li>
  <li><code>URL to PDF</code>: URL of the PDF that needs to be summarized</li>
  <li><code>filename (optional)</code>: Optional local filename under which the PDF is stored</li>
</ol>

<h2>Example</h2>
<pre>
<code>python PDF_AI_Sum.py French https://arxiv.org/pdf/1906.01185.pdf mypaper.pdf</code>
</pre>
<p>This will generate a French summary of the paper</p>

<h2>Notes</h2>
<ul>
  <li>It will use the OpenAI's <code>gpt-3.5-turbo</code> model to generate summary</li>
</ul>

<h2>Limitations</h2>
<ul>
  <li>This script uses OpenAI API to generate summary which has usage limit based on the plan you have subscribed to.</li>
  <li>It will only work for PDF documents.</li>
</ul>
</body>
</html>
