from cv2 import VideoCapture, imwrite
import requests
import sys, os, time

token = os.environ.get('KILTACAM_TOKEN', 'empty')
host = os.environ.get('KILTACAM_HOST', '127.0.0.1')

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

                baseUrl = 'http://{}/cam/api/set'.format(host)
                files = {"current": open('last.jpg', 'rb')}
                res = requests.post(baseUrl, {"position": index, "token": token}, files=files)
        except Exception as e:
            print("Camera by index {}: {}".format(index, e))
    time.sleep(5)