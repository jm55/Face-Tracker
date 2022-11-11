# FaceTracker
 
Simply run `App.py` to start

**Description:**
The project is a simple tracking and recording software that uses OpenCV through Python for face tracking and recording, ffmpeg for video re-encoding, and Arduino for hardware control.

Though recommended and intended for the application of the technology, the use of Arduino for active tracking is not necessary. Certain smart CCTV cameras make use of such technology even without active tracking, though it may require a better FOV camera to track more people.

The program was not tested completely with many people but was once tested to be able to track more than 1 person seen by the camera at a time.

**Status:**
1. Common misdetection of persons are curtains in certain lighting conditions
2. Haven't tested on higher resolution cameras, though it is expected to execute slowly.
3. The program runs around 10<= to <30fps depending on background load and camera capture speed depending on lighting conditions (darker scenes == slow FPS)
4. Tracking and recording functions are threaded separately on their own OpenCV instances (Yes, we know that OpenCV wasn't meant for recording). Using a single camera for both tracking and recording causes A/V time mismatch, thus it would be best if it was separated.

**Execution/Notes:**

0. Dependencies: Execute `Install.bat` batch script using the terminal to install dependencies of the project. (Just type `Install.bat`)
1. Main Application:
	1. Plug cameras 
	2. Upon launching the app, enter the number/id for the tracking and recording (separate; From a given range of 0 to n, only use from 0 to n-1 as n is sort of a loopback feed)
	3. Wait for the program to load until a window shows up.
2. Test.py: 
	1. Enter folder path
	2. State whether it should detect a face or not
	3. State whether it should multiple faces or not (if it would detect faces)
	4. Run scanning

**Face Tracking Program Files:**
1. `App.py` = Driver
2. `TrackNRecord.py` = Face Tracking and Recording Driver
3. `AVRecorder.py` = Video Recording (Separate Thread)
4. ffmpeg.exe = muxer to H.264
5. Arduino IDE = For controlling motor via Arduino (uses C/++ like language; Arduino code is at #1 of sources)

**Algorithm Testing Program Files**
1. Test.py = For testing algorithms against a set of images, whether as base truth or false.

**Recommended Hardware**
1. Arduino Uno
2. Stepper Motor
3. Breadboard
4. Jumper wires (pin-like)
5. 2 Cameras

**Sources:**
1. Face Tracking by Shubham Santosh (https://create.arduino.cc/projecthub/shubhamsantosh99/face-tracker-using-opencv-and-arduino-55412e)
2. AV Recording by JRodrigoF (https://github.com/JRodrigoF/AVrecordeR)
