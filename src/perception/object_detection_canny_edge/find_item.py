import cv2.cv2 as cv2
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import io, feature, filters, exposure, color


# Resources:
# https://stackoverflow.com/questions/56604151/python-extract-multiple-objects-from-image-opencv
# https://stackoverflow.com/questions/46274961/removing-horizontal-lines-in-image-opencv-python-matplotlib

def find_item(img, img_name=None, debug=False):
    """Find the object on floor in an image.

        Arguments:
        opencv_image -- the image

        Return:
            rectangles containing object: [x, y, w, h]
    """
    # check if image in gray scale
    if not is_gray_scale(img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # improve contrast
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
    tuned = clahe.apply(img)
    # tuned = cv2.equalizeHist(img)
    # alpha: contrast, beta: brightness
    tuned = cv2.convertScaleAbs(tuned, alpha=1.5, beta=0)

    # blur image
    blurred = cv2.GaussianBlur(tuned, (5, 5), 0)

    # get edges
    canny = cv2.Canny(blurred, 50, 255, 1)

    # filter straight lines
    smoothed = smooth_edge(canny, debug=False)
    filtered_horizontal = filter_horizontal_lines(smoothed, debug=False)
    filtered_vertical = filter_vertical_lines(filtered_horizontal, debug=False)
    filtered = filter_straight_lines(filtered_vertical, debug=False)

    closing = closing_transform(filtered, debug=False)
    opening = opening_transform(closing, debug=False)

    # form a larger contour
    dilated = dilating_transform(opening, (5, 5), 2, debug=False)

    # find contours
    cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate through contours
    image_number = 0
    rect = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        rect.append((x, y, w, h))
        image_number += 1

    # sort by contour area, and distance to camera.
    rect.sort(key=get_area_and_distance, reverse=True)

    detected_item = None if len(rect) == 0 else rect[0]
    if detected_item is not None:
        x, y, w, h = detected_item
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

    # return the largest contour
    if debug:
        # image = Image.fromarray(tuned)
        # image.show()

        # image = Image.fromarray(dilated)
        # image.show()

        cv2.imwrite("./res_annotated_imgs/" + img_name, img)
        cv2.imwrite("./res_contour_imgs/" + img_name, dilated)
        cv2.imwrite("./res_edge_imgs/" + img_name, canny)

    print("Detected", image_number, "objects, selected object", detected_item)
    return detected_item

def get_area_and_distance(rect):
    # sort by largest area, and closest to camera
    x, y, w, h = rect
    return (w * h) + y

def is_gray_scale(img):
    return len(img.shape) < 3


def filter_horizontal_lines(img, debug):
    res = np.copy(img)

    cols = res.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    eroded = cv2.erode(res, horizontal_structure)
    dilated = cv2.dilate(eroded, horizontal_structure)

    cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(res, [c], -1, (0, 0, 0), 2)

    if debug:
        image = Image.fromarray(res)
        image.show()

    return res

def filter_vertical_lines(img, debug):
    res = np.copy(img)
    rows = res.shape[0]
    vertical_size = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    # Apply morphology operations
    eroded = cv2.erode(res, vertical_structure)
    dilated = cv2.dilate(eroded, vertical_structure)

    cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(res, [c], -1, (0, 0, 0), 2)

    # Show extracted vertical lines
    if debug:
        image = Image.fromarray(res)
        image.show()


    return res


# filter lines in any angles
def filter_straight_lines(img, debug):
    res = np.copy(img)
    lines = cv2.HoughLinesP(res, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=5)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(res, (x1, y1), (x2, y2), (0, 0, 0), 2)
    if debug:
        image = Image.fromarray(res)
        image.show(title="filter_lines")

    return res

def smooth_edge(img, debug):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

    closing_kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, closing_kernel, iterations=3)

    canny = cv2.Canny(closing, 120, 255, 1)

    if debug:
        image = Image.fromarray(canny)
        image.show()

    return canny


def closing_transform(img, debug):
    # closing edges to form a larger contour (dilation then erosion)
    closing_kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, closing_kernel, iterations=3)
    if debug:
        image = Image.fromarray(closing)
        image.show()
    return closing


def opening_transform(img, debug):
    # opening to reduce noise
    opening_kernel = np.ones((9, 9), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, opening_kernel, iterations=1)
    if debug:
        image = Image.fromarray(opening)
        image.show()
    return opening


def eroding_transform(img, ksize, iter, debug):
    erode_kernel = np.ones(ksize, np.uint8)
    eroded = cv2.erode(img, erode_kernel, iterations=iter)
    if debug:
        image = Image.fromarray(eroded)
        image.show()
    return eroded


def dilating_transform(img, ksize, iter, debug):
    dilate_kernel = np.ones(ksize, np.uint8)
    dilated = cv2.dilate(img, dilate_kernel, iterations=iter)
    if debug:
        image = Image.fromarray(dilated)
        image.show()
    return dilated
