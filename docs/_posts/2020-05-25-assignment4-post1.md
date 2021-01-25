---
layout: post
title:  "A4 Post #1: Progress Update"
date:   2020-05-25
---

This week, we focus on implementing our MVP.  Here’s a video showing our robot attempting to retrieve keys, in a 
fairly isolated environment. [Demo here](https://www.youtube.com/watch?v=o50NG1CFeoQ). In this simplified scenario, 
Cozmo started out facing the target object, it is able to detect the object, navigate toward it and push it back to 
the starting position. Links to our code 
[here](https://github.com/starry97/cse481c-project/tree/master/src).
 
### Perception Update - Cynthia
This week, we experimented with different object detection algorithms and further optimized the most performant 
algorithm by manually tuning hyperparameters. 

We narrowed down a list of objects for testing. 
- keys
- cell phone chargers
- pen caps
- dog toys/tennis balls

These objects are selected because they are common items people drop. They have different sizes and shapes, at the same 
time they are small and light enough to be manipulated by Cozmo. 

We took 25 pictures of our targeted objects from different angles and in different lighting conditions. 
Below are some examples:

![test objects](https://starry97.github.io/cse481c-project/assets/a4-perception-test-objects.jpg)

We improved last week’s object detection algorithm to work with photos taken by Cozmo. The new algorithm works with 
different lightning conditions by changing contrast and brightness, and additionally it filters out straight lines to 
reduce noise from furniture and floor. We then use these 25 pictures to further tune hyperparameters. It turned out to 
be more challenging to do object detection using the Cozmo camera because of low resolution. We are able to 
successfully detect 16 images (accuracy 64%). 

Some issues we are seeing:
- Images too dark or too bright
    - it’s difficult to adjust parameters that work in all lighting conditions
- Difficult to detect small objects
    - We observe that accuracy is especially low when detecting pen caps. It’s difficult to distinguish between small 
    objects and noise in the following image, the black rectangle is what our algorithm thinks the target object is, 
    and the white rectangles are two other possible candidates. Though the target object is detected, our algorithm 
    thinks the lower-left object is larger and closer, therefore more likely to be the target.
 
        ![small object](https://starry97.github.io/cse481c-project/assets/a4-perception-small-object.jpg)


- Difficult to detect objects in rectangle shapes, because we filter out edges that could be furniture or floor.
    - When detecting cell phone chargers, only the metal part is detected. It falsely filters out the body of the charger 
    because its edge consists of straight long line
    
        ![charger](https://starry97.github.io/cse481c-project/assets/a4-perception-charger.jpg)
    
    
- Sensitive to noise.
  
    ![noise](https://starry97.github.io/cse481c-project/assets/a4-perception-noise.jpg)


#### Next steps
I feel like the result is not very satisfactory. It definitely won’t work well in the real world. Another thought is we 
can use tensorflow to train Cozmo to recognize a predefined set of objects, and if none of these are detected, we can 
fall back to use edge detection. I still need to experiment with it.

### Navigation - Khai
This step, we focus on how to navigate to the items which users want to pick up for them. The goal is Cozmo can pick up 
anywhere, but we are testing for Cozmo picking up items in an isolated environment. This step will help us to have more 
experience to program Cozmo to pick items which are far from the position. Cozmo will turn around to find the familiar 
item, and navigate to the exact location to pick up and turn all the way back to the start position.

[Video Demo 1](https://www.youtube.com/watch?v=j747YR2vNS4)

[Video Demo 2](https://www.youtube.com/watch?v=o50NG1CFeoQ)
#### Issues
- Cozmo can not go to the items so far away

### Manipulation - Saketh
Added a wider sideguard to the lift to address some of last week's problems. Now Cozmo can move larger objects.
This lift is not fully functional on carpeted surfaces, as the motion of the lift across the rough surface of the carpet 
can cause the tape attaching to the robot to get detached. However, for our MVP we are assuming that Cozmo operates on 
a smooth surface,

Pictures of some new objects we tested with this week, and sample designs.
![example1](https://starry97.github.io/cse481c-project/assets/a4-manipulation-example1.jpg)
![example2](https://starry97.github.io/cse481c-project/assets/a4-manipulation-example2.jpg)

#### Takeaways
While it is technically true that we can make wider and wider lifts to capture wider objects, the problem is that these 
wider lift designs are not as stable and tend to rip off more easily. Therefore going forward we can either keep the 
wider lifts but figure out a stronger material and design to use for them, or we can compromise and scale our lift 
width down a little bit, but still enough to capture all the objects in our test set (Maybe by revising some of our 
assumptions about the environment and objects)

#### Next Steps:
One strategy that we are going to try next are having a singular U shaped piece of cardboard attached to the front of Cozmo because this design is more stable. However since this approach obstructs our camera, the Cozmo lift will be raised during the initial perception and navigation to the object. However one Cozmo reaches the object we will lower the lift which obstructs the camera. At this point, we will have to rely on a strategy like dead-reckoning or something similar to return to the user. 
