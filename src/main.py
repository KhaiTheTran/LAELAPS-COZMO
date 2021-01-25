import random

import cozmo
from cozmo.util import distance_mm, speed_mmps, degrees, Pose
from PIL import ImageDraw, ImageFont
import cv2.cv2 as cv2
import numpy as np
import tensorflow.compat.v1 as tf
import os
from perception import main as perception
from navigation import main as navigation
from manipulation import main as manipulation


# from object_detection_edge import find_item
path = os.path.dirname(os.path.realpath(__file__)) + "/"

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = path + "perception/object_detection_tensorflow/" + MODEL_NAME + '/frozen_inference_graph.pb'


# Define a decorator as a subclass of Annotator; displays the item
class itemAnnotator(cozmo.annotate.Annotator):
    item = None

    def apply(self, image, scale):

        if itemAnnotator.item is not None:
            #define and display bounding box with params:
            #msg.img_topLeft_x, msg.img_topLeft_y, msg.img_width, msg.img_height
            box = cozmo.util.ImageBox(itemAnnotator.item[0] * scale,
                                      itemAnnotator.item[1] * scale,
                                      itemAnnotator.item[2] * scale,
                                      itemAnnotator.item[3] * scale)
            cozmo.annotate.add_img_box_to_image(image, box, "green", text=None)

            # itemAnnotator.item = None


async def run_fetch(robot: cozmo.robot.Robot):
    '''The run method runs once the Cozmo SDK is connected.'''

    robot.world.image_annotator.add_annotator('item', itemAnnotator)

    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    with detection_graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                        tensor_name)

            search_count = 0

            await robot.set_lift_height(0.9).wait_for_completed()
            await robot.set_head_angle(degrees(0.0)).wait_for_completed()


            while True:
                item = None
                opencv_image = None

                for _ in range(5):
                    # get camera image
                    event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)

                    # convert camera image to opencv format
                    curr_opencv_image = np.asarray(event.image)

                    # find the item
                    curr_item = perception.find_item(curr_opencv_image, detection_graph, tensor_dict, sess)

                    if curr_item is not None:
                        item = curr_item
                        opencv_image = curr_opencv_image
                        break

                itemAnnotator.item = item

                if item is None:
                    print("[EVENT] Did not find item in view")
                    if search_count < 16:
                        print("[STATE] Search")
                        await navigation.search(robot)
                        search_count += 1
                    else:
                        print("[EVENT] Cannot find object")
                        print("[EVENT] Terminated")
                        break
                else:
                    print("[EVENT] Find item", item)
                    search_count = 0

                    if perception.is_close(item, opencv_image):
                        print("[STATE] Manipulate")
                        await robot.set_lift_height(0.0).wait_for_completed()
                        await manipulation.manipulate(robot)
                        print("[EVENT] Succeeded")
                        break
                    else:
                        print("[STATE] Move-to")
                        await navigation.move_to(robot, item, event.image)

def fetch():
    cozmo.run_program(run_fetch, use_viewer=True)


if __name__ == '__main__':
    fetch()
