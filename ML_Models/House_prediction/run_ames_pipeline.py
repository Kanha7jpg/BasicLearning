"""Run the full Ames Housing workflow in one command.

The wrapper can either download the Ames dataset from OpenML or use a local
CSV, then runs ingestion, preprocessing, and training for XGBoost and/or MLP.

Example:
    python run_ames_pipeline.py --search
    python run_ames_pipeline.py --model both --search
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Ames Housing pipeline end to end.")
    parser.add_argument(
        "--input-csv",
        default="",
        help="Optional local CSV to use instead of downloading from OpenML",
    )
    parser.add_argument(
        "--dataset-name",
        default="house_prices",
        help="OpenML dataset name to download when --input-csv is not provided",
    )
    parser.add_argument(
        "--target-column",
        default="SalePrice",
        help="Name of the target column",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts",
        help="Working directory for raw, ingested, processed, and model artifacts",
    )
    parser.add_argument(
        "--model",
        choices=["xgb", "mlp", "both"],
        default="both",
        help="Which model(s) to train after preprocessing",
    )
    parser.add_argument(
        "--search",
        action="store_true",
        help="Run randomized hyperparameter search before training",
    )
    parser.add_argument("--n-iter", type=int, default=20, help="Number of hyperparameter samples")
    parser.add_argument("--cv", type=int, default=3, help="Cross-validation folds for search")
    return parser.parse_args()


def run_step(command: list[str]) -> None:
    print("\n$ " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    args = parse_args()
    project_dir = Path(__file__).resolve().parent
    python_executable = sys.executable

    output_dir = Path(args.output_dir).resolve()
    raw_dir = output_dir / "raw"
    processed_dir = output_dir / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if args.input_csv:
        source_csv = Path(args.input_csv)
    else:
        source_csv = raw_dir / "ames_housing.csv"
        download_script = project_dir / "download_ames.py"
        run_step(
            [
                python_executable,
                str(download_script),
                "--dataset-name",
                args.dataset_name,
                "--output-csv",
                str(source_csv),
            ]
        )

    ingestion_script = project_dir / "house_data_ingestion.py"
    preprocess_script = project_dir / "preprocess_ames.py"
    xgb_script = project_dir / "xgb_train.py"
    mlp_script = project_dir / "mlp_train.py"

    run_step(
        [
            python_executable,
            str(ingestion_script),
            "--input-csv",
            str(source_csv),
            "--target-column",
            args.target_column,
            "--output-dir",
            str(output_dir),
        ]
    )

    run_step(
        [
            python_executable,
            str(preprocess_script),
            "--input-dir",
            str(output_dir),
            "--target-column",
            args.target_column,
            "--output-dir",
            str(processed_dir),
        ]
    )

    common_training_args = [
        "--processed-dir",
        str(processed_dir),
        "--target-column",
        args.target_column,
    ]
    if args.search:
        common_training_args += ["--search", "--n-iter", str(args.n_iter), "--cv", str(args.cv)]

    if args.model in {"xgb", "both"}:
        run_step([
            python_executable,
            str(xgb_script),
            *common_training_args,
            "--model-out",
            str((output_dir / "xgb_model.joblib").resolve()),
        ])

    if args.model in {"mlp", "both"}:
        run_step([
            python_executable,
            str(mlp_script),
            *common_training_args,
            "--model-out",
            str((output_dir / "mlp_model.joblib").resolve()),
        ])


if __name__ == "__main__":
    main()