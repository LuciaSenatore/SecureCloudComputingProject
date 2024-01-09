import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd


def _url_https_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)

    def httpSecure(url):
        htp = urlparse(url).scheme
        match = str(htp)
        if match=='https':
            return 1
        else:
            return 0
    
    print("checking if url has https")
    data['https'] = data['url'].apply(lambda x: httpSecure(x))
        
    
    print("saving data")
    data.to_csv(args.DataOut)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_https_ext(args)