import cv2
import json
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class DistractionDetector:
    def __init__(self, config_path="config/settings.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Load lightweight YOLOv8 model
        self.model = YOLO('yolov8n.pt') 
        
        # Initialize modern MediaPipe Tasks Face Detector targeting the local model file
        base_options = python.BaseOptions(
            model_asset_path='assets/blaze_face_short_range.tflite'
        )
        options = vision.FaceDetectorOptions(
            base_options=base_options,
            min_detection_confidence=self.config["yolo_confidence"]
        )
        
        self.detector = vision.FaceDetector.create_from_options(options)

    def process_frame(self, frame):
        """
        Processes a single frame to look for both a face and a phone.
        Returns: face_detected (bool), face_box (list), phone_detected (bool), phone_box (list)
        """
        # 1. Run YOLO Object Detection with performance flags
        # 'half=False' ensures compatibility on older CPUs, 'device=cpu' ensures it doesn't get stuck searching for broken CUDA drivers
        results = self.model(frame, verbose=False, device='cpu')[0]
        phone_detected = False
        phone_box = None

        for box in results.boxes:
            if int(box.cls[0]) == 67 and box.conf[0] >= self.config["yolo_confidence"]:
                phone_detected = True
                phone_box = [int(coord) for coord in box.xyxy[0].tolist()] 
                break

        # 2. Run Modern MediaPipe Face Detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        face_results = self.detector.detect(mp_image)
        face_detected = False
        face_box = None

        if face_results.detections:
            face_detected = True
            bbox = face_results.detections[0].bounding_box
            h, w, _ = frame.shape
            
            # Extract absolute pixel positions
            face_box = [
                max(0, int(bbox.origin_x)), 
                max(0, int(bbox.origin_y)), 
                min(w, int(bbox.origin_x + bbox.width)), 
                min(h, int(bbox.origin_y + bbox.height))
            ]

        return face_detected, face_box, phone_detected, phone_box