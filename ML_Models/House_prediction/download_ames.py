"""Download the Ames Housing dataset from OpenML.

This script downloads the classic Ames Housing dataset, then saves it as a CSV
so the rest of the project can ingest, preprocess, and train models locally.

Example:
    python download_ames.py --output-csv artifacts/raw/ames_housing.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.datasets import fetch_openml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download the Ames Housing dataset from OpenML.")
    parser.add_argument(
        "--dataset-name",
        default="house_prices",
        help="OpenML dataset name (default: house_prices)",
    )
    parser.add_argument(
        "--output-csv",
        default="artifacts/raw/ames_housing.csv",
        help="Path where the downloaded CSV will be saved",
    )
    return parser.parse_args()


def download_ames_dataset(dataset_name: str) -> pd.DataFrame:
    try:
        dataset = fetch_openml(name=dataset_name, as_frame=True)
    except Exception as exc:  # pragma: no cover - network dependent
        raise RuntimeError(
            f"Failed to download OpenML dataset '{dataset_name}'. Check your internet connection and dataset name."
        ) from exc

    frame = dataset.frame
    if frame is None:
        frame = pd.concat([dataset.data, dataset.target.rename(dataset.target.name or "target")], axis=1)

    if frame.empty:
        raise ValueError(f"Downloaded dataset '{dataset_name}' is empty.")

    return frame


def main() -> None:
    args = parse_args()
    output_csv = Path(args.output_csv)

    print(f"Downloading '{args.dataset_name}' from OpenML...")
    dataset = download_ames_dataset(args.dataset_name)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(output_csv, index=False)

    print(f"Saved dataset to: {output_csv}")
    print(f"Rows: {len(dataset)} | Columns: {len(dataset.columns)}")


if __name__ == "__main__":
    main()