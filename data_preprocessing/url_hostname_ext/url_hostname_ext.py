import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlparse

import pandas as pd


def _url_hostname_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)
    
    def has_hostname(url):
        hostname = urlparse(url).hostname
        hostname = str(hostname)
        match = re.search(hostname, url)
        print(hostname)
        if match:
            return 1
        else:
            return 0
        
    print("checking host name")
    data['has_hostname'] = data['url'].apply(lambda x: has_hostname(x))

    print("saving data")
    # Saves the json object into a file
    data.to_csv(args.DataOut)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_hostname_ext(args)