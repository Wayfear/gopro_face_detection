from goprocam import GoProCamera
from goprocam import constants
import cv2
import socket
from os.path import join
import os
from src import detect_faces, show_bboxes
from PIL import Image
import time
import sys
import yaml

sock = None
restart_flag = False

project_dir = os.getcwd()
with open(join(project_dir, 'config.yaml'), 'r') as f:
    cfg = yaml.load(f)

shoot_duration = cfg['auto_stream']['shoot_hours'] * 3600

start = time.time()
while True:
    skip = 4
    if sock is not None:
        sock.close()
        time.sleep(3)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    t=time.time()
    gpCam = GoProCamera.GoPro()
    gpCam.syncTime()
    gpCam.livestream("start")
    cap = cv2.VideoCapture("udp://10.5.5.9:8554")
    num = 0
    skip_frame = 0

    while True:
        if restart_flag:
            restart_flag = False
            break
        start_time = time.time()
        flag = time.time()
        count = 0

        while True:
            num+=1
            # frame = None
            nmat, frame = cap.read()
            if flag - start_time > 1:
                print("Restart!")
                restart_flag = True
                break
            if frame is None:
                print("No frame!")
                flag = time.time()
                continue
            if skip_frame!=0:
                skip_frame-=1
                # print(skip_frame)
                continue
            if num%skip!=0:
                continue
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # start = timeit.default_timer()
            bounding_boxes, landmarks = detect_faces(image)
            # stop = timeit.default_timer()
            print(bounding_boxes)
            if len(bounding_boxes)>0:
                count += 1
            else:
                count = 0
            if count>0:
                print(str(time.time()) + ' take_video!')
                skip_frame = 100
                gpCam.shoot_video(5)
                print("Finish!")
                # print('mtcnn process time: {}'.format(stop - start))
                start_time = time.time()
                break


            for b in bounding_boxes:
                cv2.rectangle(frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (55, 255, 155), 2)

            cv2.imshow('frame', frame)
            start_time = time.time()
            flag = time.time()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - t >= 2.5:
                sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
                t=time.time()

        cv2.destroyAllWindows()


