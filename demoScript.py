import cv2
import torch
import time
import json
from ultralytics import YOLO

import asyncio
import websockets
import json

model_path = "Yolov5l_4labels.pt"
# Define normalization function
def normalize_coordinates(x_pixel, y_pixel, frame_width, frame_height):
    x_normalized = (x_pixel - frame_width / 2) / (frame_width / 16)  # Normalize x to range -8 to 8
    y_normalized = -(y_pixel - frame_height / 2) / (frame_height / 9)  # Normalize y to range -4.5 to 4.5
    return x_normalized, y_normalized

model = YOLO(model_path)
model.classes = [0, 1, 2, 3]  # Specify 4 class labels (0, 1, 2, 3)

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for default camera or provide a video file path

# Frame dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize JSON structure
json_data = {
    "smallArmTop": {"x": 0, "y": 0},
    "smallArmBottom": {"x": 0, "y": 0},
    "bigArmTop": {"x": 0, "y": 0},
    "bigArmBottom": {"x": 0, "y": 0}
}

# Label mapping
label_map = {
    0: "bigArmBottom",
    1: "bigArmTop",
    2: "smallArmBottom",
    3: "smallArmTop",
}

# Capture and process video
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Run inference
        start_time = time.time()
        results = model.predict(source=frame, conf=0.5) 
        end_time = time.time()
        time_taken = end_time - start_time
        print("Time required to show the output:", time_taken, "seconds")

        # Update JSON structure for the current frame
        frame_json = json_data.copy()

        # Process detections
        for result in results:
            boxes = result.boxes.xyxy  # Bounding box coordinates in [x1, y1, x2, y2] format
            class_ids = result.boxes.cls  # Class IDs
            scores = result.boxes.conf  # Confidence scores

            for i in range(len(boxes)):
                x1, y1, x2, y2 = boxes[i].tolist()  # Extract coordinates
                class_id = int(class_ids[i])  # Class ID
                score = scores[i].item()  # Confidence score

                if class_id in label_map: 
                    x_center = (x1 + x2) / 2
                    y_center = (y1 + y2) / 2
                    x_normalized, y_normalized = normalize_coordinates(x_center, y_center, frame_width, frame_height)
                    frame_json[label_map[class_id]] = {"x": x_normalized, "y": y_normalized}

                    # Draw circle on the frame at the pixel location
                    cv2.circle(frame, (int(x_center), int(y_center)), radius=5, color=(0, 255, 0), thickness=-1)


        # Print missing coordinates
        for key in frame_json:
            if isinstance(frame_json[key], dict) and frame_json[key] == {"x": 0, "y": 0}:
                print(f"Coordinate for {key} is missing")

        # Convert to JSON string
        json_string = json.dumps(frame_json, indent=4)
        print(json_string)

        # Display the video frame
        cv2.imshow("YOLO Real-Time", frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Pause for half a second to generate JSON output
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
