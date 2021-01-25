from navigation import main as navigation
from cozmo.util import distance_mm, speed_mmps, degrees, Pose


async def manipulate(robot):
    await robot.drive_wheels(20, 20, duration=5)
    await robot.turn_in_place(angle=degrees(180), speed=degrees(60)).wait_for_completed()
    await navigation.go_to_start_position(robot)
