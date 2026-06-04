"""Basic house-price data ingestion.

This script reads a CSV file, validates the target column, splits the data into
train and test sets, and saves the results to an output folder.

Example:
    python house_data_ingestion.py --input-csv data\\housing.csv --target-column SalePrice
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class IngestionConfig:
    input_csv: Path
    target_column: str
    output_dir: Path
    test_size: float
    random_state: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest a house price dataset and create train/test CSV files.",
    )
    parser.add_argument("--input-csv", required=True, help="Path to the source CSV file")
    parser.add_argument(
        "--target-column",
        default="SalePrice",
        help="Name of the target column to predict",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts",
        help="Directory where train/test files will be written",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of rows to reserve for testing",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed used for the split",
    )
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> IngestionConfig:
    return IngestionConfig(
        input_csv=Path(args.input_csv),
        target_column=args.target_column,
        output_dir=Path(args.output_dir),
        test_size=args.test_size,
        random_state=args.random_state,
    )


def load_dataset(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    data = pd.read_csv(csv_path)
    if data.empty:
        raise ValueError(f"The dataset at {csv_path} is empty.")

    return data


def split_dataset(data: pd.DataFrame, target_column: str, test_size: float, random_state: int):
    if target_column not in data.columns:
        available_columns = ", ".join(data.columns.astype(str))
        raise KeyError(
            f"Target column '{target_column}' was not found. Available columns: {available_columns}"
        )

    features = data.drop(columns=[target_column])
    target = data[target_column]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
    )

    train_data = x_train.copy()
    train_data[target_column] = y_train.values

    test_data = x_test.copy()
    test_data[target_column] = y_test.values

    return train_data, test_data


def save_splits(train_data: pd.DataFrame, test_data: pd.DataFrame, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"

    train_data.to_csv(train_path, index=False)
    test_data.to_csv(test_path, index=False)

    return train_path, test_path


def main() -> None:
    args = parse_args()
    config = build_config(args)

    print(f"Loading dataset from: {config.input_csv}")
    data = load_dataset(config.input_csv)
    print(f"Loaded {len(data)} rows and {len(data.columns)} columns.")

    train_data, test_data = split_dataset(
        data=data,
        target_column=config.target_column,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    train_path, test_path = save_splits(train_data, test_data, config.output_dir)

    print(f"Saved train split to: {train_path}")
    print(f"Saved test split to: {test_path}")
    print(f"Train shape: {train_data.shape}")
    print(f"Test shape: {test_data.shape}")


if __name__ == "__main__":
    main()