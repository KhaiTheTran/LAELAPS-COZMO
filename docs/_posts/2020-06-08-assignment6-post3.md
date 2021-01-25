---
layout: post
title:  "A6 Post #3: Mini Evaluation"
date:   2020-06-08
---

### Environment 1: living room; objects under a TV console

| Objects | Success rate (out of 10 trials) | Detection success rate | Manipulation success rate |
| -------- | --------------------------------- | ------------------------ | --------------------------- |
|Dog toys| 80% | 80% |100%|
|Pen caps|60%|70%|86%|

#### Retrieve Pen Caps
![pen caps](https://starry97.github.io/cse481c-project/assets/a6-evalulation-retrieve_pen_caps.jpg)

#### Retrieve Dog Toys
![dog toys](https://starry97.github.io/cse481c-project/assets/a6-evaluation-retrieve_dog_toys.jpg)

### Environment 2: dining room; objects under a table

| Objects |Success rate (out of 10 trials) | Detection success rate | Manipulation success rate |
| -------- | ----------------------------- | ----------------------- | ------------------------- |
| keys | 70% | 70% | 90% |

#### Retrieve Keys
![keys](https://starry97.github.io/cse481c-project/assets/a6-evaluation-retrieve_keys.jpg)

### Summary

| Success rate (out of 30 trials) | Detection success rate (out of 30 trials) | Manipulation success rate (out of 22 trials, where detection is successful) |
| ------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------- |
| 70% | 73% | 91% |


### Observations

It works best when the target object is large, but light. This is because larger items 
are easier to detect, and lighter items are easier to manipulate. The Perception success 
rate is lower when objects are small or far away, because it’s difficult to differentiate 
between the target objects and noise. Manipulation works very well, especially for light 
objects. However, sometimes the sticky attachment may stick to the wall or furniture. 
For heavier objects, sometimes Cozmo doesn’t go back to its starting position. From our 
observation, perception works better when the object is directly in front of a wall, because 
there’s less noise. 
