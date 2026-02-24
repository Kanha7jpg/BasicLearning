import argparse
import os
import warnings
from typing import List, Optional

import fastf1
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

warnings.filterwarnings("ignore", category=UserWarning)

TRAIN_START_YEAR = 2025
TRAIN_END_YEAR = 2025
PREDICT_YEAR = 2026


def _find_race_round(year: int, race_name: str) -> Optional[int]:
    schedule = fastf1.get_event_schedule(year, include_testing=False)

    event_name = schedule.get("EventName", pd.Series(dtype=str)).astype(str)
    official_name = schedule.get("OfficialEventName", pd.Series(dtype=str)).astype(str)
    target = race_name.strip()

    mask = event_name.str.contains(target, case=False, na=False) | official_name.str.contains(
        target, case=False, na=False
    )

    matched = schedule[mask]
    if matched.empty:
        return None

    return int(matched.iloc[0]["RoundNumber"])


def fetch_gp_data(race_name: str, start_year: int = TRAIN_START_YEAR, end_year: int = TRAIN_END_YEAR) -> pd.DataFrame:
    """Fetch race and qualifying data for a selected GP and build a driver-level dataset."""
    rows: List[dict] = []

    for year in range(start_year, end_year + 1):
        try:
            round_number = _find_race_round(year, race_name)
            if round_number is None:
                continue

            race = fastf1.get_session(year, round_number, "R")
            quali = fastf1.get_session(year, round_number, "Q")
            race.load(telemetry=False, weather=False, messages=False)
            quali.load(telemetry=False, weather=False, messages=False)
        except Exception:
            continue

        race_res = race.results.reset_index(drop=True).copy()
        quali_res = quali.results.reset_index(drop=True).copy()

        if race_res.empty or quali_res.empty:
            continue

        race_res = race_res[["DriverNumber", "Abbreviation", "Position", "GridPosition", "Points", "TeamName"]].copy()
        quali_res = quali_res[["DriverNumber", "Position"]].copy()
        quali_res = quali_res.rename(columns={"Position": "QualiPosition"})

        merged = race_res.merge(quali_res, on="DriverNumber", how="left")
        merged["Year"] = year

        for _, r in merged.iterrows():
            race_pos = int(r["Position"]) if pd.notna(r["Position"]) else 99
            grid_pos = int(r["GridPosition"]) if pd.notna(r["GridPosition"]) else 99
            quali_pos = int(r["QualiPosition"]) if pd.notna(r["QualiPosition"]) else 99
            points = float(r["Points"]) if pd.notna(r["Points"]) else 0.0

            rows.append(
                {
                    "Year": int(r["Year"]),
                    "Driver": r["Abbreviation"],
                    "Team": r["TeamName"],
                    "GridPosition": grid_pos,
                    "QualiPosition": quali_pos,
                    "Points": points,
                    "IsWinner": 1 if race_pos == 1 else 0,
                }
            )

    return pd.DataFrame(rows)


def build_features(df: pd.DataFrame):
    """Create model features and one-hot encode team and driver."""
    if df.empty:
        raise ValueError("No GP data found. Check race name, internet connection, and fastf1 cache.")

    feature_df = df.copy()
    feature_df["GridQualiDelta"] = feature_df["GridPosition"] - feature_df["QualiPosition"]

    numeric_cols = ["Year", "GridPosition", "QualiPosition", "GridQualiDelta", "Points"]
    cat_cols = ["Driver", "Team"]

    x_num = feature_df[numeric_cols]
    x_cat = pd.get_dummies(feature_df[cat_cols], prefix=cat_cols)
    x = pd.concat([x_num, x_cat], axis=1)
    y = feature_df["IsWinner"]

    return x, y, x.columns


def train_model(x: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a simple classifier to estimate winner probability."""
    model = RandomForestClassifier(
        n_estimators=400,
        random_state=42,
        class_weight="balanced",
        max_depth=8,
        min_samples_leaf=2,
    )
    model.fit(x, y)
    return model


def evaluate(model: RandomForestClassifier, x: pd.DataFrame, y: pd.Series) -> None:
    preds = model.predict(x)
    print("\nTraining-set evaluation (quick sanity check):")
    print(classification_report(y, preds, digits=3))


def predict_next_gp_winner(
    model: RandomForestClassifier,
    feature_columns: pd.Index,
    current_grid: pd.DataFrame,
    year: int,
) -> pd.DataFrame:
    """
    Predict winner probabilities for a given GP grid.

    current_grid must include: Driver, Team, GridPosition, QualiPosition, Points
    """
    pred_df = current_grid.copy()
    pred_df["Year"] = year
    pred_df["GridQualiDelta"] = pred_df["GridPosition"] - pred_df["QualiPosition"]

    x_num = pred_df[["Year", "GridPosition", "QualiPosition", "GridQualiDelta", "Points"]]
    x_cat = pd.get_dummies(pred_df[["Driver", "Team"]], prefix=["Driver", "Team"])
    x = pd.concat([x_num, x_cat], axis=1)

    x = x.reindex(columns=feature_columns, fill_value=0)

    winner_proba = model.predict_proba(x)[:, 1]
    pred_df["WinProbability"] = winner_proba
    pred_df = pred_df.sort_values("WinProbability", ascending=False).reset_index(drop=True)

    return pred_df[["Driver", "Team", "GridPosition", "WinProbability"]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict F1 GP winner probabilities.")
    parser.add_argument("race", nargs="+", help='Race name, e.g. Abu Dhabi Grand Prix')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    race_name = " ".join(args.race).strip()

    os.makedirs("./f1_cache", exist_ok=True)
    fastf1.Cache.enable_cache("./f1_cache")

    data = fetch_gp_data(race_name, TRAIN_START_YEAR, TRAIN_END_YEAR)
    if data.empty:
        print(f"No data downloaded for '{race_name}'. Could not train model.")
        return

    x, y, feature_columns = build_features(data)
    model = train_model(x, y)
    evaluate(model, x, y)

    # Replace this with the actual grid for the target GP before predicting.
    sample_grid = pd.DataFrame(
        [
            {"Driver": "VER", "Team": "Red Bull Racing", "GridPosition": 1, "QualiPosition": 1, "Points": 0},
            {"Driver": "LEC", "Team": "Ferrari", "GridPosition": 2, "QualiPosition": 2, "Points": 0},
            {"Driver": "NOR", "Team": "McLaren", "GridPosition": 3, "QualiPosition": 3, "Points": 0},
            {"Driver": "HAM", "Team": "Mercedes", "GridPosition": 4, "QualiPosition": 4, "Points": 0},
        ]
    )

    predictions = predict_next_gp_winner(model, feature_columns, sample_grid, year=PREDICT_YEAR)
    print(f"\nPredicted {race_name} winner probabilities ({PREDICT_YEAR}) using data from {TRAIN_START_YEAR}-{TRAIN_END_YEAR}:")
    print(predictions.to_string(index=False))


if __name__ == "__main__":
    main()
