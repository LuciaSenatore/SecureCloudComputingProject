import argparse
from pathlib import Path
import json
import joblib
from sklearn.pipeline import Pipeline

def _show_result(args):

    
    print(args.AccuracyLR, args.AccuracyDT)
    #read accuracy from file
    with open(args.AccuracyLR, 'r') as f:
        accuracyLR = f.read()
    with open(args.AccuracyDT, 'r') as f:
        accuracyDT = f.read()
    print(accuracyLR, accuracyDT)

    if float(accuracyLR) >= float(accuracyDT):

        # Create a dictionary to store details of the best model
        best_model_details = {
            "accuracy": args.AccuracyLR,
            "model_path": args.ModelLR,
            "scaler_path": args.ScalerLR
        }

        ''' # Save the best model details to a JSON file
        with open('best_model_details.json', 'w') as json_file:
            json.dump(best_model_details, json_file, indent=4)

        # Save the best model to a specific folder
        best_model_folder = Path('best_model')
        best_model_folder.mkdir(parents=True, exist_ok=True)

        # Copy or move the best model and scaler to the specified folder
        best_model_path = Path(args.ModelLR)
        best_scaler_path = Path(args.ScalerLR)

        best_model_path.rename(best_model_folder / best_model_path.name)
        best_scaler_path.rename(best_model_folder / best_scaler_path.name)

        # Load the best model and save it using joblib
        model = joblib.load(args.ModelLR)
        joblib.dump(model, best_model_folder / f"bestmodel{args.AccuracyLR}.joblib")

        scaler = joblib.load(args.ScalerLR)
        joblib.dump(scaler, best_model_folder / f"bestscaler{args.AccuracyLR}.joblib")'''

    else:
        # Create a dictionary to store details of the best model
        best_model_details = {
            "accuracy": args.AccuracyDT,
            "model_path": args.ModelDT,
            "scaler_path": args.ScalerDT
        }

    print("il miglior modello è: ")
    print(best_model_details)

    ''' # Save the best model details to a JSON file
    with open('best_model_details.json', 'w') as json_file:
        json.dump(best_model_details, json_file, indent=4)

    # Save the best model to a specific folder
    best_model_folder = Path('best_model')
    best_model_folder.mkdir(parents=True, exist_ok=True)

    # Copy or move the best model and scaler to the specified folder
    best_model_path = Path(args.ModelDT)
    best_scaler_path = Path(args.ScalerDT)

    best_model_path.rename(best_model_folder / best_model_path.name)
    best_scaler_path.rename(best_model_folder / best_scaler_path.name)

    # Load the best model and save it using joblib
    model = joblib.load(args.ModelDT)
    joblib.dump(model, best_model_folder / f"bestmodel{args.AccuracyDT}.joblib")
    scaler = joblib.load(args.ScalerDT)
    joblib.dump(scaler, best_model_folder / f"bestscaler{args.AccuracyDT}.joblib")'''



if __name__ == '__main__':
    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('AccuracyLR', type=str)
    parser.add_argument('ModelLR', type=str)
    parser.add_argument('ScalerLR', type=str)
    parser.add_argument('AccuracyDT', type=str)
    parser.add_argument('ModelDT', type=str)
    parser.add_argument('ScalerDT', type=str)

    args = parser.parse_args()

    _show_result(args)

