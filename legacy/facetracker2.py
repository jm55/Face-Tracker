#Face tracker using OpenCV and Arduino
#by Shubham Santosh

#Audio Recording by JRodrigoF (https://github.com/JRodrigoF/AVrecordeR)

print('Importing libraries...')
import cv2 #Camera
#import serial #Arduino Connection #PLEASE UNCOMMENT THIS
import time #Timing
from AVrecordeR import start_audio_recording, stop_AVrecording

#Classifier
print("Loading classifier...")
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Camera
camera = 0 #Set camera value
print("Loading camera: "+str(camera)+"...")
cap=cv2.VideoCapture(camera + cv2.CAP_DSHOW)

#Video Recording
filename = time.ctime(time.time())
filename = filename.replace(':','-')
print("Footage to be saved as: "+ filename + ".avi")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#FPS set to 10.0 instead of the default 20.0 since the recordings seem quick and not in real time.
out = cv2.VideoWriter(filename+'.avi',fourcc,10.0,(640,480)) 

#Arduino Connection
#ArduinoSerial=serial.Serial('com3',9600,timeout=0.1) #PLEASE UNCOMMENT THIS
time.sleep(1)

#Capture
start_time = time.time()
end_time = 0
print("Capturing...")
while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #Mirror the image
    #print(frame.shape) #Prints frame size
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)  #Detect Face`
    track=""
    for x,y,w,h in faces:
        #sending coordinates to Arduino
        track='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
        #ArduinoSerial.write(track.encode('utf-8')) #PLEASE UNCOMMENT THIS
        #print(track) #Tracking for Arduino
        
        #Center of Face
        cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
        #Region of Interest
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    #Plot the squared region in the center of the screen
    cv2.rectangle(frame,(640//2-30,480//2-30),(640//2+30,480//2+30),(255,255,255),3)
    
    #Write text data on frame
    #Just comment out what you need and don't need
    #Reference: https://stackoverflow.com/a/34273603
    cv2.putText(frame, 'Face Count: ' + str(faces), org=(20,400), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Face Tracking Data
    cv2.putText(frame, 'Arduino Track: ' + track, org=(20,420), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Arduino Tracking Data
    cv2.putText(frame, 'Recorded Time: ' + time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)), org=(20,440), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Recorded Time
    cv2.putText(frame, time.ctime(time.time()), org=(20,460), fontFace=0, fontScale=0.6, color=(255,255,255), thickness=2) #Time Data
    
    
    #Camera Window
    window_title = "Face Tracker" #Window Title
    cv2.imshow(window_title,frame)
    
    #Write output as video or image
    out.write(frame) #Video
    #cv2.imwrite('output_img.jpg',frame) #Image
    
    '''for testing purpose
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''
    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
