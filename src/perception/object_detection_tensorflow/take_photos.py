# script used to take photos using Cozmo camera
# Resource https://github.com/whatrocks/cozmo-tensorflow/blob/master

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import sys
import os

# GLOBALS
liveCamera = True

def on_new_camera_image(evt, **kwargs):
    category = sys.argv[1]
    global liveCamera

    if liveCamera:
        image = kwargs['image'].raw_image
        image.save(f"data/{category}/{category}-1.jpg", "JPEG")
        liveCamera = False

def cozmo_program(robot: cozmo.robot.Robot):
    category = sys.argv[1]

    # Make sure Cozmo's head and arm are at reasonable levels
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()

    print(f"taking photos of {category}")

    # Set directory to the Category that Cozmo is going to photograph
    if not os.path.exists(f'data'):
        os.makedirs('data')
    if not os.path.exists(f'data/{category}'):
        os.makedirs(f'data/{category}')

    # Anytime Cozmo sees a "new" image, take a photo
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

    # And we're done here
    robot.say_text("All done!").wait_for_completed()


def main(argv):
    argc = len(argv)
    if argc != 1:
        print("usage: take_photos.py <object>")
        exit()
    cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)

if __name__ == "__main__":
    main(sys.argv[1:])
