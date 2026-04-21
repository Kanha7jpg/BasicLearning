# F1 Winner Predictor

This project tries to guess which driver can win a Formula 1 race.

It uses old race data and a machine learning model.

## Main file

- `F1_Model.py`

## Setup

Install needed packages:

```bash
pip install fastf1 pandas scikit-learn
```

## How to run

Open terminal in this folder and run:

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

## What you get

- A list of drivers
- Win probability for each driver
- Ranked output from highest to lowest chance

## Important note

This is a prediction, not a guarantee.