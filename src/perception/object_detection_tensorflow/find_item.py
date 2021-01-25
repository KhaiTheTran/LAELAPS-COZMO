import numpy as np
import os
import tensorflow.compat.v1 as tf


from distutils.version import StrictVersion
from object_detection.utils import label_map_util


# https://towardsdatascience.com/creating-your-own-object-detector-ad69dda69c85

from object_detection.utils import ops as utils_ops



path = os.path.dirname(os.path.realpath(__file__)) + "/"

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = path + MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = path + 'training/object-detection.pbtxt'

SCORE_THRESHOLD = 0.5

# only returns bounding box
def find_item(image, graph, tensor_dict, sess):
    output_dict = find_item_annotate(image, graph, tensor_dict, sess)
    bounding_boxes = output_dict['detection_boxes']
    scores = output_dict['detection_scores']

    # it's sorted by score, only return item if we are > 50% confident
    if len(bounding_boxes) > 0 and len(scores) > 0 and scores[0] > SCORE_THRESHOLD:
        im_height, im_width, _ = image.shape
        ymin, xmin, ymax, xmax = bounding_boxes[0]
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
        width = right - left
        height = bottom - top
        detected_item = (int(left), int(top), int(width), int(height))
        return detected_item
    return None



def find_item_annotate(image, graph, tensor_dict, sess):
    if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, SCORE_THRESHOLD), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
    # image_tensor = 'image_tensor:0'

    # Run inference
    output_dict = sess.run(tensor_dict,
                           feed_dict={image_tensor: np.expand_dims(image, 0)})
    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict

