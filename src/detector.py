import cv2
import json
from ultralytics import YOLO
import mediapipe as mp

class DistractionDetector:
    def __init__(self, config_path="config/settings.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Load lightweight YOLOv8 model (automatically downloads on first run)
        self.model = YOLO('yolov8n.pt') 
        
        # Initialize MediaPipe Face Detection
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(
            min_detection_confidence=self.config["yolo_confidence"]
        )

    def process_frame(self, frame):
        """
        Processes a single frame to look for both a face and a phone.
        Returns: face_detected (bool), face_box (list), phone_detected (bool), phone_box (list)
        """
        # 1. Run YOLO Object Detection for phone
        results = self.model(frame, verbose=False)[0]
        phone_detected = False
        phone_box = None

        for box in results.boxes:
            # Class 67 in the COCO dataset corresponds to 'cell phone'
            if int(box.cls[0]) == 67 and box.conf[0] >= self.config["yolo_confidence"]:
                phone_detected = True
                phone_box = [int(coord) for coord in box.xyxy[0].tolist()] 
                break

        # 2. Run MediaPipe Face Detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.face_detection.process(frame_rgb)
        face_detected = False
        face_box = None

        if face_results.detections:
            face_detected = True
            bbox = face_results.detections[0].location_data.relative_bounding_box
            h, w, _ = frame.shape
            face_box = [
                max(0, int(bbox.xmin * w)), 
                max(0, int(bbox.ymin * h)), 
                min(w, int((bbox.xmin + bbox.width) * w)), 
                min(h, int((bbox.ymin + bbox.height) * h))
            ]

        return face_detected, face_box, phone_detected, phone_box