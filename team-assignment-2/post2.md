## Assumptions
To make our implementation more feasible, we will make the following assumptions:
Object is next to the wall (Easier to Lift)
the target object is the only object under the furniture 

## Navigation
When Cozmo turns on, it seeks darkness using Braitenberg’s behavior, this could be a good heuristic for navigating under furniture. Once it is in a significantly dark area, another heuristic for being under furniture, it will rotate from side to side, ensuring that it is not facing in a direction that leads out of the furniture, to find the object. Once we have picked up the object, we will use Braitenberg’s behavior to seek out the light.

- Ability to navigate in dark and daylight
  - we can attach a light source to the robot
- Ability to navigate towards dark areas
    - Reuse Braitenberg behavior code
- Ability to drives around, and drives toward an object
    - We can refer to Lab 6 and Lab 7
    - Functions we might use
    `robot.turn_in_place(degrees(degree))`
    `robot.drive_straight(distance_mm(distance), speed_mmps(speed))`

### Perception
- Detect furniture
    - Refer to lab 3 Braitenberg to detect brightness changes, to indicate Cozmo is under furniture. 
    - Functions we might want to use
    `sense_brightness(image, columns)` in `braitenberg.py`
- Detect objects under furniture (might be in the dark)
In the course of its rotations, it will perform an edge detection algorithm to detect things that are not corners or the edge between floor and wall, as this will likely be the object we want.
To simplify our problem, we will assume the object is next to a wall, and the target object is the only object under the bed/sofa
- Needs to do edge detection
    - We can refer to Lab 4 and Lab 5 for edge detection and image processing
    - We will use `opencv` for image processing

### Manipulation
- Ability to move objects
    - Build a forklift attach for Cozmo so that it can pick up objects
    - We can try attaching a magnet and experiment with other modifications to make this task easier
    -  We will refer to Lab 8. 
        - `robot.set_lift_height(height)` to pick up / drop off objects
        - `robot.drive_straight(distance_mm(distance), speed_mmps(speed))` to push objects around

### Other capabilities
- Can use the same technology to retrieve items on a table for people who are unable to or hard place to get them
- Can also use the same technology to be a “Fetch” robot, to play with kids or help people and pets exercise

### External devices
We explored two paths to implement this product. One path is a Remote Control App on iOS/Android. In the App, we get a forwarded feed from Cozmo’s camera, and we have buttons that allow us to have Cozmo change its head position, rotate in place, move forward, and move its lift. Cozmo will be like a remote “arm” that the users control through their phone, rather than an autonomous agent. The advantage of this approach is it’s flexible. We don’t need to implement detection of different objects. However, we are not sure if it’s easy to connect Cozmo to our own mobile app.  

Another path is to make assumptions about the size and shape of objects we want to retrieve. We will attach a light source to Cozmo and use Cozmo built-in camera for object detection. As an MVP, we will pick this path, and Cozmo will pick up the first object it sees under furniture. 
