"""Preprocess Ames-style house dataset.

Reads `train.csv` and `test.csv` produced by the ingestion step (default
location: `artifacts/train.csv`), applies simple missing-value handling and
one-hot encoding for categoricals, and writes processed CSVs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess Ames house dataset CSVs.")
    parser.add_argument(
        "--input-dir",
        default="artifacts",
        help="Directory containing train.csv and test.csv created by ingestion",
    )
    parser.add_argument(
        "--target-column",
        default="SalePrice",
        help="Name of the target column",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/processed",
        help="Directory to write processed CSVs",
    )
    return parser.parse_args()


def load_splits(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_path = input_dir / "train.csv"
    test_path = input_dir / "test.csv"
    if not train_path.exists() or not test_path.exists():
        raise FileNotFoundError(f"train.csv and test.csv must exist in {input_dir}")

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test


def preprocess(train: pd.DataFrame, test: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = train.copy()
    test = test.copy()

    train_idx = len(train)

    combined = pd.concat([train, test], axis=0, ignore_index=True)

    # Separate numeric and categorical
    numeric_cols = combined.select_dtypes(include=["number"]).columns.tolist()
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)

    categorical_cols = combined.select_dtypes(include=["object", "category", "string"]).columns.tolist()

    # Fill numeric missing with train medians
    for col in numeric_cols:
        med = combined.loc[: train_idx - 1, col].median()
        combined[col] = combined[col].fillna(med)

    # Fill categorical missing with a placeholder
    for col in categorical_cols:
        combined[col] = combined[col].fillna("Missing")

    # One-hot encode categoricals (simple, may expand columns)
    combined = pd.get_dummies(combined, columns=categorical_cols, drop_first=False)

    # Split back
    processed_train = combined.iloc[:train_idx].reset_index(drop=True)
    processed_test = combined.iloc[train_idx:].reset_index(drop=True)

    # Ensure target column exists in processed splits
    if target_column not in processed_train.columns:
        raise KeyError(f"Target column '{target_column}' missing after preprocessing")

    return processed_train, processed_test


def save_processed(train: pd.DataFrame, test: pd.DataFrame, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "processed_train.csv"
    test_path = output_dir / "processed_test.csv"

    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    return train_path, test_path


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    train, test = load_splits(input_dir)
    proc_train, proc_test = preprocess(train, test, args.target_column)
    train_path, test_path = save_processed(proc_train, proc_test, output_dir)

    print(f"Processed train saved to: {train_path}")
    print(f"Processed test saved to: {test_path}")


if __name__ == "__main__":
    main()
