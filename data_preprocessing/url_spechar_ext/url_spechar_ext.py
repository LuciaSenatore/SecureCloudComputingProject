import argparse
from pathlib import Path
import json
import pandas as pd


def _url_spechar_ext(args):

    print("reading data")
    # Open and reads file "data"
    data = pd.read_csv(args.DataIn)

    feature = ['@','?','-','=','.','#','%','+','$','!','*',',','//']
    
    print("checking special characters")
    for i in feature:
        data[i] = data['url'].apply(lambda x: x.count(i))

    print("saving data")
    data.to_csv(args.DataOut)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('DataIn', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    _url_spechar_ext(args)