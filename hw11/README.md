# Homework 11

## Videos
Six sets of parameters were attempted. Three of the sets of parameters with completed training:
(All of the training and testing videos were uploaded but I sampled some accroding to the homework instrcutions and linked below)

1. dense layer 1: 200 nodes, dense layer 2: 100 nodes. Everything else is default:  
> Initial training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100/episode0.mp4
> Intermediate training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100/episode250.mp4
> Final training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100/episode470.mp4

> Testing videos: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100/testing_run90.mp4

2. dense layer 1: 200 nodes, dense layer 2: 100 nodes, epsilon: 0.99 Everything else is default:
> Initial training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100_0.99/episode0.mp4  
> Intermediate training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100_0.99/episode250.mp4  
> Final training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100_0.99/episode330.mp4

> Testing videos: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_200_100_0.99/testing_run90.mp4

3. dense layer 1: 150 nodes, dense layer 2: 75 nodes, epsilon: 0.99, learning rate: 0.003. Everything else is default:
> Initial training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_150_75_0.003_0.99/episode0.mp4  
> Intermediate training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_150_75_0.003_0.99/episode250.mp4  
> Final training: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_150_75_0.003_0.99/episode430.mp4

> Testing videos: http://s3.us-east.cloud-object-storage.appdomain.cloud/erik-w251-hw3-bucket/videos_150_75_0.003_0.99/testing_run90.mp4


## Questions

1. What parameters did you change?
> I tried to changed the number of nodes in the dense layers, the learning rate and the epsilon decay value.
2. What values did you try?
> Learning Rate: I tried 0.001, 0.003, 0.005, 0.007.
> Nodes in the dense layers: (200, 100) and (150,75).

3. Did you try any other changes that made things better or worse?
> I also tried changing epsilon decay from 0.995 to 0.99 which seems to speed up the training and make the model more stable at the end of training when everything else is equal.

4. Did they improve or degrade the model? Did you have a test run with 100% of the scores above 200?
> There isn't any significant change observed when the number of nodes were changed from (200, 100) t
o (150, 75). However, when learning rate was changed to 0.007, the model seemed to be too unstable (probably learning too much from a small batch of size 64).
> I was not able to achieve a test run with 100% of the scores above 200. The best run still had four test episode lower than 200 (196, 196, 195, 90).

5. Based on what you observed, what conclusions can you draw about the different parameters and their values?
> I think as long as the number of nodes in the dense layer provides the network enough capacity to remember the training examples and gradually train to make good approximation of the Q-value, it shouldn't have too much impact on the performance of the agent. However, bigger model might take longer to train.  
> As to learning rate, it is important to recognize though larger learning rate prompts the model to learn faster, when it is too large, the model will be unstable and fail to converge. I think the learning rate could be set in conjuction with the batch size (e.g., when we train on larger batches, we could potentially raise the learning rate more since now each update should have more useful information and less contradicting information). Lastly, I think this network could potentially benefit from warm-up in the learning rate. Since in the beginning of the training, everything is shifting very quickly including the target itself, therefore, baby-steps should be taken. It is the middle part of the training that could potentially benefit from a larger learning rate for acceleration in training without much sacrifice in performance. 

6. What is the purpose of the epsilon value?
> Epsilon is the parameter that controls how much the model will explore a random action when training. The model is in full exploration mode when the training is just started since there is no previous experience in the memory that the model can draw from (epsilon starts with 1.00). Then as the agent accumulates more examples of its past moves, the network model starts to exploit those experience in training and explore randomly less (the epsilon is reduced by multiplying the epsilon decay parameter). I observed that the model since to be more stable when using the epsilon decay of 0.99 than 0.995. I think it might be beneficial to have epsilon value lower (i.e., to have the model mainly exploit and make better approximation of the Q-value of good moves) towards the end of training. This stragey seems to result in more stable agent that has stable test rewards.

7. Describe "Q-Learning"
> Q-Learning is a type of reinforcement learning that has a agent which approximates the reward of a given (state, action) pair (this potential reward is called a Q-value) and uses that approximation to make decision on which action to take when given a state (the agent will select the action which it predicts can maximize reward). The general strategy of the Q-Learning is to explore different state-action pair and keep modify the agent's approximation for the rewards based the feedback from the envrionment. This updated approximation then will be stored in the agents memory and (as model weights in the example of DQN) for exploitation or further exploration in the future. There are different ways in which a Q-Learning agent can implement the approximation. In this this homework we have a DQN (deep Q-learning) agent which approximates the reward of a given state-action pair with a deep nerual network.  
