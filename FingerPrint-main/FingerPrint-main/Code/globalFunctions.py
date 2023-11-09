#!/usr/bin/env python

"""
This file defines global functions for Fingerprint project.

Author: Ayelet Zadock
Last modified: 28-05-2018

"""

# Imports:
import os
import glob
import cv2
import pandas as pd
#import tkinter.filedialog as tk # or
from tkinter import filedialog
import ntpath
from stitch import Stitcher
# import mysql
import PIL
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np
import imutils
import random
global DBpath, excelDB, DBsheet
import json
from json import JSONEncoder, JSONDecoder
# from MongoConnection import MongoDB


global root, list_fingers, list_hand, img_label, rotate_scale, brightness_scale, sharpness_scale


DBpath = os.getcwd() + os.sep + 'database'# + os.sep + 'FFP0519'
DBpath = os.getcwd() + os.sep + 'database' + os.sep + 'Relationships'
#DBpath = 'C:/database/'
excelDB = 'database.xlsx'
DBsheet = 'fingerprints'
details_title = 'Details'
ips_title = 'InterestingPoints'

data_title = 'data'
id_title = "_id"
image_format = 'JPEG'

class Titles:
    ipoints_title = 'ipoints'
    features_title = 'features'


stitcher = Stitcher()
# mongodb = MongoDB()

"""
def getInputImage(inputPath)
Brief: This function gets a path to image and extracts it into filename, file path and file prefix.

Input:
    -inputPath: a path to file.
Output:
    -_inputName: filename.
    -_inputDirName: filename directory name (father).
    -_inputDirPath: directory path.
    -_inputPrefix: filename prefix.
"""
def getInputImage(inputPath):
    # prompts for an image file, and returns the filename, father directory, path, and input prefix
    _inputFileName = ntpath.basename(inputPath)
    _inputDirPath = inputPath[:-len(_inputFileName)]
    _inputDirName = ntpath.basename(_inputDirPath[:-1])
    _dotPos = _inputFileName.rfind('.')
    if _dotPos == -1:  # if there is not a dot in file's name
        _inputFilePrefix = _inputFileName
    else:
        _inputFilePrefix = _inputFileName[:_dotPos]  # assumes that a suffix exists

    return [_inputFileName, _inputDirName, _inputDirPath, _inputFilePrefix]


"""
def extractFingerDataFromFilename(filename)
Brief: This function gets a filename and extracts data of: person name, hand and finger in hand.

Exceptions:
    -Hand should be right(R) or left (L).
    -Finger should be a number between 1-5 while: thumb is 1 and pinkie is 5.
    Otherwise (for both), a variable called _inStandard is changed to be False.

Input:
    -filename: a prefix of filename.
Output:
    -__person: person id.
    -_hand: hand letter.
    -_finger: finger number.
    -_inStandard: a variable that returns True/False. Means, in standard or not.
"""
def extractFingerDataFromFilename(filename):
    _inStandard = True
    _hand = filename[-2]
    _finger = filename[-1]
    if _hand not in 'RL' or _finger not in '12345':
        _inStandard = False
    _handPos = filename.rfind(_hand)
    _person = filename[:_handPos]

    return [_person, _hand, _finger, _inStandard]


def check_existence_by_stitcher(image, linkImages):
    stitcher = Stitcher()  # define a variable of Stitcher class
    source_img = cv2.imread(image)
    ipoints = None
    features = None

    for linkId, linkImage_filename in linkImages:
        img = cv2.imread(linkImage_filename)  # read linked image from path
        #linkImage = numpy.empty_like(linkImage[0])
        #image = numpy.array(image)
        #print("Linked: ", linkImage, type(linkImage), type(image))
        imagesList = [source_img,
                      img]  # thresh_source_img  # define a list of source and destination images to stitch
        # if mse_after_threshold-mse_before_threshold <= 0:
        # stitch the images together to create a panorama
        result, vis, ipoints, features = stitcher.stitch(imagesList, showMatches=True)
        # else:
        #    result = None

        if not (result is None):  # if succeed to find matches between the two images
            # print("Match was found.")
            #cv2.imshow("VIS", vis)

            # cv2.imshow("result", result)  # show result image (for check)
            vis = Image.fromarray(vis, 'RGB')
            img = Image.fromarray(img, 'RGB')
            source_img = Image.fromarray(source_img)#, 'RGB')
            # img.show()
            #img2 = trim(img)
            # img2.show()
            #cv2.waitKey(0)
            return True, ipoints, features, vis, source_img, img, linkImage_filename, linkId
    #    else:
    #        print("There are not enough matches.")
    # print("There are not enough matches.")
    return False, ipoints, features, None, None, None, None, None


def detectAndDescribe(image):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we are using OpenCV 3.X
    if imutils.is_cv3():
        # detect and extract features from the image
        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)

    # otherwise, we are using OpenCV 2.4.X
    else:
        # detect keypoints in the image
        detector = cv2.FeatureDetector_create("SIFT")
        kps = detector.detect(gray)

        # extract features from the image
        extractor = cv2.DescriptorExtractor_create("SIFT")
        (kps, features) = extractor.compute(gray, kps)

    # convert the keypoints from KeyPoint objects to NumPy
    # arrays
    kps = np.float32([kp.pt for kp in kps])

    # return a tuple of keypoints and features
    return (kps, features)


def matchKeypoints(kpsA, kpsB, featuresA, featuresB,
                   ratio, reprojThresh, accuLevel):
    # compute the raw matches and initialize the list of actual
    # matches
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    rawMatches = matcher.knnMatch(featuresA, featuresB, 2)

    matches = []

    # loop over the raw matches
    for m in rawMatches:
        # ensure the distance is within a certain ratio of each
        # other (i.e. Lowe's ratio test)
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            matches.append((m[0].trainIdx, m[0].queryIdx))

    # computing a homograph requires at least "accuLevel" matches
    if len(matches) >= accuLevel * len(rawMatches):
        # construct the two sets of points

        rand_accu = random.sample(range(int(len(matches))), int(accuLevel * len(rawMatches)))
        _ptsA = [kpsA[i] for (_, i) in matches]
        _ptsB = [kpsB[i] for (i, _) in matches]
        ptsA = np.float32([_ptsA[i] for i in range(len(matches)) if i in rand_accu])
        ptsB = np.float32([_ptsB[i] for i in range(len(matches)) if i in rand_accu])

        # compute the homograph between the two sets of points
        (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                         reprojThresh)

        # return the matches along with the homograph matrix
        # and status of each matched point
        return (matches, H, status)
    return None, None, None


def drawMatches(imageA, imageB, kpsA, kpsB, matches, status):
    # initialize the output visualization image
    (hA, wA) = imageA.shape[:2]
    (hB, wB) = imageB.shape[:2]
    vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
    vis[0:hA, 0:wA] = imageA
    #vis[0:hB, wB:] = imageB  # this is the source code!
    vis[0:hB, wA:] = imageB

    # loop over the matches
    for ((queryIdx, trainIdx), s) in zip(matches, status):
        # only process the match if the keypoint was successfully
        # matched
        if s == 1:
            # draw the match
            ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
            ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
            cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

    # return the visualization
    return vis

def clean_img(image, k_value):
    kernel = (k_value, k_value)  # the dimension of the x and y axis of the kernel.
    cleaned_image = cv2.blur(image, kernel)
    return cleaned_image

def convert_cv2_to_pil(img):
    # convert cv2 image to pil
    converted_img = Image.fromarray(np.uint8(img))
    return converted_img

def convert_pil_to_cv2(img):
    # convert pil image to cv2
    converted_img = np.array(img)
    return converted_img

def dilation(image, k_value):
    # k_value = 3
    kernel = np.ones((k_value, k_value), np.uint8)
    dilation_image = cv2.dilate(image, kernel, iterations=2)
    return dilation_image

def brightness(img, val):
    func_name = "brightness"
    #print(f"In {func_name}")

    enhancer = ImageEnhance.Brightness(img)
    enhance = enhancer.enhance(val)
    return enhance


def clean_fingerprint(img, val, k_value):
    func_name = "clean_fingerprint"
    # print(f"In {func_name}")

    # convert pil image to cv2
    img = np.array(img)
    # print("-----------------------------------------------")
    # print(type(img))
    # print(img)
    # print("-----------------------------------------------")
    # converted_img = cv2.cvtColor(pix, cv2.COLOR_GRAY2BGR)
    inverted_image = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 11, 32)

    pil_img = convert_cv2_to_pil(inverted_image)
    bright_img = brightness(pil_img, 1.4)

    cv2_img = convert_pil_to_cv2(bright_img)
    _, mask = cv2.threshold(cv2_img, 100, 255, cv2.THRESH_BINARY_INV)
    dilation_image = dilation(mask, val)
    kernel = k_value
    cleaned_img = clean_img(img, kernel)

    mask_img = dilation_image  # mask
    mask = (mask_img == 0)
    cleaned_fingerprint = np.copy(cleaned_img)
    cleaned_fingerprint[mask] = img[mask]

    # convert cv2 image to pil
    converted_img = convert_cv2_to_pil(cleaned_fingerprint)
    return converted_img


def check_existence_by_ipoints(image, linkImages, accuracyLevel):
    ratio = 0.75
    reprojThresh = 4.0

    source_img = cv2.imread(image)  # read new (source) image
    source_img = source_img.astype('uint8')
    (kpsA, featuresA) = detectAndDescribe(source_img)

    exists_images = []

    try:
        accuracyLevel = int(accuracyLevel) / 100
    except:
        accuracyLevel = 0.1

    for linkId, linkImage_filename, _ipoints in linkImages:
        print(linkImage_filename)
        try:
            new_img = cv2.imread(linkImage_filename)  # read linked image from path
            new_img = new_img.astype('uint8')
            (kpsB, featuresB) = detectAndDescribe(new_img)

            M = matchKeypoints(kpsB, kpsA, featuresB, featuresA, ratio, reprojThresh, accuracyLevel)

            # if the match is None, then there aren't enough matched
            # keypoints to create a panorama
            if M[1] is not None:
                # apply a perspective warp to stitch the images together
                (matches, H, status) = M
                result = cv2.warpPerspective(new_img, H, (source_img.shape[1] + new_img.shape[1], source_img.shape[0]))

                result[0:new_img.shape[0], 0:new_img.shape[1]] = source_img
                vis = drawMatches(source_img, new_img, kpsA, kpsB, matches, status)

                if result is not None:  # there's a match for sure
                    # print("Match was found.")
                    vis = Image.fromarray(vis, 'RGB')
                    exists_images.append((linkImage_filename, kpsA, featuresA, vis, linkId))
        except:
            continue
    return exists_images

def check_existence_by_ipoints_features(image, userData, accuracyLevel):
    ratio = 0.75
    reprojThresh = 4.0

    source_img = cv2.imread(image)  # read new (source) image
    source_img = source_img.astype('uint8')
    (kpsA, featuresA) = detectAndDescribe(source_img)

    exists_images = []

    try:
        accuracyLevel = int(accuracyLevel) / 100
    except:
        accuracyLevel = 0.1

    for user_id, user_details, user_ip, user_features in userData:
        try:
            M = stitcher.stitch_ips(kpsA, featuresA, user_ip, user_features)

            # if the match is None, then there aren't enough matched
            # keypoints to create a panorama
            if M is not None:
                # apply a perspective warp to stitch the images together


                (matches, H, status) = M
                result = stitcher.get_result()
                vis = stitcher.get_vis()


                result = cv2.warpPerspective(new_img, H, (source_img.shape[1] + new_img.shape[1], source_img.shape[0]))

                result[0:new_img.shape[0], 0:new_img.shape[1]] = source_img
                vis = drawMatches(source_img, new_img, kpsA, kpsB, matches, status)

                if result is not None:  # there's a match for sure
                    # print("Match was found.")
                    vis = Image.fromarray(vis, 'RGB')
                    exists_images.append((linkImage_filename, kpsA, featuresA, vis, linkId))
        except:
            continue
    return exists_images


def check_existence_by_c2c_old(image, linkImages, hand, finger, accuracyLevel, val, kernel):
    ratio = 0.75
    reprojThresh = 4.0

    source_img = cv2.imread(image)  # read new (source) image
    source_img = clean_fingerprint(source_img, val, kernel)
    source_img = convert_pil_to_cv2(source_img)
    (kpsA, featuresA) = detectAndDescribe(source_img)

    exists_images = []

    try:
        accuracyLevel = int(accuracyLevel) / 100
    except:
        accuracyLevel = 0.1

    for linkId, linkImage_filename, _ipoints in linkImages:
        new_img = cv2.imread(linkImage_filename)  # read linked image from path
        new_img = clean_fingerprint(new_img, val, kernel)
        new_img = convert_pil_to_cv2(new_img)
        (kpsB, featuresB) = detectAndDescribe(new_img)

        M = matchKeypoints(kpsB, kpsA, featuresB, featuresA, ratio, reprojThresh, accuracyLevel)

        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M[1] is not None:
            # apply a perspective warp to stitch the images together
            (matches, H, status) = M
            result = cv2.warpPerspective(new_img, H, (source_img.shape[1] + new_img.shape[1], source_img.shape[0]))

            result[0:new_img.shape[0], 0:new_img.shape[1]] = source_img
            vis = drawMatches(source_img, new_img, kpsA, kpsB, matches, status)

            if result is not None:  # there's a match for sure
                # print("Match was found.")
                vis = Image.fromarray(vis, 'RGB')
                exists_images.append((linkImage_filename, kpsA, featuresA, vis, linkId))

    return exists_images

def check_existence_by_c2c(image, linkImages, accuracyLevel, val, kernel):
    ratio = 0.75
    reprojThresh = 4.0

    source_img = cv2.imread(image)  # read new (source) image
    source_img = clean_fingerprint(source_img, val, kernel)
    source_img = convert_pil_to_cv2(source_img)
    (kpsA, featuresA) = stitcher.get_interesting_points_by_img(source_img)

    exists_images = []

    try:
        accuracyLevel = int(accuracyLevel) / 100
    except:
        accuracyLevel = 0.1

    for idfp, id_image, id_ipoints, id_features in linkImages:
        idfp_str = str(idfp)
        new_img = mongodb.get_image(id_image, idfp_str, convert_json_to_numpy, dtype=np.uint8)
        kpsB = mongodb.get_ipoints(id_ipoints, idfp_str, convert_json_to_numpy)
        featuresB = mongodb.get_features(id_features, idfp_str, convert_json_to_numpy)

        # featuresA = convert_json_to_numpy(convert_numpy_to_json(featuresA, Titles.features_title), Titles.features_title)
        # kpsA = convert_json_to_numpy(convert_numpy_to_json(kpsA, Titles.ipoints_title), Titles.ipoints_title)

        M = stitcher.stitch_ips(kpsB, kpsA, featuresB, featuresA, ratio, reprojThresh, accuracyLevel)

        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M is not None:
            # apply a perspective warp to stitch the images together
            (matches, H, status) = M
            result = stitcher.get_result(source_img, new_img, H)
            vis = stitcher.get_vis(source_img, new_img, kpsA, kpsB, matches, status)

            if result is not None:  # there's a match for sure
                # print("Match was found.")
                vis = Image.fromarray(vis, 'RGB')
                exists_images.append((idfp, kpsA, featuresA, vis))

    return exists_images

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def convert_numpy_to_json(numpy_arr, title):
    # Serialization
    try:
        numpyData = {title: numpy_arr}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
        # print("Printing JSON serialized NumPy array")
        # print(encodedNumpyData)
        return encodedNumpyData
    except Exception as e:
        print(f"Error in convert_numpy_to_json: {e}")
        return None


def convert_json_to_numpy(json_data, title, dtype='float32'):
    # Deserialization
    # print("Decode JSON serialized NumPy array")
    try:
        decodedArrays = json.loads(json_data)

        finalNumpyArray = np.asarray(decodedArrays[title], dtype=dtype)
        # finalNumpyArray = np.asarray(decodedArrays[title], dtype=np.uint8)

        # print("NumPy Array")
        # print(finalNumpyArray)
        return finalNumpyArray
    except Exception as e:
        print(f"Error in convert_json_to_numpy: {e}")
        return None


class CONSTANT(object):
    FLOAT_TYPE_STR = "float"
    IMG_TIF_TYPE = '.tif'
    IMG_JPG_TYPE = '.jpg'
    STAR = '*'
    ZERO = 0
    SCALE = 2.0
    OFFSET = 100
    THRESHOLD = 30000
