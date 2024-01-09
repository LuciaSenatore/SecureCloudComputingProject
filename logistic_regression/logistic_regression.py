import argparse
from pathlib import Path
import json
import joblib
from scipy.sparse import issparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def _logistic_regression(args):
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
            'y_test': y_test}

    # Creates a json object based on `data`
    data_json = json.dumps(data)
    print(data_json)
    print("Saving data to file...")
    # Saves the json object into a file
    with open(args.TestData, 'w') as out_file:
        json.dump(data_json, out_file)


    # Initialize and train the model
    model = LogisticRegression(C=1, penalty='l2')  # You can set your preferred hyperparameters here

    # Initialize StandardScaler
    scaler = StandardScaler(with_mean=not issparse(x_train))

    # Create a pipeline with the scaler and the model
    pipeline = Pipeline([('scaler', scaler), ('model', model)])

    best_score = float('-inf')
    best_params = None

    # Define parameter grid for manual search
    param_grid = {
        'model__C': [0.001, 0.01, 0.1, 1, 10, 100],
        'model__l1_ratio': ['l1','l2']
    }

    for C in param_grid['model__C']:
        for penalty in param_grid['model__l1_ratio']:
            # Set parameters and create model
            model.set_params(C=C, penalty=penalty, solver='liblinear',max_iter=10000)

            # Fit the model on training set
            pipeline.fit(x_train, y_train)

            # Evaluate on validation set
            val_score = pipeline.score(x_validation, y_validation)
            print("Validation score: {:.3f}".format(val_score))
            # Check if this is the best model so far
            if val_score > best_score:
                best_score = val_score
                best_params = {'C': C, 'penalty': penalty}

    # Print the best parameters
    print("Best Parameters:", best_params)

    # Save the best model
    model.set_params(**best_params)
    model.fit(x_train, y_train)  # Fit on the entire training set
    best_model = model
    model_path = Path(args.model) / 'best_lr_model.joblib'
    print("Saving model to: {}".format(model_path))
    joblib.dump(best_model, model_path)

    # Save the scaler
    scaler.fit(x_train)  # Fit on the entire training set
    scaler_path = Path(args.scaler) / 'best_lr_scaler.joblib'
    joblib.dump(scaler, scaler_path)



if __name__ == '__main__':
    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--data', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--scaler', type=str)
    parser.add_argument('TestData', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created (the directory may or may not exist).
    model_path = Path(args.model) / 'best_lr_model.joblib'
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    #print the path of the new directory
    scaler_path = Path(args.scaler) / 'best_lr_scaler.joblib'
    Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)
    
    #path of the new directory
    Path(args.TestData).parent.mkdir(parents=True, exist_ok=True)

    _logistic_regression(args)