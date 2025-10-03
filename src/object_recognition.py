
"""
object_recognition.py - Object and scene recognition using camera
Cross-platform scaffolding for integration with assistant hub.
"""


import sys
import platform
try:
    import cv2
except ImportError:
    cv2 = None
from .camera import get_live_frame

def describe_scene():
    """
    Describe the scene using the latest frame from the shared camera (sunglasses or default).
    Uses MobileNet-SSD for object detection on desktop platforms.
    """
    if cv2 is None:
        raise ImportError('OpenCV (cv2) is required for object recognition.')
    import os
    proto = 'MobileNetSSD_deploy.prototxt.txt'
    model = 'MobileNetSSD_deploy.caffemodel'
    if not (os.path.exists(proto) and os.path.exists(model)):
        return ("Model files not found. Please download 'MobileNetSSD_deploy.prototxt.txt' and "
                "'MobileNetSSD_deploy.caffemodel' and place them in the same directory as this script.\n"
                "Get them from: https://github.com/chuanqi305/MobileNet-SSD")
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    net = cv2.dnn.readNetFromCaffe(proto, model)
    frame = get_live_frame()
    if frame is None:
        return "No camera frame available. Ensure your sunglasses or camera is connected."
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    objects = set()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.4:
            idx = int(detections[0, 0, i, 1])
            if 0 <= idx < len(CLASSES):
                objects.add(CLASSES[idx])
    if objects:
        return "Scene description: " + ", ".join(sorted(objects))
    else:
        return "No recognizable objects detected."

def identify_object():
    """
    Identify the most prominent object using the latest frame from the shared camera.
    Uses MobileNet-SSD for object detection on desktop platforms.
    """
    if cv2 is None:
        raise ImportError('OpenCV (cv2) is required for object recognition.')
    import os
    proto = 'MobileNetSSD_deploy.prototxt.txt'
    model = 'MobileNetSSD_deploy.caffemodel'
    if not (os.path.exists(proto) and os.path.exists(model)):
        return ("Model files not found. Please download 'MobileNetSSD_deploy.prototxt.txt' and "
                "'MobileNetSSD_deploy.caffemodel' and place them in the same directory as this script.\n"
                "Get them from: https://github.com/chuanqi305/MobileNet-SSD")
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    net = cv2.dnn.readNetFromCaffe(proto, model)
    frame = get_live_frame()
    if frame is None:
        return "No camera frame available. Ensure your sunglasses or camera is connected."
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    best_conf = 0
    best_obj = None
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > best_conf and confidence > 0.4:
            idx = int(detections[0, 0, i, 1])
            if 0 <= idx < len(CLASSES):
                best_conf = confidence
                best_obj = CLASSES[idx]
    if best_obj:
        return f"Identified object: {best_obj} (confidence: {best_conf:.2f})"
    else:
        return "No recognizable object detected."
