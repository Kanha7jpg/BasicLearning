# House Prediction Data Ingestion

This folder contains a basic beginner-friendly data ingestion script for a house price prediction project.

The script:

- reads a CSV dataset
- checks that the target column exists
- splits the data into train and test sets
- saves the results as CSV files inside an output folder

## Files

- `house_data_ingestion.py` - main ingestion script
- `download_ames.py` - automatic Ames Housing downloader from OpenML
- `preprocess_ames.py` - preprocessing for the ingested dataset
- `xgb_train.py` - XGBoost training and optional search
- `mlp_train.py` - MLP training and optional search
- `run_ames_pipeline.py` - one-command wrapper for the full workflow
- `requirements.txt` - Python dependencies

## Setup

Install the dependencies first:

```bash
pip install -r requirements.txt
```

## Run

Download the Ames dataset automatically from OpenML:

```bash
python download_ames.py --output-csv artifacts/raw/ames_housing.csv
```

Then ingest the downloaded CSV:

```bash
python house_data_ingestion.py --input-csv artifacts/raw/ames_housing.csv --target-column SalePrice --output-dir artifacts
```

Use your own house dataset CSV and point the script to the target column you want to predict.

```bash
python house_data_ingestion.py --input-csv path\to\house_data.csv --target-column SalePrice
```

If your dataset uses a different target name, change `--target-column`:

```bash
python house_data_ingestion.py --input-csv path\to\house_data.csv --target-column price
```

## Output

By default, the script creates an `artifacts` folder and writes:

- `train.csv`
- `test.csv`

## Ames-specific preprocessing and training

After running the ingestion, preprocess the splits for Ames and train models:

```bash
# Preprocess the ingested splits (creates artifacts/processed/processed_*.csv)
python preprocess_ames.py --input-dir artifacts --target-column SalePrice

# Train XGBoost (falls back to sklearn if xgboost is not installed)
python xgb_train.py --processed-dir artifacts/processed --target-column SalePrice

# Train an MLP (scikit-learn)
python mlp_train.py --processed-dir artifacts/processed --target-column SalePrice

# Optional: randomized hyperparameter search for XGBoost
python xgb_train.py --processed-dir artifacts/processed --target-column SalePrice --search

# Optional: randomized hyperparameter search for the MLP
python mlp_train.py --processed-dir artifacts/processed --target-column SalePrice --search
```

Models are saved under `artifacts/` by default:

- `artifacts/xgb_model.joblib`
- `artifacts/mlp_model.joblib`

If you run search mode, the same files are overwritten with the best estimator found.

## One-command workflow

Run the full pipeline from download to training in one command:

```bash
python run_ames_pipeline.py --search --model both
```

To use a local CSV instead of downloading from OpenML:

```bash
python run_ames_pipeline.py --input-csv path\to\ames.csv --search --model both
```

Useful options:

- `--model xgb` to train only XGBoost
- `--model mlp` to train only the MLP
- `--n-iter 50` to try more search candidates
- `--cv 5` to use 5-fold search validation

## Notes

- The default target column is `SalePrice`, which works well for common house-price datasets.
- If your dataset uses another name, pass it explicitly with `--target-column`.