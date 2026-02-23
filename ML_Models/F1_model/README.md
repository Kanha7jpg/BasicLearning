# F1 Grand Prix Predictor (2026 Season)

This machine learning tool predicts the most likely winner of a specific Formula 1 Grand Prix by analyzing historical performance patterns from the 2021–2025 seasons.

## Overview

The script, `mlmodel.py`, utilizes a **RandomForestClassifier** trained on data retrieved via the FastF1 API. By evaluating the relationship between qualifying performance, grid starts, and final race results, it generates win probabilities for the 2026 driver lineup.

---

| Feature | Details |
| :--- | :--- |
| **Model Type** | RandomForestClassifier |
| **Training Data** | Historical race results and telemetry from **2021 to 2025** |
| **Prediction Year** | **2026** |
| **Primary Features** | Grid Position, Qualifying Position, Grid-vs-Quali Delta, Driver/Team ID, Points Context |
| **Output** | Probability estimates per driver, ranked by likelihood of winning |

---

## Usage

To generate predictions for a specific race, run the script from your terminal providing the official Grand Prix name as an argument.

### Command Syntax
`python mlmodel.py "[Race Name]"`

### Supported 2026 Calendar Inputs
| | | |
| :--- | :--- | :--- |
| Australian Grand Prix | Chinese Grand Prix | Japanese Grand Prix |
| Bahrain Grand Prix | Saudi Arabian Grand Prix | Miami Grand Prix |
| Emilia Romagna Grand Prix | Monaco Grand Prix | Spanish Grand Prix |
| Canadian Grand Prix | Austrian Grand Prix | British Grand Prix |
| Belgian Grand Prix | Hungarian Grand Prix | Dutch Grand Prix |
| Italian Grand Prix | Azerbaijan Grand Prix | Singapore Grand Prix |
| United States Grand Prix | Mexico City Grand Prix | São Paulo Grand Prix |
| Las Vegas Grand Prix | Qatar Grand Prix | Abu Dhabi Grand Prix |

---

## Important Considerations

| Factor | Description |
| :--- | :--- |
| **Probabilistic Nature** | Results are estimates based on historical trends; they are not guaranteed outcomes. |
| **Model Accuracy** | Accuracy on training data (2021-2025) may appear higher than real-world predictive performance. |
| **Data Sensitivity** | For the most accurate 2026 predictions, the model requires the actual qualifying and grid data from the specific 2026 event. |

---

> **Note:** Ensure you have `fastf1`, `pandas`, and `scikit-learn` installed in your environment before running the model.