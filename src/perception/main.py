from .object_detection_tensorflow import find_item as find_item_predefined
from .object_detection_canny_edge import find_item as find_item_fallback

from cozmo.util import degrees


def find_item(img,  detection_graph, tensor_dict, sess):
    item = find_item_predefined.find_item(img, detection_graph, tensor_dict, sess)
    # if item is None:
    #     print("object detection using edge detection")
    #     item = find_item_fallback.find_item(img)
    # else:
    # print("object detection using tensorflow")
    return item


def is_close(obj, img):
    _, y, _, h = obj
    height, _, _ = img.shape
    # at the bottom
    return (y + h) >= (height - 40)

