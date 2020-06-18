Describe your solution in detail. What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
* My solution is by swapping out the cv2.CascadeClassifier in hw3 with [Tensorflow Face Detector](https://github.com/yeephycho/tensorflow-face-detection). It is trained by [WIDERFACE dataset](http://shuoyang1213.me/WIDERFACE/).

Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
* Yes, the model works well. It can detect faces even when they are blurry. 

What framerate does this method achieve on the Jetson? Where is the bottleneck?
Which is a better quality detector: the OpenCV or yours?
* I was able to get 10 fps. It seems like the neural model slows the system downa bit since I get 24-30 fps for OpenCV when using the same way to meausre frame per second. The neural model definitely works better, especailly when the faces are small and blurry.
