import cv2
import pickle
import cvzone
import numpy as np
import picamera
import base64
import imutils
from mqtt_publish import send_mqtt


#import requests
#from ubidots1 import *

# Video feed
#cap = cv2.VideoCapture('carPark.h264')

#with open('CarParkPos', 'rb') as f:
    #posList = pickle.load(f)

#width, height = 88, 188

def main():
    
        
    # Video feed
    cap = cv2.VideoCapture('output.h264')

    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

    width, height = 88, 188
    
    def checkParkingSpace(imgPro):
        spaceCounter = 0

        for pos in posList:
            x, y = pos

            imgCrop = imgPro[y:y + height, x:x + width]
            # cv2.imshow(str(x * y), imgCrop)
            count = cv2.countNonZero(imgCrop)


            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                #print(spaceCounter)
                spaceCounter += 1
                
                #parking = []
                #parking.append(spaceCounter)
                #print(parking)
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                               thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                               thickness=5, offset=20, colorR=(0,200,0))
    
    while True:
        try :
            
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16)
            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            checkParkingSpace(imgDilate)
            cv2.imshow("image", img)
            filename = 'output.jpg'
            cv2.imwrite(filename, img)
            # cv2.imshow("ImageBlur", imgBlur)
            # cv2.imshow("ImageThres", imgMedian)
            cv2.waitKey(1)
            return img
        except :
            
            return f"balik lagi"
    

# while True:

#     if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#     success, img = cap.read()
#    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
#    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                         cv2.THRESH_BINARY_INV, 25, 16)
#    imgMedian = cv2.medianBlur(imgThreshold, 5)
#    kernel = np.ones((3, 3), np.uint8)
#    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

#    checkParkingSpace(imgDilate)
#    cv2.imshow("Image", img)
#     cv2.imshow("ImageBlur", imgBlur)
#     cv2.imshow("ImageThres", imgMedian)
#    cv2.waitKey(10)
    
if __name__ == '__main__':
    #while (True):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = (40)
    while True :
        
        camera.start_recording('output.h264')
        camera.wait_recording(0.1)
        camera.stop_recording()
        image = main()
        with open("output.jpg", "rb") as image:
            img = image.read()
    
        message = img
        base64_bytes = base64.b64encode(message)
        base64_message = base64_bytes.decode('ascii')
        send_mqtt(base64_message)
        #with open("output.png", "rb") as img_file:
            # b64_string = base64.b64encode(img_file.read())
        # image = imutils.resize(image, width=400)
        # img_str = cv2.imencode('.png', image)[1].tostring()
        # b64 = base64.b64encode(img_str)
        # print(b64)
        # b64 = b64.decode('utf-8')
        # send_data(b64)
    #time.sleep(1)
