from flask import Flask, jsonify, Response, render_template
from flask_cors import CORS
import cv2
import base64
from flask import request
from pyzbar.pyzbar import decode

app = Flask(__name__)
CORS(app)

# OpenCV VideoCapture for webcam
video_capture = cv2.VideoCapture(0)

# Function to generate frames from the webcam
def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # You can perform any additional processing on the frame here if needed
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Endpoint to get webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint to get data for the frontend
@app.route('/get_data', methods=['GET'])
def get_data():
    # Sending specific values for length, width, height, and weight
    data_to_send = {
        'length': 10,
        'width': 10,
        'height': 10,
        'weight': 10
    }

    return jsonify(data_to_send)

@app.route('/get_barcode', methods=['GET'])
def get_barcode():

    #Take a picture from the webcam
    success, image = video_capture.read()
    if not success:
        return "Error taking picture from webcam"
    
    barcodes = decode(image)
    if barcodes:
        barcode_data = barcodes[0].data.decode('utf-8')
    else:
        barcode_data = 0
    
    
    
    data_to_send = {
        'barcode': barcode_data
    }

    return jsonify(data_to_send)
    
    
        
      

# Endpoint to render the HTML page with video feed
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
