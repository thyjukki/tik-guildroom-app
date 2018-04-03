import cv2
from threading import Thread
import requests
import sys, os, time
import json
import datetime

class webcamImageGetter:
    def __init__(self, id):
        self.currentFrame = None
        self.CAMERA_WIDTH = 1280
        self.CAMERA_HEIGHT = 800
        self.CAMERA_NUM = id

        self.capture = cv2.VideoCapture(self.CAMERA_NUM) #Put in correct capture number here
        #OpenCV by default gets a half resolution image so we manually set the correct resolution
        self.capture.set(3,self.CAMERA_WIDTH)
        self.capture.set(4,self.CAMERA_HEIGHT)

    #Starts updating the images in a thread
    def start(self):
        Thread(target=self.updateFrame, args=()).start()

    #Continually updates the frame
    def updateFrame(self):
        while True:
            ret, self.currentFrame = self.capture.read()

            while not ret: #Continually grab frames until we get a good one
                ret, frame = self.capture.read()

    def getFrame(self):
        return self.currentFrame

    def isOpened(self):
        print ("Camera {} is {}".format(self.CAMERA_NUM, self.capture.isOpened()))
        return self.capture.isOpened()

token = os.environ.get('KILTACAM_TOKEN', 'empty')
host = os.environ.get('KILTACAM_HOST', '127.0.0.1')
flip_cams = json.loads(os.environ.get('KILTACAM_FLIP_CAMS', '[]'))

print ("Starting camera client for {} host, password {}".format(host, token))
def listCameras():
    cams = []
    while True: 
        try: 
            cam = webcamImageGetter(len(cams))
            value = cam.isOpened() 
 
            if not value: 
                return cams

            cam.start()
            cams.append(cam)
        except: 
            return cams 

def insertTimestamp(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fontScale = 0.5
    thickness = 1

    retval, baseLine = cv2.getTextSize(str, font, fontScale, thickness)
    textWidth, textHeight = retval
    newimg = cv2.copyMakeBorder(
                     img, 
                     0, 
                     textHeight + 4, 
                     0, 
                     0, 
                     cv2.BORDER_CONSTANT, 
                     value=(0, 0, 0)
                  )
    height, width, channels = newimg.shape 
    cv2.putText(newimg, str, (width - textWidth-2, height - textHeight + 8), font, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
    return newimg

cameras = []

while not cameras:
    cameras = listCameras()
    if not cameras:
        print("NO CAMERAS FOUND, checking again in 10 seconds!")
        time.sleep (10)
    else:
        print("Found {} camera(s)".format(len(cameras)))

while True:
    for index, cam in enumerate(cameras):
        try:
            img = cam.getFrame()

            if img:
                if (index in flip_cams):
                    img = cv2.flip( img, -1 )
                img = insertTimestamp(img)
                cv2.imwrite("last.jpg",img)

                baseUrl = 'http://{}/cam/api/set'.format(host)
                files = {"current": open('last.jpg', 'rb')}
                res = requests.post(baseUrl, {"position": index, "token": token}, files=files)
        except Exception as e:
            print("Camera by index {}: {}".format(index, e))
    time.sleep(30)