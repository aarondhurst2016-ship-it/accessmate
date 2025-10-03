# Object detection for Tkinter (desktop)
import cv2
import numpy as np

def detect_objects_from_camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Camera', frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        # Placeholder: use a pre-trained MobileNet or YOLO model for real detection
        print("Detected: shirt, pants, apple, milk (example)")
    cap.release()
