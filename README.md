# FaceTracker
 
Simply run `App.py` to start

Upon camera selection, it would be better if you have 2 cameras that could be used for tracking and recording. Do note of certain hardware compatibility issues as the program was not tested fully with different hardware.

Face Tracking Program Files:
1. `App.py` = Driver
2. `TrackNRecord.py` = Face Tracking and Recording Driver
3. `AVRecorder.py` = Video Recording (Separate Thread)
4. ffmpeg.exe = muxer to H.264

Algorithm Testing Program Files
1. Test.py = For testing algorithms against a set of images, whether as base truth or false.
