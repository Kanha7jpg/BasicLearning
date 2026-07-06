
"""Train a feedforward neural network (MLP) using scikit-learn.

Uses a simple pipeline with StandardScaler and MLPRegressor.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def parse_args():
    parser = argparse.ArgumentParser(description="Train an MLP regressor on processed CSVs")
    parser.add_argument("--processed-dir", default="artifacts/processed", help="Directory with processed_train.csv")
    parser.add_argument("--target-column", default="SalePrice")
    parser.add_argument("--model-out", default="artifacts/mlp_model.joblib")
    parser.add_argument("--search", action="store_true", help="Run randomized hyperparameter search before training")
    parser.add_argument("--n-iter", type=int, default=20, help="Number of hyperparameter combinations to sample")
    parser.add_argument("--cv", type=int, default=3, help="Number of cross-validation folds")
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


def build_search_space():
    pipe = make_pipeline(
        StandardScaler(),
        MLPRegressor(max_iter=1000, random_state=42, early_stopping=False),
    )
    param_distributions = {
        "mlpregressor__hidden_layer_sizes": [(64, 32), (100, 50), (128, 64), (128, 64, 32)],
        "mlpregressor__activation": ["relu", "tanh"],
        "mlpregressor__alpha": [1e-5, 1e-4, 1e-3, 1e-2],
        "mlpregressor__learning_rate_init": [1e-4, 5e-4, 1e-3, 5e-3],
        "mlpregressor__solver": ["adam"],
    }
    return pipe, param_distributions


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)
    model_out = Path(args.model_out)

    X_train, X_test, y_train, y_test = load_processed(processed_dir, args.target_column)

    if not model_out.is_absolute():
        model_out = processed_dir.parent / model_out

    if args.search:
        pipe, param_distributions = build_search_space()
        cv = min(args.cv, len(y_train))
        if cv < 2:
            raise ValueError("Need at least 2 training rows for hyperparameter search.")

        search = RandomizedSearchCV(
            pipe,
            param_distributions=param_distributions,
            n_iter=args.n_iter,
            scoring="neg_mean_squared_error",
            cv=cv,
            random_state=42,
            n_jobs=-1,
            verbose=1,
        )
        search.fit(X_train, y_train)
        pipe = search.best_estimator_
        print(f"Best CV score: {search.best_score_:.6f}")
        print(f"Best params: {search.best_params_}")
    else:
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
