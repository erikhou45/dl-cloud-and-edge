# Homework 9

## Questions

* How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)
> It took 22 hours and 12 minutes
* Do you think your model is fully trained? How can you tell?
> I think there is still room for the model to train more and get better performance because from the eval BLEU score is still increasing constantly and eval loss is still decreasing.
* Were you overfitting?
> Since the model doesn't have the eval BLEU score peaked and then declined or the eval loss started rising after reaching a minimum, I don't think we have overfitting issue with the model. 
* Were your GPUs fully utilized?
> Yes. When running nvidia-smi command, though there is some fluctuation in the GPU usage, it's mostly pretty high and it goes to 100% pretty often.
* Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
> 
* Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
* How big was your training set (mb)? How many training lines did it contain?
* What are the files that a TF checkpoint is comprised of?
* How big is your resulting model checkpoint (mb)?
* Remember the definition of a "step". How long did an average step take?
* How does that correlate with the observed network utilization between nodes?
