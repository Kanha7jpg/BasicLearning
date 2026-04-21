# Handwritten Number Guesser

This project can learn numbers from `0` to `9`.
Then you can draw a number with your mouse, and the computer will guess it.

## What this does

- Learns from the MNIST number pictures dataset
- Opens a small drawing window
- Lets you draw one number
- Tells you the guessed number and confidence

## Files in this folder

- `handwritten_digit_recognition.py` -> main program
- `requirements.txt` -> needed Python packages
- `mnist_digit_model.keras` -> saved model (created after first training)

## Easy setup

Open terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## How to run

### First time (train model + open drawing window)

```bash
python handwritten_digit_recognition.py
```

### Faster next time (skip training + open drawing window)

```bash
python handwritten_digit_recognition.py --skip-train
```

### Optional: train longer and show learning graphs

```bash
python handwritten_digit_recognition.py --epochs 10 --show-plots
```

## How to use the drawing window

1. Draw one number on the black box.
2. Click `Predict`.
3. See the guessed number.
4. Click `Clear` to try again.
5. Click `Close` to exit.

## Helpful tips

- Draw one big number in the center.
- Use a thick, clear stroke.
- If guess is wrong, click `Clear` and try again.

## Do I need to download MNIST manually?

No. TensorFlow downloads it automatically the first time.