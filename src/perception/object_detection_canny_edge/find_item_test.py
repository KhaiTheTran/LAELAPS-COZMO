'''
Output accuracy of our object detection algorithm
'''
import glob
import os
import cv2.cv2 as cv2
import find_item


def object_detection_folder(folder):
    for img_relative_path in glob.glob(folder + '/*.jpg'):
        img_name = os.path.basename(img_relative_path)
        object_detection_single_image(folder, img_name)

def object_detection_single_image(folder, img_name):
    opencv_image = cv2.imread(folder + img_name)
    if not is_gray_scale(opencv_image):
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
    find_item.find_item(opencv_image, img_name, debug=True)

def is_gray_scale(img):
    return len(img.shape) < 3


def main():
    setup_res_folder("res_annotated_imgs")
    setup_res_folder("res_contour_imgs")
    setup_res_folder("res_edge_imgs")

    test_file_path = "./test_imgs/"
    # object_detection_single_image(test_file_path, file)

    object_detection_folder(test_file_path)

def setup_res_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        # remove previous files
        files = glob.glob(folder_name + "/*")
        for f in files:
            os.remove(f)


if __name__ == '__main__':
    main()