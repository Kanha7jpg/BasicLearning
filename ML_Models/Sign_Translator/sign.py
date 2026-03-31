import argparse
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model

try:
	import pyttsx3
except ImportError:
	pyttsx3 = None


def parse_args():
	parser = argparse.ArgumentParser(
		description="Real-time Sign Language Translator (webcam + TensorFlow/Keras model)",
	)
	parser.add_argument(
		"--model",
		type=str,
		default="model/sign_model.h5",
		help="Path to trained Keras model (.h5/.keras)",
	)
	parser.add_argument(
		"--labels",
		type=str,
		default="model/labels.txt",
		help="Path to labels text file (one label per line or 'index,label')",
	)
	parser.add_argument(
		"--camera",
		type=int,
		default=0,
		help="Webcam index (default: 0)",
	)
	parser.add_argument(
		"--confidence",
		type=float,
		default=0.75,
		help="Minimum confidence to accept a prediction",
	)
	parser.add_argument(
		"--stability",
		type=int,
		default=6,
		help="Frames needed with same prediction before adding text",
	)
	parser.add_argument(
		"--cooldown",
		type=float,
		default=0.8,
		help="Seconds between accepted gesture commits",
	)
	parser.add_argument(
		"--roi-scale",
		type=float,
		default=0.55,
		help="Central square ROI size relative to min(frame_w, frame_h)",
	)
	parser.add_argument(
		"--audio",
		action="store_true",
		help="Enable text-to-speech output (requires pyttsx3)",
	)
	return parser.parse_args()


def load_labels(labels_path):
	path = Path(labels_path)
	if not path.exists():
		raise FileNotFoundError(f"Labels file not found: {path}")

	labels = []
	with path.open("r", encoding="utf-8") as file:
		for line in file:
			line = line.strip()
			if not line:
				continue
			if "," in line:
				_, label = line.split(",", 1)
				labels.append(label.strip())
			else:
				labels.append(line)

	if not labels:
		raise ValueError("Labels file is empty.")

	return labels


def build_tts_engine(enable_audio):
	if not enable_audio:
		return None
	if pyttsx3 is None:
		print("[WARN] pyttsx3 is not installed. Audio output is disabled.")
		return None

	engine = pyttsx3.init()
	engine.setProperty("rate", 165)
	return engine


def get_model_input_spec(model):
	input_shape = model.input_shape
	if isinstance(input_shape, list):
		input_shape = input_shape[0]

	if len(input_shape) != 4:
		raise ValueError(
			f"Expected a 4D model input shape (batch, h, w, c), got: {input_shape}"
		)

	_, height, width, channels = input_shape
	if height is None or width is None:
		raise ValueError(
			"Model input height/width cannot be None. Use a fixed input shape model."
		)

	if channels not in (1, 3):
		raise ValueError(
			f"Expected model channels to be 1 or 3, got: {channels}"
		)

	return int(height), int(width), int(channels)


def preprocess_roi(roi_bgr, input_height, input_width, channels):
	image = cv2.resize(roi_bgr, (input_width, input_height), interpolation=cv2.INTER_AREA)
	if channels == 1:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image = image.astype(np.float32) / 255.0
		image = np.expand_dims(image, axis=-1)
	else:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = image.astype(np.float32) / 255.0

	return np.expand_dims(image, axis=0)


def apply_command(token, sentence):
	key = token.strip().lower()
	if key in {"space", "_", "[space]"}:
		return sentence + " "
	if key in {"del", "delete", "backspace", "[del]"}:
		return sentence[:-1]
	if key in {"clear", "cls", "[clear]"}:
		return ""
	return sentence + token


def main():
	args = parse_args()

	model_path = Path(args.model)
	if not model_path.exists():
		raise FileNotFoundError(
			f"Model file not found: {model_path}\n"
			"Train a model first and pass --model with the correct path."
		)

	print("[INFO] Loading model...")
	model = load_model(model_path)
	labels = load_labels(args.labels)
	input_h, input_w, input_c = get_model_input_spec(model)
	tts_engine = build_tts_engine(args.audio)

	print(f"[INFO] Model input shape: ({input_h}, {input_w}, {input_c})")
	print(f"[INFO] Loaded {len(labels)} labels")

	cap = cv2.VideoCapture(args.camera)
	if not cap.isOpened():
		raise RuntimeError(
			f"Could not open webcam index {args.camera}. Check camera permissions."
		)

	buffer = deque(maxlen=max(1, args.stability))
	last_commit_time = 0.0
	last_committed_label = ""
	sentence = ""

	print("[INFO] Press 'q' to quit | 'c' to clear | 'v' to speak sentence")

	while True:
		ok, frame = cap.read()
		if not ok:
			print("[WARN] Failed to read frame from webcam.")
			break

		frame = cv2.flip(frame, 1)
		frame_h, frame_w = frame.shape[:2]

		roi_size = int(min(frame_h, frame_w) * args.roi_scale)
		roi_size = max(64, roi_size)
		x1 = frame_w // 2 - roi_size // 2
		y1 = frame_h // 2 - roi_size // 2
		x2 = x1 + roi_size
		y2 = y1 + roi_size

		x1 = max(0, x1)
		y1 = max(0, y1)
		x2 = min(frame_w, x2)
		y2 = min(frame_h, y2)

		roi = frame[y1:y2, x1:x2]
		model_input = preprocess_roi(roi, input_h, input_w, input_c)
		predictions = model.predict(model_input, verbose=0)[0]

		pred_idx = int(np.argmax(predictions))
		confidence = float(predictions[pred_idx])
		predicted_label = labels[pred_idx] if pred_idx < len(labels) else f"class_{pred_idx}"

		if confidence >= args.confidence:
			buffer.append(predicted_label)
		else:
			buffer.append("")

		stable_label = ""
		if len(buffer) == buffer.maxlen and len(set(buffer)) == 1 and buffer[0] != "":
			stable_label = buffer[0]

		now = time.time()
		if (
			stable_label
			and (now - last_commit_time) >= args.cooldown
			and stable_label != last_committed_label
		):
			sentence = apply_command(stable_label, sentence)
			last_commit_time = now
			last_committed_label = stable_label

		cv2.rectangle(frame, (x1, y1), (x2, y2), (60, 220, 120), 2)
		cv2.putText(
			frame,
			f"Pred: {predicted_label} ({confidence:.2f})",
			(10, 30),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.8,
			(0, 255, 255),
			2,
			cv2.LINE_AA,
		)
		cv2.putText(
			frame,
			f"Text: {sentence[-45:]}",
			(10, frame_h - 15),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,
			(255, 255, 255),
			2,
			cv2.LINE_AA,
		)
		cv2.putText(
			frame,
			"q: quit | c: clear | v: voice",
			(10, frame_h - 45),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.62,
			(200, 200, 200),
			2,
			cv2.LINE_AA,
		)

		cv2.imshow("Real-Time Sign Language Translator", frame)

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		if key == ord("c"):
			sentence = ""
			last_committed_label = ""
		if key == ord("v") and sentence.strip() and tts_engine is not None:
			tts_engine.say(sentence)
			tts_engine.runAndWait()

	cap.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
