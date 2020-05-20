import paho.mqtt.client as mqtt
import os
import re

LOCAL_MQTT_HOST="mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="cloud/face"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received!")
    msg = msg.payload
    files = os.listdir("/tmp")
    cur_face_num = 1
    for file in files:
        m = re.match("^face\d+.png", file)
        if m:
            num = re.match("d+", file)
            if num >= cur_face_num:
                cur_face_num = num + 1
    with open("/tmp/"+"face" + str(cur_face_num) + ".png", "wb") as img:
        img.write(msg)
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
