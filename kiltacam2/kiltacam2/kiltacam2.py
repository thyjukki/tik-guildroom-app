from cv2 import VideoCapture, imwrite,CAP_PROP_BUFFERSIZE
import requests
import sys, os, time

token = os.environ.get('KILTACAM_TOKEN', 'empty')
host = os.environ.get('KILTACAM_HOST', '127.0.0.1')

print ("Starting camera client for {} host, password {}".format(host, token))
def listCameras():
    cams = []
    while True: 
        try: 
            cam = VideoCapture(len(cams)) 
            value = cam.isOpened() 
 
            if not value: 
                return cams

            cam.set(CAP_PROP_BUFFERSIZE, 1)
            cam.set(3,1280)
            cam.set(4,800)
            cams.append(cam)
        except: 
            return cams 


print("Found {} camera(s)".format(len(cameras)))

while(True):
    cameras = listCameras()
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
        cam.release()
    time.sleep(30)