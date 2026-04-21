# Real-Time Sign Language Translator

This project reads hand signs from your webcam and turns them into text.

## What you need

- Python
- Webcam
- A trained model file: `model/sign_model.h5`
- A labels file: `model/labels.txt`

## Setup

In this folder, run:

```bash
pip install -r requirements.txt
```

## How to run

```bash
python sign.py --model model/sign_model.h5 --labels model/labels.txt --camera 0
```

If you want voice output too:

```bash
python sign.py --model model/sign_model.h5 --labels model/labels.txt --camera 0 --audio
```

## Keyboard controls

- `q` - quit
- `c` - clear text
- `v` - speak text (when audio is on)

## labels.txt example

You can write labels like this:

```text
A
B
C
space
del
```

or like this:

```text
0,A
1,B
2,C
3,space
4,del
```
