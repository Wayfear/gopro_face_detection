from goprocam import GoProCamera
from goprocam import constants
import cv2
import socket
import numpy as np
from src import detect_faces, show_bboxes
from PIL import Image
import time

skip = 4
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t=time.time()
gpCam = GoProCamera.GoPro()
gpCam.syncTime()
gpCam.livestream("start")
cap = cv2.VideoCapture("udp://10.5.5.9:8554")
num = 0
skip_frame = 0



while True:
    count = 0
    while True:
        num+=1
       	nmat, frame = cap.read()
        # print(len(frame))
        if frame is None:
            continue
        if skip_frame!=0:
            skip_frame-=1
            # print(skip_frame)
            continue
        if num%skip!=0:
            continue
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        bounding_boxes, landmarks = detect_faces(image)
        print(bounding_boxes)
        if len(bounding_boxes)>0:
            count += 1
        else:
            count = 0
        if count>0:
            print(str(time.time()) + ' take_video!')
            skip_frame = 100
            gpCam.shoot_video(5)
            break


        for b in bounding_boxes:
            cv2.rectangle(frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (55, 255, 155), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time.time() - t >= 2.5:
            sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
            t=time.time()
    cv2.destroyAllWindows()

