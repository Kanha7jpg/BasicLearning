p# Real-Time Sign Language Translator

This project translates hand signs from a webcam feed into text in real-time using a trained TensorFlow/Keras model.

## Tech Stack

- Python
- OpenCV (live camera + UI)
- TensorFlow/Keras (gesture classification)
- Hand gesture dataset (for model training)
- Webcam
- Optional: `pyttsx3` for audio output

## Project Files

- `sign.py`: Real-time inference pipeline
- `requirements.txt`: Python dependencies
- `model/sign_model.h5` (you provide): trained classifier model
- `model/labels.txt` (you provide): class labels

## labels.txt Format

You can use either format:

1. One label per line:

```txt
A
B
C
space
del
```

2. `index,label` per line:

```txt
0,A
1,B
2,C
3,space
4,del
```

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python sign.py --model model/sign_model.h5 --labels model/labels.txt --camera 0 --audio
```

## Controls

- `q`: Quit
- `c`: Clear translated text
- `v`: Speak translated text (if audio enabled)

## Notes

- The model should be trained on image crops similar to the ROI shown in the app window.
- If your training data is grayscale, use a model with input shape `(H, W, 1)`.
- If your training data is RGB, use input shape `(H, W, 3)`.
- The script accepts special labels to control text:
  - `space` adds a space
  - `del` / `delete` / `backspace` removes one character
  - `clear` resets the sentence

## Suggested Dataset Sources

- ASL Alphabet dataset
- Custom hand gesture datasets captured with OpenCV

For best accuracy, retrain with lighting/background conditions similar to your real webcam setup.
