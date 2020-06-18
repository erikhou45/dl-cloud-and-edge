import os
import tensorflow.contrib.tensorrt as trt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph

import cv2
import time
import paho.mqtt.client as mqtt


FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'

output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())


INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]


# trt_graph = trt.create_inference_graph(
#     input_graph_def=frozen_graph,
#     outputs=output_names,
#     max_batch_size=1,
#     max_workspace_size_bytes=1 << 25,
#     precision_mode='FP16',
#     minimum_segment_size=50
# )

tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')



LOCAL_MQTT_HOST="mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="edge/face"

local_mqttclient = mqtt.Client()
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 600)

cap = cv2.VideoCapture(1)

num_frames = 0
frame_batch = 50
start = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    num_frames += 1
#     frame = cv2.imread(IMAGE_PATH)
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = frame
    image_resized = cv2.resize(image, (300, 300))
    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
        tf_input: image_resized[None, ...]
    })

    boxes = boxes[0] # index by 0 to remove batch dimension
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]

    plot_ind = 0
    DETECTION_THRESHOLD = 0.5
    
    for i in range(int(num_detections)):
        if scores[i] < DETECTION_THRESHOLD:
            continue
        # scale box to image coordinates
        box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
    #     print(box)
        box = box.astype(int)
        face = image[box[0]:box[2]+1, box[1]:box[3]+1]
#         cv2.imwrite("face_"+str(plot_ind)+".png", face)
        rc, png = cv2.imencode('.png', face)
        msg = png.tobytes()
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    
    if num_frames % frame_batch == 0:
        end = time.time()
        seconds = end - start
        print("Time taken : {0} seconds".format(seconds))
#         print("Process: {0} frames".format(num_frames))
        fps  = frame_batch / seconds
        print("Estimated frames per second : {0}".format(fps))
        start = time.time()
