import os
import sys
import cv2
import tifffile as tiff
import math
import numpy as np
from itertools import combinations


id = sys.argv[1] # first command-line arg is patient ID
patient_filepath = sys.argv[2] # second command-line arg is filepath to patient image


def read_images(path):
    with tiff.TiffFile(path) as tif:
        # high-res image
        image = tif.pages[3].asarray()

        # low-res image
        image_cv2 = tif.pages[-3].asarray()

    return image, image_cv2


def remove_overlap(contours):

    if len(contours) > 1:

        # generate indices of all possible contour pairs
        pairs = combinations(range(len(contours)), 2)

        for i, j in pairs:
            c1 = contours[i]
            c2 = contours[j]

            x1, y1, w1, h1 = cv2.boundingRect(c1)
            x2, y2, w2, h2 = cv2.boundingRect(c2)

            # use contour coordinates to check intersection
            if all([x1 < x2 + w2, x1 + w1 > x2, y1 < y2 + h2, y1 + h1 > y2]):
                if cv2.contourArea(c1) > cv2.contourArea(c2):
                    contours.pop(j)
                else:
                    contours.pop(i)
                
                # recursively call the function on the updated contour list
                return remove_overlap(contours)
    
    return contours


def filter_slices(contours, image, image_cv2):
    slices = []

    # take (up to) 8 largest contours with area >= 10
    contours = sorted(
        filter(lambda x: cv2.contourArea(x) >= 50, contours), 
        key = lambda x: cv2.contourArea(x), 
        reverse = True
    )[:8]

    contours = remove_overlap(contours)

    for contour in contours:
        # contour bounding coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # normalized y-coords of the contour
        ymin_norm = y/image_cv2.shape[0]
        ymax_norm = (y+h)/image_cv2.shape[0]

        # normalized x-coords of the contour
        xmin_norm = x/image_cv2.shape[1]
        xmax_norm = (x+w)/image_cv2.shape[1]

        # map the normalized coords to the high-res image and store the slice
        slices.append(image[math.floor(ymin_norm * image.shape[0]):math.ceil(ymax_norm * image.shape[0]),
                            math.floor(xmin_norm * image.shape[1]):math.ceil(xmax_norm * image.shape[1])])
    
    return slices


def write_slices(slices, id):

    # set output directory for cropped slices
    output_path = os.path.join('patients', id)

    os.makedirs(output_path, exist_ok = True)
    
    # write filtered slices to output directory
    for i, slice in enumerate(slices, 1):
        cv2.imwrite(f'{output_path}/slice_{i}.tif',
                    slice,
                    [cv2.IMWRITE_TIFF_COMPRESSION,
                     cv2.IMWRITE_TIFF_COMPRESSION_NONE])
        
lower_bound = np.array([10, 10, 10]) # black-ish
upper_bound = np.array([200, 200, 200]) # white-ish

def preprocess_image(image_cv2): # Convert the image to grayscale for better thresholding 
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) # Apply a Gaussian blur to reduce noise 
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Adaptive thresholding to handle varying light conditions 
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2 ) 
    return adaptive_thresh 
    
image, image_cv2 = read_images(patient_filepath) # Preprocess the image to get better separation for lighter regions 
mask = preprocess_image(image_cv2)

# use the mask to extract possible slices
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# filter slices
filtered_slices = filter_slices(contours, image, image_cv2)

# save filtered slices
write_slices(filtered_slices, id)