from cv2 import *
import requests
import sys, os, time
sys.path.append('lib')

cam = VideoCapture(0)
cam.set(3,1280)
cam.set(4,800)

while(True):
    s, img = cam.read()
    if s:    # frame captured without any errors
        imwrite("last.jpg",img)

        baseUrl = 'http://localhost:8000/cam/api/set'
        files = {"current": open('last.jpg', 'rb')}
        res = requests.post(baseUrl, {"position": 0}, files=files)
    time.sleep(5)