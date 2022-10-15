import cv2
import os
import math

#global var
count = 0 #sampled images
quantity = 0 #total images
faceMode = False
facecascade = ''

def checkImage(face_cascade, filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces)

def load():
    return cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def cls():
    os.system('cls')

cls()

#load auxilliaries
currDir = os.getcwd()
facecascade = load()

#menu (single-run)
print("====FACE DETECTION TESTING SCRIPT====")
foldername = input("Enter folder path: ")
mode = int(input("Has face (1 - Yes, 0 - No): "))
if mode == 0:
    mode = False
else:
    mode = True
files = os.listdir(foldername)
quantity = len(files)
print("Selected folder: " + foldername)
print("# of files: " + str(quantity))
print("Find face?: " + str(mode))

#execute command
ctr = 1
cls()
for f in files:
    print("====FACE DETECTION TESTING SCRIPT====")
    print("Selected folder: " + foldername)
    print("# of files: " + str(quantity))
    print("Find face?: " + str(mode))
    print("Finding faces: " + str(math.ceil((ctr/quantity)*100)) + "% (" + str(ctr) + "/" + str(quantity) + ")...")
    faces = checkImage(facecascade, foldername+"\\"+f)
    if mode: #find faces
        if faces > 0:
            count += 1
    else:
        if faces == 0:
            count += 1
    ctr += 1
    cls()
rate = math.ceil((count/quantity)*100)

#final print
print("====FACE DETECTION TESTING SCRIPT====")
print("Selected folder: " + foldername)
print("# of files: " + str(quantity))
print("Find face?: " + str(mode))
print("Results: " + str(rate) + "%")