import argparse
import json
from pathlib import Path
import pandas as pd


def _url_len_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)

    print("counting url length")
    data['url_len'] = data['url'].apply(lambda x: len(x))

    print("saving data")
    data.to_csv(args.DataOut)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()
    
    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_len_ext(args)