import cv2
import time
import math
import json
from src.detector import DistractionDetector
from src.audio_manager import AudioManager

def calculate_center(box):
    """Calculates the center (x, y) coordinates of a bounding box."""
    cx = int((box[0] + box[2]) / 2)
    cy = int((box[1] + box[3]) / 2)
    return cx, cy

def main():
    # Load configuration thresholds
    with open("config/settings.json", "r") as f:
        config = json.load(f)

    # Initialize components
    detector = DistractionDetector()
    audio = AudioManager()
    cap = cv2.VideoCapture(0)

    # State tracking variables
    distraction_start_time = None
    
    print("---------------------------------------------")
    print("AI Distraction Detector Active. Press 'q' to exit.")
    print("---------------------------------------------")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        # Mirror effect for natural interaction
        frame = cv2.flip(frame, 1)

        # Process frame via AI models
        face_found, f_box, phone_found, p_box = detector.process_frame(frame)
        
        is_distracted = False

        # Visuals & Spatial relationship checks
        if face_found:
            cv2.rectangle(frame, (f_box[0], f_box[1]), (f_box[2], f_box[3]), (0, 255, 0), 2)
        
        if phone_found:
            cv2.rectangle(frame, (p_box[0], p_box[1]), (p_box[2], p_box[3]), (0, 165, 255), 2)

        # Proximity and Relation Check
        if face_found and phone_found:
            face_center = calculate_center(f_box)
            phone_center = calculate_center(p_box)
            
            # Calculate Euclidean distance between centers
            distance = math.sqrt((face_center[0] - phone_center[0])**2 + (face_center[1] - phone_center[1])**2)
            
            # Draw a line between face and phone center
            cv2.line(frame, face_center, phone_center, (255, 255, 255), 1)

            # Check if phone is close enough to face to mean distraction
            if distance < config["proximity_threshold_pixels"]:
                is_distracted = True

        # Timing and Threat Level logic
        if is_distracted:
            if distraction_start_time is None:
                distraction_start_time = time.time()
            
            elapsed_distraction = time.time() - distraction_start_time
            time_left = max(0.0, config["grace_period_seconds"] - elapsed_distraction)

            if elapsed_distraction >= config["grace_period_seconds"]:
                # Trigger Action!
                cv2.putText(frame, "PUT YOUR PHONE DOWN!", (50, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                audio.play_alarm()
            else:
                # Warning phase
                cv2.putText(frame, f"Put it away in: {time_left:.1f}s", (50, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        else:
            # User is focused
            distraction_start_time = None
            audio.stop_alarm()
            cv2.putText(frame, "Focused", (50, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        # Render display
        cv2.imshow('Anti-Distraction AI System', frame)

        # Key break listener
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources
    cap.release()
    cv2.destroyAllWindows()
    audio.stop_alarm()

if __name__ == "__main__":
    main()