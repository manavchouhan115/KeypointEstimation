import cv2
import torch
from ultralytics import YOLO
import numpy as np

# Load the trained YOLOv8s model
model = YOLO('C:\\Users\\Manav\\Downloads\\Yolomodel.pt') # Use the path where the model is saved

frame = cv2.imread("C:\\Users\\Manav\\Desktop\\KeypointEstimation\\testYoloModel\\testYoloImageSamples\\15_frame_0012.jpeg")
# Run YOLOv8 inference on the frame
results = model(frame)
coordinates = []
# Loop through the detection results

def draw_heatmap(frame, coordinates, color=(0, 0, 255), alpha=0.5):
    heatmap = np.zeros_like(frame, dtype=np.uint8)
    for (x1, y1), (x2, y2) in coordinates:
        cv2.line(heatmap, (x1, y1), (x2, y2), color, 5)  # Draw lines for the sticks
    cv2.addWeighted(heatmap, alpha, frame, 1 - alpha, 0, frame)  # Blend heatmap with frame

labels = []
#labels = [0,1]
print(len(results[0].boxes))
for r in results:
    boxes = r.boxes
    for box in boxes:
        # Extract box coordinates and label
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert coordinates to integers
        conf = box.conf[0]  # Confidence score
        label = box.cls[0]  # Class label

        # Determine whether the stick is big or small
        stick_label = "Small Stick" if label == 0 else "Big Stick"
        if label not in labels:
            labels.append(label)
            # Draw the bounding box and label on the frame

            #cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Bounding box in blue
            cv2.putText(frame, f"{stick_label}: {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Display the coordinates
            coordinates_text = f"({x1}, {y1}), ({x2}, {y2})"
            cv2.putText(frame, coordinates_text, (x1, y2 + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            coordinates.append(((x1, y1), (x2, y2)))

# Show the frame with bounding boxes and labels
if coordinates:
    draw_heatmap(frame, coordinates)
cv2.imshow("YOLOv8s Stick Detection", frame)
cv2.imwrite("C:\\Users\\Manav\\Desktop\\KeypointEstimation\\testYoloModel\\testYoloImageSamples\\15_frame_0012_output.jpeg", frame)