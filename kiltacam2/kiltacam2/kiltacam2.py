import cv2
import requests
import sys, os, time
import json
import datetime

token = os.environ.get('KILTACAM_TOKEN', 'empty')
host = os.environ.get('KILTACAM_HOST', '127.0.0.1')
flip_cams = json.loads(os.environ.get('KILTACAM_FLIP_CAMS', '[]'))

print ("Starting camera client for {} host, password {}".format(host, token))
def listCameras():
    cams = []
    while True: 
        try: 
            cam = cv2.VideoCapture(len(cams)) 
            value = cam.isOpened() 
 
            if not value: 
                return cams

            cam.set(3,1280)
            cam.set(4,800)
            cams.append(cam)
        except: 
            return cams 

def insertTimestamp(img):
    height, width, channels = img.shape 
    font = cv2.FONT_HERSHEY_SIMPLEX
    str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fontScale = 0.5
    thickness = 1

    retval, baseLine = cv2.getTextSize(str, font, fontScale, thickness)
    textWidth, textHeight = retval
    cv2.putText(img, str, (width - textWidth , height - textHeight), font, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)



while(True):
    cameras = listCameras()
    print("Found {} camera(s)".format(len(cameras)))
    for index, cam in enumerate(cameras):
        try:
            s, img = cam.read()
            if s:# frame captured without any errors
                if (index in flip_cams):
                    img = cv2.flip( img, -1 )
                cv2.imwrite("last.jpg",img)

                baseUrl = 'http://{}/cam/api/set'.format(host)
                files = {"current": cv2.open('last.jpg', 'rb')}
                res = requests.post(baseUrl, {"position": index, "token": token}, files=files)
        except Exception as e:
            print("Camera by index {}: {}".format(index, e))
        cam.release()
    time.sleep(30)