'''
Face Tracking by Shubham Santosh (https://create.arduino.cc/projecthub/shubhamsantosh99/face-tracker-using-opencv-and-arduino-55412e)
AV Recording by JRodrigoF (https://github.com/JRodrigoF/AVrecordeR)
'''

#Tracking Libraries
import cv2
import serial #PLEASE UNCOMMENT THIS
import time

#Recording Libraries
import AVrecordeR
import subprocess
import os

print("Setting variables...")
print("Loading classifier...")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
print("Loading camera...")
camera = 0
cap = cv2.VideoCapture(camera)
print("Setting output file...")
filename = time.ctime(time.time()).replace(':','').replace(' ','-')
audio_thread = None
print("Setting timestamp...")
start_time = 0
end_time = 0

def TrackNRecord():
    print("Output file to be saved as: " + filename + ".avi")
    #Arduino Connection
    print("Connecting to Arduino...")
    #ArduinoSerial=serial.Serial('com3',9600,timeout=0.1) #PLEASE UNCOMMENT THIS
    time.sleep(1)

    start_time = time.time()
    AVrecordeR.ready_audio_recording()
    AVrecordeR.audio_thread.start()
    framecount = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1,6)
        track = ""
        for x,y,w,h in faces:
            track = 'X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
            #ArduinoSerial.write(track.encode('utf-8')) #PLEASE UNCOMMENT THIS
            #Center of Face
            #cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
            #ROI
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
        #Squared Region
        #cv2.rectangle(frame,(640//2-30,480//2-30),(640//2+30,480//2+30),(255,255,255),3)

        #Text data on frame
        #Just comment out what you need and don't need
        #Reference: https://stackoverflow.com/a/34273603
        recorded_time = time.time()-start_time-2
        framecount = framecount + 1
        truefps = round(framecount/recorded_time,2)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(frame, 'Frame Count: ' + str(framecount) + " (" + str(truefps) + '/' + str(fps) + "fps)", org=(20,380), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Frame Count
        cv2.putText(frame, 'Arduino Track: ' + track, org=(20,420), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Arduino Tracking Data
        cv2.putText(frame, 'Recorded Time: ' + time.strftime('%H:%M:%S', time.gmtime(recorded_time)), org=(20,440), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Recorded Time
        cv2.putText(frame, time.ctime(time.time()), org=(20,460), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Time Data
        if len(faces) == 0:
            cv2.putText(frame, 'Face Count: No Face Detected',org=(20,400), fontFace=0, fontScale=0.6,color=(255,255,255),thickness=2) #No Face Alert
        else:
            cv2.putText(frame, 'Face Count: ' + str(len(faces)), org=(20,400), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Face Tracking Data
        #Camera Window
        window_title = "Face Tracker"
        cv2.imshow(window_title, frame)

        #Write output as video or image
        cv2.imwrite('frames\\' + "frame{}.jpg".format(str(framecount).zfill(5)), frame)

        #Exit
        if cv2.waitKey(10)&0xFF== ord('q'):
            AVrecordeR.audio_thread.stop()
            cv2.destroyAllWindows()
            cap.release()
    #Video writing
    print("Writing video...")
    writeVideo()
    #Muxing
    print("Muxing...")
    #Timing offsets, int only. Negative to delay, positive to advance
    audio_offset = '-1.0'
    video_offset = '0.0'
    start_trim = '00:00:02' #Don't Modify
    cmd = "ffmpeg -ac 2 -channel_layout mono -itsoffset " + audio_offset + " -i temp_audio.wav -itsoffset " + video_offset + " -i temp_video.avi -ss " + start_trim + " -b:v 6M -q:v 2 -pix_fmt yuv420p -filter:v fps=10 " + filename + ".avi"
    ffmpeg = subprocess.Popen(cmd, shell=True)
    ffmpeg.wait()
    
def writeVideo(): #https://stackoverflow.com/questions/69620079/video-recording-is-too-fast-in-opencv
    frames = [f for f in os.listdir('frames\\') if ".jpg" in f]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vid = None
    size = (640,480)
    fps = 9
    count = 0
    for f in frames:
        if not os.path.exists('frames\\' + f):
            raise FileNotFoundError(f)
        img = cv2.imread('frames\\' + f)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter('temp_video'+'.avi',fourcc,fps,size)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
    vid.release()
    return