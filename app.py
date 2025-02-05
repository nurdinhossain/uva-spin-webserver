# imports
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from collections import deque
import random

# create flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

# store data
MAX_DATA_POINTS = 20
data_points = []

# basic route
@app.route('/')
def index():
    return render_template('index.html', data=data_points)

# route for receiving data
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global data_points
    
    if request.method == 'POST':
        # Handle POST data
        input_json = request.get_json()
        timestamp = float(list(input_json.keys())[0])
        ain_value = float(list(input_json.values())[0])
        
        data_points.append({'x': timestamp, 'y': ain_value})
        if len(data_points) > MAX_DATA_POINTS:
            data_points.pop(0)

        # Broadcast update via WebSocket
        socketio.emit('update', data_points)  # Changed from return
        
        return jsonify(success=True)
    
    else:  # Handle GET requests
        return jsonify(data_points)  # Return stored data 

# run flask server
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)