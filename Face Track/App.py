#Google Drive
import pydrive #Install using pydrive

#OS
import os

#Facial Tracker and Recorder
import TrackNRecord as tr

def Upload(filename):
    print("Uploading to Google Drive...")
    print("File selected: " + filename)
    '''
    Do Google Drive related code here
    Suggested article: https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20
    '''

if __name__== "__main__":
    filename = tr.TrackNRecord() #Resulting output filename of the app.
    print("=================================================")
    print("Output file saved as: " + filename)
    Upload(filename)
    print("Exiting app...")