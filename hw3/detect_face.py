import numpy as np
import cv2
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="_local/face"

local_mqttclient = mqtt.Client()
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# proceed = True

pic_num = 1

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        # your logic goes here; for instance
        face = gray[y:y+h, x:x+w]
        # rc,png = cv2.imencode('.jpg', face)
        cv2.imwrite(f'face{pic_num}.jpg',face)
        #proceed = False
        # msg = png.tobytes()
        msg = "face" + str(pic_num) + f"{x},{y},{x+w},{y+h}"
        k = cv2.waitKey(10000)
        print("detect a face, please press c to continue")
        # if k == ord('c'): # wait for c key to continue
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
        print("continue to detect the next face")
        # msg = png.tobytes()
        pic_num += 1
