import cv2
import math
import os
from time import sleep, time


imagesFolder = os.path.dirname(os.path.realpath(__file__)) + "\\other\\images"
cap = cv2.VideoCapture(0)
value = cap.read()

def listCameras():
    count = 0
    while True:
        try:
            cap = cv2.VideoCapture(count)
            value = cap.isOpened()

            if not value:
                return count
            count = count + 1
        except:
            return count

cameracount = listCameras()
if not os.path.exists(imagesFolder):
    os.makedirs(imagesFolder)

delay = 30
lapse = delay / cameracount
camera = 0
lasttime = 0

cameras = []
for x in range(0, cameracount):
    cameras.append(cv2.VideoCapture(x))

while True:

    elapsed = time() - lasttime
    if elapsed >= lapse:
        cam = cameras[camera]
        ret, frame = cam.read()
        if (ret == True):

            filename = imagesFolder + "\\current_{}.png".format(camera)
        
            try:
                os.remove(filename)
            except OSError:
                pass
            wrote = cv2.imwrite(filename, frame)
            
        camera = camera + 1
        if cameracount <= camera:
            camera = 0
        lasttime = time()
        
print ("Done!")