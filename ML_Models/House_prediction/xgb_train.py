"""Train an XGBoost regressor (falls back to sklearn if xgboost not installed).

Trains on processed CSVs created by `preprocess_ames.py` and saves the model.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error


def parse_args():
    parser = argparse.ArgumentParser(description="Train XGBoost or fallback regressor")
    parser.add_argument("--processed-dir", default="artifacts/processed", help="Directory with processed_train.csv")
    parser.add_argument("--target-column", default="SalePrice")
    parser.add_argument("--model-out", default="artifacts/xgb_model.joblib")
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


def build_search_space():
    try:
        from xgboost import XGBRegressor

        model = XGBRegressor(random_state=42, verbosity=0)
        param_distributions = {
            "n_estimators": [100, 200, 400, 600],
            "max_depth": [3, 4, 5, 6, 8],
            "learning_rate": [0.01, 0.03, 0.05, 0.1],
            "subsample": [0.7, 0.85, 1.0],
            "colsample_bytree": [0.7, 0.85, 1.0],
            "min_child_weight": [1, 3, 5],
            "reg_alpha": [0.0, 0.1, 1.0],
            "reg_lambda": [1.0, 2.0, 5.0],
        }
        print("Using xgboost.XGBRegressor with randomized search")
    except Exception:
        from sklearn.ensemble import HistGradientBoostingRegressor

        model = HistGradientBoostingRegressor(random_state=42)
        param_distributions = {
            "max_depth": [None, 3, 5, 7, 9],
            "learning_rate": [0.01, 0.03, 0.05, 0.1],
            "max_leaf_nodes": [15, 31, 63, 127],
            "min_samples_leaf": [10, 20, 30, 40],
        }
        print("xgboost not available — using sklearn.HistGradientBoostingRegressor search space")

    return model, param_distributions


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)
    model_out = Path(args.model_out)

    X_train, X_test, y_train, y_test = load_processed(processed_dir, args.target_column)

    if not model_out.is_absolute():
        model_out = processed_dir.parent / model_out

    if args.search:
        model, param_distributions = build_search_space()
        cv = min(args.cv, len(y_train))
        if cv < 2:
            raise ValueError("Need at least 2 training rows for hyperparameter search.")

        search = RandomizedSearchCV(
            model,
            param_distributions=param_distributions,
            n_iter=args.n_iter,
            scoring="neg_mean_squared_error",
            cv=cv,
            random_state=42,
            n_jobs=-1,
            verbose=1,
        )
        search.fit(X_train, y_train)
        model = search.best_estimator_
        print(f"Best CV score: {search.best_score_:.6f}")
        print(f"Best params: {search.best_params_}")
    else:
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
