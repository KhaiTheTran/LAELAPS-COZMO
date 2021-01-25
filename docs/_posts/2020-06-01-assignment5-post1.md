---
layout: post
title:  "A5 Post #1: Progress Update"
date:   2020-06-01
---

[Demo video](https://youtu.be/66z3ZhOVjrA)

It shows Cozmo searching for an object by circling around, drives toward the 
object while it’s in view, and drives back to the starting point. After attaching our manipulator, everything should work. 

### Perception - Cynthia 
Last week, we spent hours tuning parameters on our object detection algorithm using edge detection, but the 
performance is still unsatisfactory. After some googling online, we came across this [tutorial](https://blog.floydhub.com/teaching-my-robot-with-tensorflow/). 
It inspired us to take advantage of machine learning models to do object detection. We use Cozmo to take pictures of 
objects on a surface ([script](https://github.com/starry97/cse481c-project/blob/master/src/perception/object_detection_tensorflow/take_photos.py). 
We took 144 photos of four types of items: keys, pen caps, chargers and dog toys, and manually labeled the object in 
each image, using a tool named [labelImg](https://github.com/tzutalin/labelImg). Since we want to detect all types of 
objects on a surface, we gave different types of objects the same label.  We then randomly split our images into 
training (119 images) and test set (25 images). Instead of creating our own model, we selected the fastest tensorflow 
objection detection model from their [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) 
,ssd_mobilenet_v1_coco, and fine-tune this model using our dataset to solve our problem.

#### Results
After training and fine-tuning, our test accuracy is 19/25 = 76%. With the same test images, the previous version has 
an accuracy of 56% (only successfully detected 14 images out of 25). Compared to our previous version, it is 
significantly better at detecting objects in a noisy background. We are able to loosen our previous assumption that 
the target object must be in an uncluttered environment. 
![object_in_clutter](https://starry97.github.io/cse481c-project/assets/a5-perception.jpg)


Though we only trained the model on four types of objects, it’s able to detect items outside the training data. 
For example, it’s able to detect this eraser on the floor. [Video](https://youtu.be/P0uWCCLpQgo)

### UI - Cynthia 
This is still a work-in-progress. Using Flask, we are able to expose a REST API starting the program to run Cozmo. 
Ideally, we want to redirect the video stream from its camera to our web page, but we haven’t figure out how to do it. 
Currently, we have one button that starts the Cozmo to find and retrieve an object. We will keep on improving this UI 
and provide feedback on what the robot is doing, which state it is in etc. 

![ui](https://starry97.github.io/cse481c-project/assets/a5-ui.jpg)

### Navigation - Khai
Test Cozmo navigates to the object and goes back to the start position
Add Search functionality, so Cozmo circles around when no item can be found

[Video Demo](https://www.youtube.com/watch?v=o50NG1CFeoQ)

TODO:
Test Cozmo navigates to the object and goes back to the start position by using tensorflow for object detection.

### Manipulation - Saketh
Notes: Had to move from tissue box cardboard to thicker cardboard as the lift was bending too easily and losing the object. Had to rely on duct-tape rather than plain tape for the same reason. Also chose the tape holder as a stand-in for our heavy object as it is both larger in terms of surface area and weight than all the items in our test set, so if the lift can handle it it's good to go for everything else.

Design 1: Fully Connected Lift, Obstructs View when Down

Algorithm Adjustments: On startup the robot must raise the lift so that it can properly 
see. Then when it acquires the object it can lower it’s lift and the go-to-pose’s dead 
reckoning will allow it to return to the origin without being able to see
	
Results: Works fairly well. Robot does have to be close enough to the object, and in 
some circumstances the rotation can dislodge the object from the robot’s control, 
although this is rare. Cannot grab larger objects because of the smaller width. This is 
why I did not include a heavy demo video here
	
[Video Demo](http://youtube.com/watch?v=yhM8oInC8GU&feature=youtu.be)

![img](https://starry97.github.io/cse481c-project/assets/a5-manipulation1.png)


Design 2: U-Shaped Unobstructing Lift Attachment

Results: Works even better than Design 1, can even rotate heavier things like a tape 
holder. Although the heavier objects get dislodged around 50% of the time as the lift 
bends under the stress. Pretty reliably handles smaller and lighter objects like keys, in all 
the tests, the keys never got dislodged.
	
[Video Demo](https://youtu.be/PnW4ZF7TrTg)
	
[Video Demo Heavy](https://youtu.be/-6ke-xavHog)

![img](https://starry97.github.io/cse481c-project/assets/a5-manipulation2.png)
	
Design 3: Rectangular Sticky Attachment

Results: Work extremely well, almost always sticks onto the object and offers freedom to 
move it. Requires the same thinking as Design 1, need to keep the lift up during search 
as otherwise the tape obstructs our view. Also sometimes it can be a bit tricky to get the object of the lift without tearing the tape off, more of a problem for larger objects.
	
[Video Demo](https://youtu.be/ZkRcE3CWqic)
	
[Video Demo Heavy](https://youtu.be/bRl0W8Xt8D4)

![img](https://starry97.github.io/cse481c-project/assets/a5-manipulation3.png)
	
Design 4: Rectangular Sticky Attachment with hole cut out for viewing

Results: Can successfully capture objects the vast majority of the time, without the need 
for keeping the lift up, however it has a significantly harder time grabbing larger objects 
due to the decreased surface area. Also sometimes it can be a bit tricky to get the object 
of the lift without tearing the tape off, more of a problem for larger objects.

[Video Demo](https://youtu.be/ODnEMad9pOg)
	
[Video Demo Heavy](https://youtu.be/yPy9NLOMdc4)

![img](https://starry97.github.io/cse481c-project/assets/a5-manipulation4.png)

Conclusion: The lift attachment we will use going forward is Design 4, with Design 2 as a backup strategy. Although this design failed our tests with the tape holder, it will likely function well for the large majority of our objects, so far it has worked with keys, phone chargers, and moderately well with pen caps. We think this design will be suitable for the large majority of our planned functionality, and if there are issues we think they can be solved with minor optimizations on top of this design. If there are major problems we run into while using Design 4, we can swap over to Design 2 as that is pretty good as well, working well with a large portion of the objects we wanted to test even if it only performed 50% of the time under the stress test of rotating the tape holder.



