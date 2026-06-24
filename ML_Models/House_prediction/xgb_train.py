"""Train an XGBoost regressor (falls back to sklearn if xgboost not installed).

Trains on processed CSVs created by `preprocess_ames.py` and saves the model.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def parse_args():
    parser = argparse.ArgumentParser(description="Train XGBoost or fallback regressor")
    parser.add_argument("--processed-dir", default="artifacts/processed", help="Directory with processed_train.csv")
    parser.add_argument("--target-column", default="SalePrice")
    parser.add_argument("--model-out", default="artifacts/xgb_model.joblib")
    return parser.parse_args()


def load_processed(processed_dir: Path, target_column: str):
    train = pd.read_csv(processed_dir / "processed_train.csv")
    test = pd.read_csv(processed_dir / "processed_test.csv")

    X_train = train.drop(columns=[target_column])
    y_train = train[target_column]
    X_test = test.drop(columns=[target_column])
    y_test = test[target_column]
    return X_train, X_test, y_train, y_test


def build_model():
    try:
        from xgboost import XGBRegressor

        model = XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
        print("Using xgboost.XGBRegressor")
    except Exception:
        from sklearn.ensemble import HistGradientBoostingRegressor

        model = HistGradientBoostingRegressor(max_iter=100, random_state=42)
        print("xgboost not available — using sklearn.HistGradientBoostingRegressor as fallback")
    return model


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)
    model_out = Path(args.model_out)

    X_train, X_test, y_train, y_test = load_processed(processed_dir, args.target_column)

    model = build_model()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    print(f"Test RMSE: {rmse:.4f}")

    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_out)
    print(f"Saved model to: {model_out}")


if __name__ == "__main__":
    main()
