# Homework 4

## Part 1

The first part of homework 4 is to submit the answers to the following questions about ConvenetJS MNIST demo

### ConvnetJS MNIST demo
In this lab, we will look at the processing of the MNIST data set using ConvnetJS. This demo uses this page: http://cs.stanford.edu/people/karpathy/convnetjs/demo/mnist.html The MNIST data set consists of 28x28 black and white images of hand written digits and the goal is to correctly classify them. Once you load the page, the network starts running and you can see the loss and predictions change in real time. Try the following:

Name all the layers in the network, describe what they do.
* The first layer is the input layer that just specifies how input will be transformed and pass on to subsquent layers. In our case, no transformation was applied.  
* The second layer is a convlutional layer that first pads the data by length 2 (A total increase of 4 in each axis. So the output's dimension becomes 24+4 x 24+4 x 1), then applies eight filters separately on the input for convolution calculation. After the convolution, the output takes the dimension of 24x24x8. The depth of 8 comes from applying eight filters. At the end, relu is applied as the non-linear transformation. Therefore, all light gray pixels were blackened.
* The third layer is a pooling layer which pulls the max value of two adjacent pixels. Since there's a stride of 2, no same pixel is process twice, and as a result, the x and y dimensions were halved in length (12x12x8).
* The fourth layer is another convolutional layer, which pretty much does the same thing as layer 2. However, it applies 16 5x5x8 filters on its input results in an output of 12x12x16 in dimension.
* The fifth layer is the second pooling layer that performs the simiar operation as the last pooling layer but pools three pixels at a time and has a stride of 3. We can see that the model going from processing more detailed, localized features to more broad regional features gradually.
* The last layer is a softmax layer that takes in the output from the fifth layer (total of 256 input)run through a fully-connected layer (ten outputs, the same number as the number of classes in our problem). Softmax function (transformation) is applied and the class that has the highest probability is selected as the prediction.

Experiment with the number and size of filters in each layer. Does it improve the accuracy?
> When adding numbers (to 16 filters in the first conv layer and 24 filters in the second conv layer) of filters, the model training and validation runs slower and the validation accuracy dropped. When suggests that the model is overfitting the training set. On the other hand, in contrast, when lowering the number of fileters (4 filters in the first conv layer and 8 fileters in the second conv layer), the model runs faster and the accuracy didn't change much.  
> When increasing the filter size to 7x7, the model performace dropped. I observed that in the visulization, having big filters made the output of the conv layers too blurry.
> When decreaing the filter size to 3x3, the model performance increased and ran faster. The visualization of the conv layer output is more clear and model was able to achieve over 99% of accuracy in some validation rounds after seeing more than 20000 examples.

Remove the pooling layers. Does it impact the accuracy?
> Surprisingly, the accuracy seems to remain the same or even improved by 1%. 

Add one more conv layer. Does it help with accuracy?
> Add another conv layer before the original first conv layer with 4 filters, also doesn't seem to have much effect on the accuracy.

Increase the batch size. What impact does it have?
> This slows done the updates and model training. But the error curve has less fluctuations since the model is making more prudent moves for each update.

What is the best accuracy you can achieve? Are you over 99%? 99.5%?
Over 99.5% in some rounds after lowering the filter size.

## Part 2

Please see [w251_homework04.html](https://github.com/erikhou45/w251-assignments/blob/master/hw4/w251_homework04.html)
