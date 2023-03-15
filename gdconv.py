import re
import sys
from urllib.parse import urlparse

# Getting Google Drive URL from cmd line
if len(sys.argv) == 1:
    print("Usage: SummarizePDFOpenAI <Google Drive URL>")
    sys.exit(1)
try:
    url=sys.argv[1]
except Exception as e:
    print("Error retrieving commandline arguments")
    #print(e)
    sys.exit(1)

# Parsing the URL
parsed_url = urlparse(url)
# Getting the path of the URL
path = parsed_url.path
# Extracting the file key from the path
file_key = (path.split("/"))[3]

# Constructing the new url for download
new_url = parsed_url.scheme + "://" + parsed_url.netloc + "/uc?export=download&id="  + file_key

# Escaping the new url
#new_url_e = re.escape(new_url)

#Printing the new url
print("Converted Google Drive URL")
print(new_url)