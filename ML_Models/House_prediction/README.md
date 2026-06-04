# House Prediction Data Ingestion

This folder contains a basic beginner-friendly data ingestion script for a house price prediction project.

The script:

- reads a CSV dataset
- checks that the target column exists
- splits the data into train and test sets
- saves the results as CSV files inside an output folder

## Files

- `house_data_ingestion.py` - main ingestion script
- `requirements.txt` - Python dependencies

## Setup

Install the dependencies first:

```bash
pip install -r requirements.txt
```

## Run

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

## Notes

- The default target column is `SalePrice`, which works well for common house-price datasets.
- If your dataset uses another name, pass it explicitly with `--target-column`.