import cv2
import os
import time
import math

#global var
count = 0 #sampled images
quantity = 0 #total images
faceMode = False
facecascade = ''

def checkImage(face_cascade, filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6) #refer here for parameter explanation: https://stackoverflow.com/a/20805153
    return len(faces)

def load():
    return cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def cls():
    os.system('cls')

def printDisplay(foldername, mode, completed, ctr, quantity):
    print("====FACE DETECTION TESTING SCRIPT====")
    print("Selected folder: " + foldername)
    print("# of files: " + str(quantity))
    print("Find face?: " + str(mode))
    print("Finding faces: " + str(completed) + "% (" + str(ctr) + "/" + str(quantity) + ")...")

#load auxilliaries
currDir = os.getcwd()
facecascade = load()

#menu (single-run)
cls()
print("====FACE DETECTION TESTING SCRIPT====")
foldername = input("Enter folder path: ")
mode = int(input("Has face (1 - Yes, 0 - No): "))
if mode == 0:
    mode = False
else:
    mode = True
files = os.listdir(foldername)
quantity = len(files)

#execute command
ctr = 0
cls()
start = time.time()
for f in files:
    cls()
    completed = math.ceil((ctr/quantity)*100)
    printDisplay(foldername, mode, completed, ctr, quantity)
    faces = checkImage(facecascade, foldername+"\\"+f)
    if mode and faces > 0: #find faces
        count += 1
    else:
        if faces == 0:
            count += 1
    ctr += 1
cls()
end = time.time()
rate = round((count/quantity)*100,2)

#final print
printDisplay(foldername, mode, completed, ctr, quantity)
print("=====================================")
print("Result: " + str(rate) + "%")
if mode and rate < 100:
    print("Warning: Some faces were not detected!")
elif not mode and rate < 100:
    print("Warning: False positive detected!")
print("Time elapsed: " + str(round(end-start,2)) + "s")