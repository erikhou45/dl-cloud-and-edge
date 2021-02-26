# Face Detection and Storage Pipeline

In this mini-project, I built a pipeline that will:
Capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and save these faces in the cloud for long term storage. We are requested to use MQTT as the messaging fabric and OpenCV for the face detector component.

The requested overall application flow / architecture is like ![this](hw03.png). The homework is implemented in the following steps:

Since the environment in which we are capturing faces for this homework has relatively good WiFi connection, our camera can capture many frames per second (it is expected to have the same face captured many times), and missing a few frames isn't critical for our use, we will use QoS=0 as the setting for our MQTT connection just for better efficiency.

Another setting we have for the MQTT fabric is the topics, at the edge we have `egde/face` as the topic and on the cloud, we have `cloud/face` as the topic. This way we have a good distinction between topics used at the two different steps of our messaging system.

## Spin up a VSI
Use the command below, spin up a ubuntu instance on the IBM cloud
```
ibmcloud sl vs create --hostname=storage --domain=w251.test --cpu=2 --memory=4096 --datacenter=sjc03 --os=UBUNTU_18_64 --san --disk=25 --billing=hourly --key=<my ssh key ID>
```
Install docker on the VSI

## Mount the IBM Cloud Object Storage bucket onto the cloud VSI
Use the commands below, mount a bucket in the IBM COS onto a directory in the VSI
```
sudo apt-get update
sudo apt install -y s3fs
# Create credential file using the credential created from the IBM website
echo "<Access_Key_ID>:<Secret_Access_Key>" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
# Mount the bucket
sudo mkdir -m 777 /mnt/mybucket
sudo s3fs <bucketname> /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://<bucket endpoint>
``` 
## Create docker network bridge in Jetson TX2 and the cloud VSI
Use the command below, create a network bridge in both Jetson TX2 and the cloud VSI respectively
```
docker network create --driver bridge hw03
```
## Spin up a MQTT broker in  Jetson TX2 and the Cloud VSI
Use the commands below, create a MQTT broker with an alpine linux base in TX2 and cloud VSI respectively
```
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
apk update && apk add mosquitto
/usr/sbin/mosquitto
```

## Spin up a image processing container with MQTT client in the cloud VSI
In the cloud VSI, spin up a container build by using the [Dockerfile.processor](https://github.com/erikhou45/w251-assignments/blob/master/hw3/Dockerfile.processor)
```
docker run --network hw03 -v /mnt/mybucket:/tmp --rm -it erikhou/hw3_image_processor:1.00 bash
```
Run the python script, [process_image.py](https://github.com/erikhou45/w251-assignments/blob/master/hw3/process_image.py) to subscribe topic, cloud/face at the MQTT broker on the cloud and get ready to process any incoming image.
```
python3 process_image.py
```

## Spin up a forwarder container at Jetson TX2
At TX2, use the [Dockerfile.forwarder](https://github.com/erikhou45/w251-assignments/blob/master/hw3/Dockerfile.forwarder) to build a docker image for the MQTT forwarder
```
docker build -t forwarder:1.00 -f Dockerfile.forwarder .
```
Run a forwarder container that relays face images from TX2 broker at the edge to VSI broker on the cloud
```
docker run --name forwarder --network hw03 -v /home/ehou/w251/w251-assignments/hw3:/tmp --rm -it forwarder:1.00 sh
```
Run the python script, [forward_messages.py](https://github.com/erikhou45/w251-assignments/blob/master/hw3/forward_messages.py) that will forward the messages automatically
```
cd /tmp
python3 forward_messages.py
```

## Spin up a face detection container with OpenCV and MQTT client in Jetson TX2

Use the [Dockerfile.detector](https://github.com/erikhou45/w251-assignments/blob/master/hw3/Dockerfile.detector) to build a docker image for the face detection container
```
docker build -t face_detector:1.00 -f Dockerfile.detect .
```
Spin up the container
```
docker run -e DISPLAY=$DISPLAY --privileged --network hw03 -v /home/ehou/w251/w251-assignments/hw3:/tmp --rm -it face_detector:1.00 bash
```
Run the python script, [detect_face.py](https://github.com/erikhou45/w251-assignments/blob/master/hw3/detect_face.py) to automatically detect faces in the video stream, crop the face, and send it as binary to the local broker
```
python3 detect_face.py
```

## Capture faces
Now we can either have someone or put a picture with a human face in front of the camera and their faces will be captured and stored on the cloud storage automatically

## Tear down the bucket and delete VSI 
