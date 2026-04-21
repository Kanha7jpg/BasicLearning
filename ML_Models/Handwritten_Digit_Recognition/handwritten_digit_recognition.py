"""MNIST handwritten digit recognition with a simple neural network.

This script is designed for understanding the core ideas behind a neural network:
- load and normalize image data
- build a small dense classifier
- train the model
- evaluate accuracy
- inspect a few predictions
- draw your own digit and predict it

Run:
    python handwritten_digit_recognition.py --epochs 5
    python handwritten_digit_recognition.py --skip-train
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a simple neural network on the MNIST handwritten digit dataset.",
    )
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=128, help="Batch size used for training")
    parser.add_argument(
        "--save-model",
        type=str,
        default="mnist_digit_model.keras",
        help="Path to save the trained model",
    )
    parser.add_argument(
        "--show-plots",
        action="store_true",
        help="Display training curves and sample predictions in a window",
    )
    parser.add_argument(
        "--skip-train",
        action="store_true",
        help="Skip training and load an existing saved model for prediction",
    )
    return parser.parse_args()


def load_data() -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)

    return (x_train, y_train), (x_test, y_test)


def build_model() -> tf.keras.Sequential:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(28, 28, 1)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def load_or_train_model(args: argparse.Namespace):
    save_path = Path(args.save_model)

    if args.skip_train:
        if not save_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {save_path}. Run once without --skip-train to train and save it."
            )
        print(f"Loading existing model from: {save_path}")
        model = tf.keras.models.load_model(save_path)
        return model, None, None, None

    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_data()

    print("Building model...")
    model = build_model()
    model.summary()

    print("Training model...")
    history = model.fit(
        x_train,
        y_train,
        validation_split=0.1,
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=2,
    )

    print("Evaluating on the test set...")
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Test loss: {test_loss:.4f}")

    model.save(save_path)
    print(f"Saved trained model to: {save_path}")

    return model, history, x_test, y_test


def preprocess_pil_image(image: Image.Image) -> np.ndarray:
    resized = image.resize((28, 28), Image.Resampling.LANCZOS)
    image_array = np.asarray(resized, dtype="float32") / 255.0
    image_array = np.expand_dims(image_array, axis=-1)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def predict_from_pil_image(model: tf.keras.Model, image: Image.Image) -> tuple[int, float]:
    image_batch = preprocess_pil_image(image)
    probabilities = model.predict(image_batch, verbose=0)[0]
    predicted_digit = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    return predicted_digit, confidence


def interactive_drawing_window(model: tf.keras.Model) -> None:
    canvas_size = 280
    stroke_width = 18

    root = tk.Tk()
    root.title("Draw a digit (0-9)")
    root.resizable(False, False)

    status_var = tk.StringVar(value="Draw a digit, then click Predict")

    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="black")
    canvas.pack(padx=12, pady=(12, 8))

    # Mirror the canvas into an in-memory grayscale image for model input.
    pil_image = Image.new("L", (canvas_size, canvas_size), color=0)
    draw = ImageDraw.Draw(pil_image)

    last_pos: list[int] = []

    def on_press(event) -> None:
        last_pos.clear()
        last_pos.extend([event.x, event.y])

    def on_drag(event) -> None:
        if not last_pos:
            last_pos.extend([event.x, event.y])
            return

        x1, y1 = last_pos
        x2, y2 = event.x, event.y

        canvas.create_line(x1, y1, x2, y2, fill="white", width=stroke_width, capstyle=tk.ROUND, smooth=True)
        draw.line((x1, y1, x2, y2), fill=255, width=stroke_width)

        last_pos[0], last_pos[1] = x2, y2

    def clear_canvas() -> None:
        canvas.delete("all")
        draw.rectangle((0, 0, canvas_size, canvas_size), fill=0)
        status_var.set("Canvas cleared. Draw a digit, then click Predict")

    def predict_digit() -> None:
        try:
            predicted_digit, confidence = predict_from_pil_image(model, pil_image)
            status_var.set(f"Predicted digit: {predicted_digit} | Confidence: {confidence:.2%}")
        except Exception as exc:
            status_var.set(f"Prediction failed: {exc}")

    controls = tk.Frame(root)
    controls.pack(padx=12, pady=(0, 8), fill="x")

    predict_button = tk.Button(controls, text="Predict", command=predict_digit)
    clear_button = tk.Button(controls, text="Clear", command=clear_canvas)
    close_button = tk.Button(controls, text="Close", command=root.destroy)

    predict_button.pack(side="left", expand=True, fill="x", padx=(0, 6))
    clear_button.pack(side="left", expand=True, fill="x", padx=6)
    close_button.pack(side="left", expand=True, fill="x", padx=(6, 0))

    status_label = tk.Label(root, textvariable=status_var, anchor="w")
    status_label.pack(padx=12, pady=(0, 12), fill="x")

    canvas.bind("<Button-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)

    root.mainloop()


def plot_history(history: tf.keras.callbacks.History) -> None:
    epochs = range(1, len(history.history["accuracy"]) + 1)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, history.history["accuracy"], label="Train Accuracy")
    plt.plot(epochs, history.history["val_accuracy"], label="Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Accuracy")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, history.history["loss"], label="Train Loss")
    plt.plot(epochs, history.history["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss")
    plt.legend()

    plt.tight_layout()
    plt.show()


def show_predictions(model: tf.keras.Model, x_test: np.ndarray, y_test: np.ndarray, count: int = 12) -> None:
    predictions = model.predict(x_test[:count], verbose=0)
    predicted_labels = np.argmax(predictions, axis=1)

    cols = 4
    rows = int(np.ceil(count / cols))
    plt.figure(figsize=(12, 3 * rows))

    for index in range(count):
        plt.subplot(rows, cols, index + 1)
        plt.imshow(x_test[index].squeeze(), cmap="gray")
        true_label = int(y_test[index])
        predicted_label = int(predicted_labels[index])
        color = "green" if true_label == predicted_label else "red"
        plt.title(f"True: {true_label} | Pred: {predicted_label}", color=color)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def main() -> None:
    args = parse_args()

    model, history, x_test, y_test = load_or_train_model(args)

    if history is not None and x_test is not None and y_test is not None:
        if args.show_plots:
            plot_history(history)
            show_predictions(model, x_test, y_test)
        else:
            print("Tip: rerun with --show-plots to see training curves and sample predictions.")

    interactive_drawing_window(model)


if __name__ == "__main__":
    main()