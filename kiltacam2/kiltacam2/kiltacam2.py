from cv2 import VideoCapture, imwrite
import requests
import sys, os, time
sys.path.append('lib')

def listCameras():
    cams = []
    while True: 
        try: 
            cam = VideoCapture(len(cams)) 
            value = cam.isOpened() 
 
            if not value: 
                return cams
            cam.set(3,1280)
            cam.set(4,800)
            cams.append(cam)
        except: 
            return cams 

cameras = listCameras()

while(True):
    for index, cam in enumerate(cameras):
        try:
            s, img = cam.read()
            if s:# frame captured without any errors
                imwrite("last.jpg",img)

                baseUrl = 'http://localhost:8000/cam/api/set'
                files = {"current": open('last.jpg', 'rb')}
                res = requests.post(baseUrl, {"position": index, "token": "empty"}, files=files)
        except e:
            print("Camera by index {}: {}".format(index, e))
    time.sleep(5)