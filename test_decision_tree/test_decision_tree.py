import argparse
from pathlib import Path

import json

import joblib
from sklearn.pipeline import Pipeline


def load(scaler_path, model_path):
    sc = joblib.load(scaler_path)
    model = joblib.load(model_path)
    return sc, model

def _test_decision_tree(args):
    # Open and read file "data"
    print(args.TestData)
    with open(args.TestData) as data_file:
        data = json.load(data_file)

    # The expected data type is 'dict', however, since the file
    # was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get
    # the dict-type object.
    data = json.loads(data)

    x_test = data['x_test']
    y_test = data['y_test']

    model_path = Path(args.Model) / 'best_dt_model.joblib'
    scaler_path = Path(args.Scaler) / 'best_dt_scaler.joblib'
    print(model_path)
    print(scaler_path)
    sc, model = load(scaler_path, model_path)

    pipeline = Pipeline([('scaler', sc), ('model', model)])

    accuracy = pipeline.score(x_test,y_test)
    print("Test score: {:.3f}".format(accuracy))

    # Save output into file
    with open(args.AccuracyDT, 'w') as accuracy_decision_tree_file:
        accuracy_decision_tree_file.write(str(accuracy))
        
    model_path = Path(args.ModelDT) / 'best_DT_model.joblib'
    scaler_path = Path(args.ScalerDT) / 'best_DT_scaler.joblib'

    joblib.dump(model, model_path)
    joblib.dump(sc, scaler_path)


if __name__ == '__main__':
    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('TestData', type=str)
    parser.add_argument('Model', type=str)
    parser.add_argument('Scaler', type=str)
    parser.add_argument('AccuracyDT', type=str)
    parser.add_argument('ModelDT', type=str)
    parser.add_argument('ScalerDT', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.AccuracyDT).parent.mkdir(parents=True, exist_ok=True)

    model_path = Path(args.ModelDT) / 'best_DT_model.joblib'
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)

    scaler_path = Path(args.ScalerDT) / 'best_DT_scaler.joblib'
    Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)

    _test_decision_tree(args)




