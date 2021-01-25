from cozmo.util import degrees, Pose


async def move_to(robot, item, image):
    motor_left, motor_right = get_motor_speed(item, image)
    # drive for 3s
    await robot.drive_wheels(motor_left, motor_right, duration=3)


async def go_to_start_position(robot):
    await cozmo_go_to_pose(robot, 0, 0, 180)


async def cozmo_go_to_pose(robot, x, y, angle_z):
    await robot.go_to_pose(Pose(x, y, 0, angle_z=degrees(angle_z)), relative_to_robot=False).wait_for_completed()


def get_motor_speed(item, camera_image):
    x_pos = item[0]
    x_image = camera_image.size[0] / 2

    speed_right_diff = 0
    speed_left_diff = 0
    if x_pos < x_image:
        # image on the left side, right wheel needs to be faster
        speed_right_diff =  (x_image - x_pos) / 10
    elif x_pos > x_image:
        speed_left_diff = (x_pos - x_image) / 10
    return 20 + speed_left_diff, 20 + speed_right_diff

async def search(robot):
    await robot.turn_in_place(degrees(45)).wait_for_completed()