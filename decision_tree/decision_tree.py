import argparse
from pathlib import Path
import json
import joblib
from scipy.sparse import issparse
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

def _decision_tree(args):

    # Open and read file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)

    # The expected data type is 'dict', however, since the file
    # was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get
    # the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_validation = data['x_validation']
    y_validation = data['y_validation']

    
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.1)

    
    data = {'x_test': x_test,
            'y_test': y_test }

    # Creates a json object based on `data`
    data_json = json.dumps(data)
    print(data_json)
    print("Saving data to file...")
    # Saves the json object into a file
    with open(args.TestData, 'w') as out_file:
        json.dump(data_json, out_file)


    # Initialize and train the model
    model = DecisionTreeClassifier(max_depth=3)

    # Define parameter grid for grid search
    param_grid = {
        'model__max_depth': [3, 5, 7, 10],
        'model__min_samples_split': [2, 5, 10],
        'model__min_samples_leaf': [1, 2, 4]
    }

    # Initialize StandardScaler
    scaler = StandardScaler(with_mean=not issparse(x_train))

    # Create a pipeline with the scaler and the model
    pipeline = Pipeline([('scaler', scaler), ('model', model)])

    best_score = float('-inf')
    best_params = None

    for max_depth in param_grid['model__max_depth']:
        for min_samples_split in param_grid['model__min_samples_split']:
            for min_samples_leaf in param_grid['model__min_samples_leaf']:
                # Set parameters and create model
                model.set_params(max_depth=max_depth, min_samples_split=min_samples_split,
                                    min_samples_leaf=min_samples_leaf)
                # Fit the model on training set
                pipeline.fit(x_train, y_train)

                # Evaluate on validation set
                val_score = pipeline.score(x_validation, y_validation)

                print("Validation score: {:.3f}".format(val_score))
                # Check if this is the best model so far
                if val_score > best_score:
                    best_score = val_score
                    best_params = {'max_depth': max_depth, 'min_samples_split': min_samples_split,
                                    'min_samples_leaf': min_samples_leaf}

    # Print the best parameters
    print("Best Parameters:", best_params)
    # Save the best model
    best_model = model.set_params(**best_params)
    model_path = Path(args.model) / 'best_dt_model.joblib'
    print("Saving model to: {}".format(model_path))
    joblib.dump(best_model, model_path)

    # Save the scaler
    best_scaler = scaler
    best_scaler.fit(x_train)
    scaler_path = Path(args.scaler) / 'best_dt_scaler.joblib'
    joblib.dump(best_scaler, scaler_path)





if __name__ == '__main__':
    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--data', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--scaler', type=str)
    parser.add_argument('TestData', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created (the directory may or may not exist).
    model_path = Path(args.model) / 'best_dt_model.joblib'
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    #print the path of the new directory
    scaler_path = Path(args.scaler) / 'best_dt_scaler.joblib'
    Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)
    
    #path of the new directory
    Path(args.TestData).parent.mkdir(parents=True, exist_ok=True)

    _decision_tree(args)