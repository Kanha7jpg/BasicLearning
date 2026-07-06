# House Prediction Project Status

This document summarizes how much of the House Prediction project is done and what should be built next.

## Estimated Completion

**About 75-80% complete**

The core data pipeline, model training, and one-command orchestration are already in place. What remains is mostly evaluation, polish, and project hardening.

## What Is Already Done

### Data Flow

- `download_ames.py` downloads the Ames Housing dataset from OpenML.
- `house_data_ingestion.py` reads a CSV and creates train/test splits.
- `preprocess_ames.py` handles missing values and one-hot encoding.
- `run_ames_pipeline.py` runs the full flow in one command.

### Models

- `xgb_train.py` trains XGBoost and supports randomized hyperparameter search.
- `mlp_train.py` trains a feedforward neural network using scikit-learn and also supports randomized hyperparameter search.

### Documentation and Setup

- `requirements.txt` lists the dependencies.
- `README.md` explains how to run each step and the full pipeline.

## What Still Needs Work

### High Priority

- Add a model comparison script for XGBoost vs MLP.
- Add a prediction script for inference on new rows.
- Save metrics and best parameters to a file such as JSON or CSV.
- Add feature importance plots or model explainability output.

### Medium Priority

- Add stronger data validation checks.
- Add a baseline model for comparison.
- Add residual/error analysis.
- Add automated tests for ingestion and preprocessing.

### Nice to Have

- Add a config file for search ranges and paths.
- Add a simple visualization dashboard or notebook.
- Add model versioning or timestamped artifact names.

## Best Next Step

The most useful next step is to add an **evaluation script** that:

- loads the trained XGBoost and MLP models,
- compares RMSE, MAE, and R²,
- saves the results to a file,
- and shows which model performs better on the Ames dataset.

## Suggested Roadmap

1. Build evaluation and comparison tooling.
2. Add inference for new house rows.
3. Save training metadata and metrics.
4. Add tests and cleanup for reliability.
