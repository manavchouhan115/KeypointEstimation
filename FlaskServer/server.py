from flask import Flask, jsonify, render_template, send_from_directory
import cv2
from ultralytics import YOLO

app = Flask(__name__, static_folder="static")

# Initialize YOLO and video capture
model = YOLO("Yolov5l_4labels.pt")
model.classes = [0, 1, 2, 3]  # Specify 4 class labels
cap = cv2.VideoCapture(0)

# Normalize coordinates
def normalize_coordinates(x_pixel, y_pixel, frame_width, frame_height):
    x_normalized = (x_pixel - frame_width / 2) / (frame_width / 16)  # Normalize x to range -8 to 8
    y_normalized = -(y_pixel - frame_height / 2) / (frame_height / 9)  # Normalize y to range -4.5 to 4.5
    return x_normalized, y_normalized

@app.route('/')
def index():
    return render_template("index.html")  # Serve the HTML page

@app.route('/detect', methods=['GET'])
def detect():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"}), 500

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    results = model.predict(source=frame, conf=0.5)

    # JSON structure
    frame_json = {
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

    for result in results:
        boxes = result.boxes.xyxy
        class_ids = result.boxes.cls

        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i].tolist()
            class_id = int(class_ids[i])
            if class_id in label_map:
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                x_normalized, y_normalized = normalize_coordinates(x_center, y_center, frame_width, frame_height)
                frame_json[label_map[class_id]] = {"x": x_normalized, "y": y_normalized}

    return jsonify(frame_json)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)  # Serve static files (JS, CSS, etc.)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
