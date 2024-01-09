import argparse
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import json
from sklearn.feature_extraction.text import CountVectorizer

def _load_data(args):

    # List of JSON file paths
    csv_files = [
        args.DataCD, args.DataCS, args.DataIP,
        args.DataSS, args.DataCL, args.DataHN,
        args.DataHTTPS, args.DataLen
    ]

    print(csv_files)
    # Inizializza un DataFrame vuoto
    merged_data = pd.DataFrame()

    # Loop attraverso i file e unisci i dati
    for csv_file in csv_files:
        # Carica il file CSV in un DataFrame
        df = pd.read_csv(csv_file)
        print(df['url'])
        # Unisci i dati al DataFrame principale
        merged_data = pd.concat([merged_data, df],axis=1)
    
    merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

    print(merged_data.columns)
    X = merged_data.drop(['url', 'Category', 'Unnamed: 0'], axis=1)
    y = merged_data['Category']


    print(X)
    print(y)

    # Split data into train and test sets
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    # Creates `data` structure to save and
    # share train and test datasets.
    data = {'x_train': x_train.values.tolist(),
            'y_train': y_train.values.tolist(),
            'x_validation': x_val.values.tolist(),
            'y_validation': y_val.values.tolist()}

    # Creates a json object based on `data`
    data_json = json.dumps(data)
    print(data_json)
    print("Saving data to file...")
    # Saves the json object into a file
    with open(args.DataOut, 'w') as out_file:
        json.dump(data_json, out_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('DataCD', type=str)
    parser.add_argument('DataCS', type=str)
    parser.add_argument('DataIP', type=str)
    parser.add_argument('DataSS', type=str)
    parser.add_argument('DataCL', type=str)
    parser.add_argument('DataHN', type=str)
    parser.add_argument('DataHTTPS', type=str)
    parser.add_argument('DataLen', type=str)
    parser.add_argument('DataOut', type=str)

    args = parser.parse_args()

    # Creazione della directory in cui verrà creato il file di output
    Path(args.DataOut).parent.mkdir(parents=True, exist_ok=True)

    # Chiamata alla funzione di download dei dati con il percorso del file CSV come argomento
    _load_data(args)