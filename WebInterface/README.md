# Object Detection Flask Application

This repository contains a Flask-based web application for object detection using the YOLO (You Only Look Once) model. The application can process  video streams, detecting objects and displaying the  coordinates, angles and length details.


## Requirements

- Python 3.6+
- Flask
- ultralytics
- numpy
- pillow
- opencv-python
- werkzeug

## Setup

1. Clone the repository:

```bash
git clone https://github.com/manavchouhan115/KeypointEstimation.git
cd Webinterface
```

2. In app.py there are 2 input parameters - model and frame_rate

- Enter the model here
model = YOLO(model_path) 
- Enter frame rate i.e. after how many seconds you want to process the frame 
frame_rate = 1 


3. Running the Application
To start the Flask application, run:
```bash
python app.py
```
The application will be available at http://localhost:8000.


Real-time Video Detection
1. Open your browser and navigate to http://localhost:8000/
2. The application will start the webcam and display the real-time object detection and display the coordinates, angles and length details.
