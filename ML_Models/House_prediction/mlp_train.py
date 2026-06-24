"""Train a feedforward neural network (MLP) using scikit-learn.

Uses a simple pipeline with StandardScaler and MLPRegressor.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def parse_args():
    parser = argparse.ArgumentParser(description="Train an MLP regressor on processed CSVs")
    parser.add_argument("--processed-dir", default="artifacts/processed", help="Directory with processed_train.csv")
    parser.add_argument("--target-column", default="SalePrice")
    parser.add_argument("--model-out", default="artifacts/mlp_model.joblib")
    return parser.parse_args()


def load_processed(processed_dir: Path, target_column: str):
    train = pd.read_csv(processed_dir / "processed_train.csv")
    test = pd.read_csv(processed_dir / "processed_test.csv")

    X_train = train.drop(columns=[target_column])
    y_train = train[target_column]
    X_test = test.drop(columns=[target_column])
    y_test = test[target_column]
    return X_train, X_test, y_train, y_test


def build_pipeline():
    mlp = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42, early_stopping=False)
    pipe = make_pipeline(StandardScaler(), mlp)
    return pipe


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)
    model_out = Path(args.model_out)

    X_train, X_test, y_train, y_test = load_processed(processed_dir, args.target_column)

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    rmse = float(mean_squared_error(y_test, preds) ** 0.5)
    print(f"Test RMSE: {rmse:.4f}")

    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, model_out)
    print(f"Saved MLP pipeline to: {model_out}")


if __name__ == "__main__":
    main()
