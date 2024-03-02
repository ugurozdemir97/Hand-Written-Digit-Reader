# What is this program?
Using Numpy, I had written an artificial intelligence that learned to read the numbers in the MNIST dataset. See:
https://github.com/ugurozdemir97/MNIST-Neural-Network-from-scratch
I got a lot of help from the internet while doing that. Therefore, I wanted to add something original in it and integrated the artificial intelligence from that software into a GUI program. I've used that program to train the neural network and this program uses those trained weights to predict the digits that you have written. These weights have a success rate of 93% with MNIST dataset but fails more with my hand written digits. But if you wish, you can train the network by writing the correct answer to "Teach" section before sending your drawing. So if you use "Teach" section enough times this program will eventually be able to predict your hand writing with a much better rate.

# What it does
In this program you can write your own digits on the black canvas with mouse and after you click "Send" it will show its prediction on the top right. Writing the correct answer in "Teach" section before sending the drawing will train the neural network. It will still try to predict and won't know what you have written there so it may not answer correctly even though you write the answer :D

# How does it work?
This program simply takes your drawing and converts it (in terms of image and resolution) into the data resembles the data in MNIST dataset. You will see a "temporary.png" in the folder when you send a digit. In this way, artificial intelligence can recognize your drawing as a data from MNIST which is what it's trained for to predict and make predictions. Moreover, it is possible to train artificial intelligence with your drawings. After you close the program the temporary image will be deleted.
