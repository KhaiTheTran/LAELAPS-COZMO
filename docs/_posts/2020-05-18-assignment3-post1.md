---
layout: post
title:  "A3 Post #1: System Diagram"
date:   2020-05-18
---

### System Diagram
![system diagram](https://starry97.github.io/cse481c-project/assets/a3-system-diagram.jpg)

### Assumptions
- Cozmo starts off at position where we want it to return to
- The target object is the only thing on the floor
- Smooth surface
- Object is small and light enough

### Team Responsibilities
- Khai: Navigation
    - Navigating to our object
    - Returning to User
- Cynthia: Perception, UI. 
    - Detecting the object
    - Providing feedback to users
- Saketh: Manipulation. 
    - Being able to move the object

### Components
- Detecting our object (Perception): high priority [Cynthia]
    - When Cozmo starts off, it rotates in a circle until it detects the object
    - Use edge detection. If it sees edges that aren’t part of the floor or where it meets the wall, it’s likely an object.
    - If no object can be detected, notify user: secondary  [Cynthia]
- Move to our object (Navigation): high priority [Khai]
    - Use the same methods that we used in Lab 6 (`goto_ball.py`)
- Pick up objects (Manipulation): high priority [Saketh]
    - Pick up the only objects on the floor or table
    - Assuming smooth surface for now, because rough surface may be more challenging
- Keeping objects in a stable position so they don’t fall (Manipulation): secondary [Saketh]
    - Adding Walls to each side, so that the object it’s pushing doesn’t slip out of its path
- Detecting dropped objects and re-picking them up (Perception/Navigation): secondary [Khai\Saketh]
- Return objects to user (Navigation/Perception): high priority [Khai\Cynthia]
    - Drop off objects to Cozmo’s starting position
    - Use `cozmo_go_to_pose()` to go to starting position
- UI: secondary priority [Cynthia] 
    - It can be a simple command-line user interface, or a web interface if time permits. It’s used to provide feedback 
    to users, at the same time allowing users to abort the running program.
- Hardware: we don’t need to use additional hardware for our project. It’s possible we may need to attach a flashlight 
to navigate and detect in the dark, but it may not be necessary. 
