import cv2

import os
import numpy as np
import glob
from PIL import Image

import tensorflow.compat.v1 as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from matplotlib import pyplot as plt
import find_item


path = os.path.dirname(os.path.realpath(__file__)) + "/"

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = path + MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = path + 'training/object-detection.pbtxt'

PATH_TO_TEST_IMAGES_DIR = './data/train'
IMAGE_SIZE = (12, 8)


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def test_object_detection_image():
    i = 0
    res = []
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

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

            for image_path in glob.glob(PATH_TO_TEST_IMAGES_DIR + '/*.jpg'):
                image = Image.open(image_path)
                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = load_image_into_numpy_array(image)

                # Actual detection.
                output_dict = find_item.find_item_annotate(image_np, detection_graph, tensor_dict, sess)
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    output_dict['detection_boxes'],
                    output_dict['detection_classes'],
                    output_dict['detection_scores'],
                    category_index,
                    instance_masks=output_dict.get('detection_masks'),
                    use_normalized_coordinates=True,
                    line_thickness=8)
                # plt.figure(figsize=IMAGE_SIZE)
                # plt.imshow(image_np)
                # img = Image.fromarray(image_np, 'RGB')
                # img.show()
                i += 1
                # im1_s = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)
                res.append(image_np)
                if i > 99:
                    break

    return res



def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


def main():
    images = test_object_detection_image()

    res = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            row.append(images.pop())
        res.append(row)

    # im_tile = concat_tile([[im1_s, im1_s, im1_s, im1_s],
    #                        [im1_s, im1_s, im1_s, im1_s],
    #                        [im1_s, im1_s, im1_s, im1_s]])

    im_tile = concat_tile(res)
    cv2.imwrite('data/opencv_concat_tile.jpg', im_tile)


main()