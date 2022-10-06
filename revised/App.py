#firebasee
from pyrebase import pyrebase
#OS
import os

#Facial Tracker and Recorder
import TrackNRecord as tr

def Upload(filename):
    print("Uploading to Firebase...")
    print("File selected: " + filename)
     #firebase id
    config = {
        #PASTE KEY CONFIG HERE
    }
    
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    
    path_on_cloud = filename
    path_local = filename
    
    storage.child(path_on_cloud).put(path_local)
    
    
if __name__== "__main__":
    filename = tr.TrackNRecord() #Resulting output filename of the app.
    print("=================================================")
    print("Output file saved as: " + filename)
    Upload(filename)
    print("Exiting app...")