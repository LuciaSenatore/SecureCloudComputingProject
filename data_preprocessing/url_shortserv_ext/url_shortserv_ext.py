import argparse
from pathlib import Path
import json
import re
import pandas as pd


def _url_shortserv_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)
    
    def Shortining_Service(url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        url)
        if match:
            return 1
        else:
            return 0

    print("checking if url has shortening service")
    data['Shortining_Service'] = data['url'].apply(lambda x: Shortining_Service(x))

    print("saving data")
    data.to_csv(args.DataOut)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_shortserv_ext(args)