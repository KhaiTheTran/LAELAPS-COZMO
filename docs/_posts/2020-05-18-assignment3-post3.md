---
layout: post
title:  "A3 Post #3: Progress Update"
date:   2020-05-18
---

### Perception Update - Cynthia

[Source code](https://github.com/starry97/cse481c-project/tree/master/src/perception)

One unique challenge our project has is our robot should be able to work with various objects. Training the robot to 
recognize a number of objects seems unrealistic. Though there are some existing libraries that can perform object 
detection on images for a set of predefined objects, we think this solution lacks extensibility. One potential library 
we explored is ImageAI (http://imageai.org). It’s able to detect 80 common objects, but extending it to support custom 
objects is difficult and time-consuming. Instead, we will use edge detection and various heuristics to implement object 
detection for this project. We use `opencv` to process images. This week, we took a few pictures of various items on 
different surfaces, and detected objects from these static images. We will walk through what the process looks like for 
the following image. 

Original image:
![original image](https://starry97.github.io/cse481c-project/assets/a3-perception-original.jpg)

First, we need to transform this image to gray-scale. We blur the image using gaussian blur to reduce noise. We then use 
Canny detection to extract edges by calling `cv2.Canny()`.
 
After edge detection:
![edge](https://starry97.github.io/cse481c-project/assets/a3-perception-edge.jpg)

From the image above we can see we still have some noise, like edges and patterns of the wood floor. Since these can 
have different shapes and angles, it’s difficult to filter them out using `cv2.getStructuringElement()`. We observe the 
edges for the targeted object should be closer together, therefore we try to increase the edge width and form a large
contour around the targeted objects. We use the morphological operator `MORPH_CLOSE` here. 

After closing transformation:
![closing](https://starry97.github.io/cse481c-project/assets/a3-perception-closing.jpg)

We then apply two more morphology operations -- `cv2.erode()` followed by `cv2.dilate()`, to remove small contours
 from the image above. It’s difficult to figure out how much we should erode without removing the target object. We 
 still need to tweak some parameters. Our result looks like the image below. 
 
Object contour: 
![contour](https://starry97.github.io/cse481c-project/assets/a3-perception-contour.jpg)

We detect five potential objects. A reasonable heuristics we can use is the largest contour is our target.
![annotated](https://starry97.github.io/cse481c-project/assets/a3-perception-annotated.jpg)

This approach works reasonably well for objects on a uniform and smooth surface.

More examples
![example1](https://starry97.github.io/cse481c-project/assets/a3-perception-example1.jpg)
![example2](https://starry97.github.io/cse481c-project/assets/a3-perception-example2.jpg)


### Navigation Update - Khai

The strategy of navigation is to use the coordinates returned by object detection function
[`find_item`](https://github.com/starry97/cse481c-project/blob/master/src/perception/find_item.py), and drive 
toward the object detected. Similar to `go_to_ball.py` in the lab 6, navigation is down with visual servoing, i.e.
Adjusting the relative speed of the two wheels to center the object in the robot's image.
 
After Comoz picks up the object, it returns back to the starting position(which is pose 0, 0, 0), by calling
`cozmo_go_to_pose()`. We still need to incorporate this with our new lift design.
  
[Demo video](https://www.youtube.com/watch?v=Vd4lvulaJDQ&feature=share)

### Manipulation Update - Saketh
There are a couple strategies we look at for modifying the forklift to manipulate the object

#### Design 1: Side Panels

![design1](https://starry97.github.io/cse481c-project/assets/a3-manipulation-design1.jpg)

##### Pros
- Does not have to rely on using a wall to gain control of the object
- Can rotate the object in place without it getting lost/ falling off
- Object remains relatively stable when being pushed, usually does not fall/ get lost

##### Cons
- Object has to be small enough to fit between the side panels
- Otherwise what I said about objects getting lost does not apply. See the following 
[video](https://www.youtube.com/watch?v=8XAN3SLpjxw&feature=youtu.be)

#### Design 2: Adding a platform to the base of the forklift

![design2](https://starry97.github.io/cse481c-project/assets/a3-manipulation-design2.jpg) 

##### Pros
- Can pick up larger objects than side panel
- In fact this is even relative to its size

##### Cons
- Has to rely on walls to push against to pick up the object
- Striking an obstacle on the way back to the user may dislodge the object
- The object may not be in the most stable position and can fall off

#### Takeaways
In general to be able to manipulate the object effectively and return to the user, the object should be small enough to 
fit on the platform and the robot should avoid any obstacles on the way back to the user, because striking them may 
dislodge the object from it’s grasp. To help us choose which strategy to go with, we will perform A/B testing with the 
two different strategies using various objects, and in various environments (desktop, floor)

