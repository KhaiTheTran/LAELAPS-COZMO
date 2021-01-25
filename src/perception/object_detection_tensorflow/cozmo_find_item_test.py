# https://github.com/IBM/visual-recognition-for-cozmo-with-tensorflow

import cozmo
from cozmo.util import degrees
import os
import numpy as np
import tensorflow as tf


import find_item


path = os.path.dirname(os.path.realpath(__file__)) + "/"

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = path + MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = path + 'training/object-detection.pbtxt'

PATH_TO_TEST_IMAGES_DIR = './data/test'


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

            itemAnnotator.item = None


async def run(robot: cozmo.robot.Robot):
    robot.world.image_annotator.add_annotator('item', itemAnnotator)
    await robot.set_head_angle(degrees(10.0)).wait_for_completed()
    await robot.set_lift_height(0.0).wait_for_completed()


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


            # processing = False
            while True:
                # if not processing:
                event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)

                opencv_image = np.asarray(event.image)

                # processing = True
                item = find_item.find_item(opencv_image, detection_graph, tensor_dict, sess)
                # processing = False

                itemAnnotator.item = item




cozmo.run_program(run, use_viewer=True, force_viewer_on_top=True)