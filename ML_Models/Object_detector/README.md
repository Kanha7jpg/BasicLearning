# Object Detector (Webcam)

This project looks at your webcam and finds objects like person, bottle, car, and more.

## Files

- `object_detector.py` - main program
- `requirements.txt` - needed packages

## Setup

In this folder, run:

```bash
pip install -r requirements.txt
```

## How to run

```bash
python object_detector.py --camera 0 --threshold 0.35
```

## Controls

- `q` - quit window

## Notes

- First run may be slow because model download happens once.
- Lower threshold shows more boxes.
- Higher threshold shows fewer, more confident boxes.
