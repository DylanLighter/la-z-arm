# La-Z-Arm
A robotic arm that mimics hand movement through MediaPipe tracking.

### Hardware
- NVidia Jetson Nano
- Sparkfun Pi Servo Shield
- Micro Servos
- Webcam

### Basic Dependencies
- Python 3
- Mediapipe (see below)
- OpenCV
- Numpy

The Jetson Nano has ARM64 architecture, which makes the setup process for MediaPipe a little more complicated than `pip install mediapipe`. See [this helpful repo](https://github.com/pinto0309/mediapipe-bin).

### Extras
- 3D-printed hand
- Twine

### Goals

So far, finger movement is almost fully implemented.

`finger-angle.py` contains code to calculate, based on a triangle formed between points at the fingertip, knuckle, and wrist, how much a finger is curled. `motors.py` converts that into a number in the range -180 to 180 degrees to turn a motor that tightens "tendons" of twine in the hand's segmented fingers.

The next goal is arm movement, which will be achieved in mostly the same way--I expect similar angle calculations can be used, but the conversion to rotation for each joint's motors will be more complex as there is more than one axis of articulation.

If both of these goals are reached reasonably quickly, another goal could be AI integration using inverse kinematics and the webcam to detect and manipulate objects without the need for a human to control it.
