# --- Placeholder for owner voice enrollment ---
def enroll_owner_voice():
    """Simulate enrolling the owner's voice. Returns True for success."""
    # TODO: Replace with real voice enrollment logic
    print("[INFO] enroll_owner_voice called (placeholder)")
    return True

# --- Placeholder for owner voice recognition ---
def recognize_owner_voice():
    """Simulate recognizing the owner's voice. Returns True if recognized, False otherwise."""
    # TODO: Replace with real voice recognition logic
    print("[INFO] recognize_owner_voice called (placeholder)")
    return True

# --- Shared Camera Manager for Live Camera Access ---
import cv2
import threading
import time
from PIL import Image
import numpy as np
import pytesseract

class CameraManager:
    """
    Singleton camera manager for live frame access from sunglasses or default camera.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_camera()
            return cls._instance

    def _init_camera(self):
        self.cap = None
        self.frame = None
        self.running = False
        self.thread = None
        self.device_index = self._find_sunglasses_camera()
        self._open_camera()

    def _find_sunglasses_camera(self):
        # Try to find sunglasses camera by name (if available), else use default (0)
        # This is a stub: on Windows, use DirectShow to list devices; on Linux, enumerate /dev/video*
        # For now, return 0. You can customize this to select the correct device.
        return 0

    def _open_camera(self):
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Unable to open camera at index {self.device_index}")
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
            time.sleep(0.03)  # ~30 FPS

    def get_frame(self):
        """Return the latest frame as a numpy array (BGR)."""
        return self.frame

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

# --- Example usage for other modules ---
def get_live_frame():
    """Get the latest frame from the shared camera manager."""
    cam = CameraManager()
    return cam.get_frame()

# --- Legacy functions (can be refactored to use CameraManager) ---
def capture_and_read_text():
    frame = get_live_frame()
    if frame is not None:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(img)
        print(f"Detected text: {text}")
    else:
        print("No camera frame available.")
