import re
import sys
from urllib.parse import urlparse

def get_arg(arg_name, default=None):
    """
    Safely reads a command line argument by name.
    :param arg_name: the name of the argument to read.
    :param default: the default value to return if the argument is not found.
    :return: the value of the argument if found, or the default value.
    """
    if "--help" in sys.argv:
        print("Usage: python gdconv.py [--help] [--gdurl]")
        print("Arguments:")
        print("\t--help\t\tHelp\t\tNone")
        print("\t--gdurl\t\tGoogle Drive URL\tNone")

        # Add more argument descriptions here as needed
        sys.exit(0)
    try:
        arg_value = sys.argv[sys.argv.index(arg_name) + 1]
        return arg_value
    except (IndexError, ValueError):
        return default

# Getting Google Drive URL from cmd line
# if len(sys.argv) == 1:
#     print("Usage: SummarizePDFOpenAI <Google Drive URL>")
#     sys.exit(1)
# try:
#     url=sys.argv[1]
# except Exception as e:
#     print("Error retrieving commandline arguments")
#     #print(e)
#     sys.exit(1)

url=get_arg('--gdurl')
if(url == None):
    print("Type “--help\" for more information.")
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