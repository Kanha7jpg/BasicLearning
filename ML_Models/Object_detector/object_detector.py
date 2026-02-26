"""
Simple webcam object detector using TensorFlow Hub and OpenCV.

Usage:
    python object_detector.py --camera 0 --threshold 0.35

Press 'q' to quit the video window.
"""

import time
import argparse

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# COCO labels (index 1-based from model classes). Index 0 is reserved.
COCO_LABELS = [
    '???', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
    'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
    'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
    'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
    'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]


def load_model(model_handle: str):
    print('Loading model from:', model_handle)
    t0 = time.time()
    model = hub.load(model_handle)
    print('Model loaded in %.2f sec' % (time.time() - t0))
    return model


def draw_boxes(frame, boxes, classes, scores, threshold=0.35):
    h, w, _ = frame.shape
    for i in range(boxes.shape[0]):
        score = scores[i]
        if score < threshold:
            continue
        ymin, xmin, ymax, xmax = boxes[i]
        left, top, right, bottom = int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h)
        class_id = int(classes[i])
        label = COCO_LABELS[class_id] if class_id < len(COCO_LABELS) else str(class_id)
        cv2.rectangle(frame, (left, top), (right, bottom), (10, 255, 0), 2)
        label_text = f"{label}: {score:.2f}"
        t_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.rectangle(frame, (left, top - t_size[1] - 6), (left + t_size[0] + 6, top), (10, 255, 0), -1)
        cv2.putText(frame, label_text, (left + 3, top - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)


def run_detector(model, camera_index=0, threshold=0.35, width=640, height=480):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        raise RuntimeError(f'Could not open camera index {camera_index}')

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)
            input_tensor = tf.expand_dims(input_tensor, 0)  # batch

            outputs = model(input_tensor)

            # Model outputs may be tensors; convert to numpy
            boxes = outputs['detection_boxes'].numpy()[0]
            classes = outputs['detection_classes'].numpy()[0].astype(np.int32)
            scores = outputs['detection_scores'].numpy()[0]

            draw_boxes(frame, boxes, classes, scores, threshold)

            cv2.imshow('Object Detector (press q to quit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser(description='Webcam object detector using TensorFlow Hub + OpenCV')
    parser.add_argument('--model', help='TF-Hub model handle',
                        default='https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')
    parser.add_argument('--camera', type=int, default=0, help='Camera device index')
    parser.add_argument('--threshold', type=float, default=0.35, help='Detection score threshold')
    parser.add_argument('--width', type=int, default=640, help='Camera width')
    parser.add_argument('--height', type=int, default=480, help='Camera height')
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        model = load_model(args.model)
    except Exception as e:
        print('Failed to load model:', e)
        print('If you haven\'t installed dependencies, run: pip install -r requirements.txt')
        return

    run_detector(model, camera_index=args.camera, threshold=args.threshold, width=args.width, height=args.height)


if __name__ == '__main__':
    main()
