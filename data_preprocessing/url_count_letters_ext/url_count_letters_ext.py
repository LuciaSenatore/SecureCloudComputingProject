import argparse
import json
from pathlib import Path
import pandas as pd


def _url_count_letters_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)

    def letters_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    
    print("counting letters")
    data['letters'] = data['url'].apply(lambda x: letters_count(x))

    print("saving data")
    data.to_csv(args.DataOut)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_count_letters_ext(args)