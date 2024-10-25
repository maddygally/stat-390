import os
import sys
import cv2
import tifffile as tiff
import math
import numpy as np
from itertools import combinations

id = sys.argv[1]  # first command-line arg is patient ID
patient_filepath = sys.argv[2]  # second command-line arg is filepath to patient image

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

def preprocess_image(image_cv2):
    # convert to grayscale
    gray_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    
    # apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(gray_image, 255, 
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY_INV, 
                                            11, 2)

    # apply morphological operations to close gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    return morph

def filter_slices(contours, image, image_cv2):
    slices = []
    # take (up to) 8 largest contours with area >= 10
    contours = sorted(
        filter(lambda x: cv2.contourArea(x) >= 10, contours), 
        key=lambda x: cv2.contourArea(x), 
        reverse=True
    )[:8]
    contours = remove_overlap(contours)
    
    for contour in contours:
        # contour bounding coordinates
        x, y, w, h = cv2.boundingRect(contour)
        # normalized y-coords of the contour
        ymin_norm = y / image_cv2.shape[0]
        ymax_norm = (y + h) / image_cv2.shape[0]
        # normalized x-coords of the contour
        xmin_norm = x / image_cv2.shape[1]
        xmax_norm = (x + w) / image_cv2.shape[1]
        # map the normalized coords to the high-res image and store the slice
        slices.append(image[math.floor(ymin_norm * image.shape[0]):math.ceil(ymax_norm * image.shape[0]),
                            math.floor(xmin_norm * image.shape[1]):math.ceil(xmax_norm * image.shape[1])])
    return slices

def write_slices(slices, patient_id, stain):
    # Set output directory for cropped slices, using the stain type directly
    stain_folder = stain.replace('.tif', '').strip()  # Ensure the stain name is clean
    output_path = os.path.join('patients', patient_id, stain_folder)  
    os.makedirs(output_path, exist_ok=True)
    
    # write filtered slices to the stain-specific output directory
    for i, slice in enumerate(slices, 1):
        slice_path = os.path.join(output_path, f'slice_{i}.tif')
        cv2.imwrite(slice_path, slice, [cv2.IMWRITE_TIFF_COMPRESSION, cv2.IMWRITE_TIFF_COMPRESSION_NONE])
        print(f'Slice saved to: {slice_path}') 

def process_image(patient_id, filepath):
    # get the stain from the filename
    stain = os.path.basename(filepath).split(' ')[1].replace('.tif', '').strip()
    print(f'Processing for Patient ID: {patient_id}, Stain: {stain}')  

    # read the images (high-res and low-res)
    image, image_cv2 = read_images(filepath)

    # preprocess image to enhance contours for low-contrast stains (sox10 and melan-a)
    if stain.lower() in ['sox10', 'melan']:
        mask = preprocess_image(image_cv2)
    else:  # for H&E stain
        lower_bound = np.array([10, 10, 10])
        upper_bound = np.array([200, 200, 200])
        mask = cv2.inRange(image_cv2, lower_bound, upper_bound)

    # Extract contours from the processed mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Filter and extract slices from the image
    filtered_slices = filter_slices(contours, image, image_cv2)

    # Write the slices to the patient and stain-specific folder
    write_slices(filtered_slices, patient_id, stain)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python separate.py <patient_id> <image_filepath>")
    else:
        patient_id = sys.argv[1]
        filepath = sys.argv[2]
        process_image(patient_id, filepath)

