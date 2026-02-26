Object Detector (Webcam)

This folder contains a simple webcam object detector using TensorFlow Hub and OpenCV.

Files:
- object_detector.py : main detection script
- requirements.txt : Python dependencies

Quick start:

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# or cmd
.venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the detector:

```bash
python object_detector.py --camera 0 --threshold 0.35
```

Press `q` to quit the window.

Notes:
- The script loads a TF-Hub SSD MobileNet model by default. The first run will download the model and may take time.
- If you need a different model, pass `--model <TFHUB_HANDLE>`.
- For better performance on constrained machines, consider an optimized or TFLite model.
