from flask import Flask, request, render_template
import json
import logging
from os import system


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)  # Left motor forward
GPIO.setup(11,GPIO.OUT)  # Left motor backward
GPIO.setup(13,GPIO.OUT)  # Right motor forward
GPIO.setup(15,GPIO.OUT)  # Right motor backward

direction = 0  # Forward
speed = 0

## Directions
# 0 - Forward
# 1 - Left
# 2 - Backward
# 3 - Right
#
# Layout:
#    0
#  1 2 3
##

# Each detection should only move the robot slightly. This resets the outputs after .1 seconds and is called if AI is True in the input
def reset_after_AI():
    global speed
    global direction
    time.sleep(0.1)
    GPIO.output(16, False)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(15, False)
    speed = 0
    direction = 0
    system('clear')
    print("\n=======Controls=======")
    print("Direction: ", direction)
    print("Speed: ", speed)

@app.route('/receiver', methods = ['POST'])
def receiver():
    global speed
    global direction
    # read json + reply
    data = request.get_json(force=True)  # Get the json and turn it into a normal dict, ignore any mistakes that i made using force=True :wink:
    # Extract the data from data into global variables to use to control the motor
    if type(data) == str:
        data = json.loads(data)
    direction = data['direction']   # Direction
    speed = data['speed']           # Turn on motors?
    AI = data['AI']                 # Does this command come from the AI?

    if direction == 0:  # Forward
        GPIO.output(16, True)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, True)
    elif direction == 1:  # Left
        GPIO.output(16, True)
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif direction == 2:  # Backward
        GPIO.output(16, False)
        GPIO.output(11, True)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif direction == 3:  # Right
        GPIO.output(16, False)
        GPIO.output(11, True)
        GPIO.output(13, False)
        GPIO.output(15, True)
    else:                 # Shouldn't happen but just in case: just shut off
        GPIO.output(16, False)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, False)

    if speed == 0:        # Speed 0 = still, Speed 1 = normal
        GPIO.output(16, False)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, False)
    
    # To prevent large movements as a result of AI detection
    if AI: reset_after_AI()

    # Print out some debugging tools and make it look pretty :)
    system('clear')
    print("\n=======Controls=======")
    print("Direction: ", direction)
    print("Speed: ", speed)
    #       direction = data['direction']
    return 'OK'

@app.route('/')
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port='80', debug=True, threaded=True)
GPIO.cleanup()