from flask import Flask, request, render_template, send_file, Response,jsonify
from werkzeug.utils import secure_filename
import io
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2
import os
import time
import math

app = Flask(__name__)

#-------------------Inputs------------------------------------------
model = YOLO(r"object_detection\yolov8n.pt") #Enter the model here
frame_rate = 1 # Enter frame rate i.e. after how many seconds you want to process the frame 

class Detection:
    def __init__(self):
        #download weights from here:https://github.com/ultralytics/ultralytics and change the path
        self.model = model
        self.stickDetails = []

    def predict(self, img, classes=[], conf=0.5):
        if classes:
            results = self.model.predict(img, classes=classes, conf=conf)
        else:
            results = self.model.predict(img, conf=conf)

        return results

    def predict_and_detect(self, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
        results = self.predict(img, classes, conf=conf)
        coordinates = []
        angles = []
        lengths = []
        for result in results:
            for box in result.boxes[:2]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                coordinates.append([(x1,y1),(x2,y2)])
                angle, length = self.calculate_diagonal_angle_and_length(x1,y1,x2,y2)
                angles.append(round(angle, 2))
                lengths.append(round(length, 2))
                label = box.cls[0]
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                              (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
                cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
        return img, results, [coordinates,angles, lengths]

    def detect_from_image(self, image):
        result_img, _, stickDetails = self.predict_and_detect(image, classes=[], conf=0.5)
        self.stickDetails = stickDetails
        return result_img

    def calculate_diagonal_angle_and_length(self, x1, y1, x2, y2):
        # Calculate the differences in x and y
        delta_y = y2 - y1
        delta_x = x2 - x1
        
        # Calculate the angle in radians and then convert to degrees
        angle_radians = math.atan2(delta_y, delta_x)
        angle_degrees = math.degrees(angle_radians)

        length = math.sqrt(delta_x**2 + delta_y**2)
        
        return angle_degrees, length

    def get_stick_details(self):
        # Simulating stick detection results (replace with actual model output)
        # angle1 = None
        # length1 = None
        # coordinates1 = None
        # angle2 = None
        # length2 = None
        # coordinates2 = None
        #if self.stickDetails == 1
        print(self.stickDetails)
        # if len(self.stickDetails) == 1:
        #     angle1 = self.stickDetails[1][0]
        #     length1 =  self.stickDetails[2][0]
        #     coordinates1 =  self.stickDetails[0][0]
        # if len(self.stickDetails) == 2:
        #     angle1 = self.stickDetails[1][1]
        #     length1 =  self.stickDetails[2][1]
        #     coordinates1 =  self.stickDetails[0][1]
        if self.stickDetails:
            try:
                details = {
                    "stick_type1": "Small",
                    "angle1": self.stickDetails[1][0],
                    "length1": self.stickDetails[2][0],
                    "coordinates1": self.stickDetails[0][0],
                    "stick_type2": "Big",
                    "angle2": self.stickDetails[1][1],
                    "length2": self.stickDetails[2][1],
                    "coordinates2": self.stickDetails[0][1]
                }
            except IndexError:
                print("IndexError: There is only 1 stick in the frame.")
        else:
            details = {
                "stick_type1": "Small",
                "angle1": 45,
                "length1": 120,
                "coordinates1": [(100, 200), (150, 300)],
                "stick_type2": "Big",
                "angle2": 30,
                "length2": 150,
                "coordinates2": [(100, 200), (150, 300)]
            }


        return details

    def draw_heatmap(frame, coordinates, color=(0, 0, 255), alpha=0.5):
        heatmap = np.zeros_like(frame, dtype=np.uint8)
        for (x1, y1), (x2, y2) in coordinates:
            cv2.line(heatmap, (x1, y1), (x2, y2), color, 5)  # Draw lines for the sticks
        cv2.addWeighted(heatmap, alpha, frame, 1 - alpha, 0, frame)  # Blend heatmap with frame


detection = Detection()


@app.route('/')
def index():
    return render_template('video1.html')


@app.route('/video')
def index_video():
    return render_template('video.html')


def gen_frames():
    cap = cv2.VideoCapture(0)
    last_checked = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (512, 512))
        if frame is None:
            break
        # Check if 1 second has passed
        if time.time() - last_checked >= frame_rate:        
            # Update the last checked time
            last_checked = time.time()
            frame = detection.detect_from_image(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        #if cv2.waitKey(1000) & 0xFF == ord('q'):
        #    break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stick_data')
def stick_data():
    # Return stick details in JSON format
    data = detection.get_stick_details()
    print(data)
    return jsonify(data)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
    #http://localhost:8000/video for video source
    #http://localhost:8000 for image source


# @app.route('/object-detection/', methods=['POST'])
# def apply_detection():
#     if 'image' not in request.files:
#         return 'No file part'

#     file = request.files['image']
#     if file.filename == '':
#         return 'No selected file'

#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         img = Image.open(file_path).convert("RGB")
#         img = np.array(img)
#         img = cv2.resize(img, (512, 512))
#         img = detection.detect_from_image(img)
#         output = Image.fromarray(img)

#         buf = io.BytesIO()
#         output.save(buf, format="PNG")
#         buf.seek(0)

#         os.remove(file_path)
#         return send_file(buf, mimetype='image/png')

# def get_stick_details():
#     # Simulating stick detection results (replace with actual model output)
#     details = {
#         "stick_type1": "Small",
#         "angle1": 45,
#         "length1": 120,
#         "coordinates1": [(100, 200), (150, 300)],
#         "stick_type2": "Big",
#         "angle2": 30,
#         "length2": 150,
#         "coordinates2": [(100, 200), (150, 300)]
#     }
#     return details

# stickJson = {
#         "stick_type1": "Small",
#         "angle1": 45,
#         "length1": 120,
#         "coordinates1": [(100, 200), (150, 300)],
#         "stick_type2": "Big",
#         "angle2": 30,
#         "length2": 150,
#         "coordinates2": [(100, 200), (150, 300)]
#     }