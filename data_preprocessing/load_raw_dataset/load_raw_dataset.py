import argparse
from pathlib import Path
import pandas as pd
import json


def _load_data(args):
    data = pd.read_csv('malicious_phish.csv')

    data['url'] = data['url'].replace('www.', '', regex=True)

    rem = {"Category": {"benign": 0, "defacement": 1, "phishing":1, "malware":1}}
    data['Category'] = data['type']
    data = data.replace(rem)

    print(data)
    
    data.drop(['type'], axis=1, inplace=True)
    
    #creates a csv structure with the data
    data.to_csv(args.data, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    # Chiamata alla funzione di download dei dati con il percorso del file CSV come argomento
    _load_data(args)