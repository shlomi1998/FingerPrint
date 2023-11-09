#!/usr/bin/env python

"""
This file defines the client side of Fingerprint project.

Author: Ayelet Zadock
Last modified: 05-05-2019

"""

# Imports:
import os
import glob
import cv2
import numpy as np
import pandas as pd
# import tkinter.filedialog as tk # or
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox

import globalFunctions as gf
from globalFunctions import *
# from pyimagesearch.panorama import Stitcher
import argparse
import imutils
from stitch import Stitcher
from PIL import Image, ImageChops

import time
import scipy.misc
import sys

import pymysql
pymysql.install_as_MySQLdb()


# Globals:
constants = CONSTANT()
FLOAT_TYPE_STR = constants.FLOAT_TYPE_STR
IMG_TIF_TYPE = constants.IMG_TIF_TYPE
IMG_JPG_TYPE = constants.IMG_JPG_TYPE
IMG_TYPE = IMG_JPG_TYPE
STAR = constants.STAR
ZERO = constants.ZERO
SCALE = constants.SCALE
OFFSET = constants.OFFSET


'''
Function name: trim()

Brief: Function to crop black border from a PIL image.

Description:
This function gets a PIL image and removes its border.

Input:
    - image (Image): a PIL image.
Output:
    - croppedImg (Image): a cropped PIL image.

Errors and exceptions:
    - If didn't succeed to find positions to crop, return input image (image). 

'''

def trim(image):
    bg = Image.new(image.mode, image.size, image.getpixel((ZERO, ZERO)))  # create a new black image
    diff = ImageChops.difference(image, bg)  # calculates absolute value of the difference between the two pix-by-pix
    diff = ImageChops.add(diff, diff, scale=SCALE,
                          offset=-OFFSET)  # adds diff to diff, divides the result by scale and adds the offset
    bbox = diff.getbbox()  # get positions to crop
    if bbox:
        croppedImg = image.crop(bbox)  # crops image by positions that found before
        return croppedImg
    return image  # if didn't succeed to find positions to crop


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype(FLOAT_TYPE_STR) - imageB.astype(FLOAT_TYPE_STR)) ** 2)
    shape_size = imageA.shape[0] * imageA.shape[1]
    err /= float(shape_size)

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def mseUpdated(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    diff = [imageA.astype(FLOAT_TYPE_STR) - imageB.astype(FLOAT_TYPE_STR)]
    print("diff: ", diff)
    err = np.sum((imageA.astype(FLOAT_TYPE_STR) - imageB.astype(FLOAT_TYPE_STR)) ** 2)
    shape_size = imageA.shape[0] * imageA.shape[1]
    err /= float(shape_size)

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def cleanImage(img, range_start=ZERO, range_stop=256):
    pixels = {i: np.sum(img == i) for i in
              range(range_start, range_stop)}  # build a dictionary that counts amount of pixels per color
    max_value = max(pixels.values())

    '''
    max_value_of_color = range_stop
    for i in range(range_stop - 1, range_start + 1, -1):
        if pixels[i] != 0:
            max_value_of_color = i
            break

    smallest = img.min(axis=0).min(axis=0)
    max_value_of_color = img.max(axis=0).max(axis=0)

    img = img * (255/max_value_of_color)
    '''
    factor = 255 / max_value
    print("--------------------")
    print("img: ", img)
    print("********************")
    img = img + factor
    #img = img / max_value
    #img = img * 255
    return img


def findThresholdByRange(img, range_start=ZERO, range_stop=256):
    pixels = {i: np.sum(img == i) for i in
              range(range_start, range_stop)}  # build a dictionary that counts amount of pixels per color
    max_value = max(pixels.values())
    max_list = [key for key in pixels if pixels[key] == max_value]
    threshold = int(sum(max_list) / len(max_list))
    threshold = min(max_list)
    return threshold


def findThreshold(img, range_start=ZERO, range_stop=256):
    threshold = findThresholdByRange(img, range_start, range_stop)
    # if threshold in [0, 255]:
    # threshold = findThresholdByRange(img, 1, 255)
    #    threshold = 138
    # return None
    print("Threshold is {}".format(threshold))

    if threshold is not None:
        ret2, thresh_img = cv2.threshold(img, threshold - 1, 255, cv2.THRESH_BINARY)
    else:
        thresh_img = img

    return thresh_img


def findMatchByMSE_Threshold(source_img, dbPath=DBpath):
    kernel = np.ones((5, 5), np.uint8)
    i = ZERO
    is_continue = False

    match_img_list = []

    thresh_source_img = findThreshold(source_img)  # find threshold of source image

    print("Path: " + dbPath)

    for filename in glob.glob(os.path.join(dbPath, STAR + IMG_TIF_TYPE)):
        print("Filename: ", filename)
        dest_img = cv2.imread(filename)  # read a new image
        ###dest_img = cv2.morphologyEx(dest_img, cv2.MORPH_CLOSE, kernel)  # clean image by morphology method
        mse_before_threshold = mse(source_img, dest_img)  # calculate MSE function
        print("MSE before threshold: ", mse_before_threshold)

        thresh_dest_img = findThreshold(dest_img)  # find threshold of current image in DB
        mse_after_threshold = mse(thresh_source_img, thresh_dest_img)  # calculate MSE function
        print("MSE after threshold: ", mse_after_threshold)

        print("index: ", i, "\n")
        i += 1
        #if i > 6:  # if condition to break loop due to runtime
        #    break
        print("----------------------------------------------")

        if mse_before_threshold < constants.THRESHOLD:
            match_img_list.append((filename, dest_img))  # thresh_dest_img

        continue  # break current iteration -prevents error of open-cv

    is_continue = True
    is_empty = False
    ###This if-else loop should be fixed!!!
    if len(match_img_list) < 1:  # if there is no match
        is_empty = True
        is_continue = bool(int(input("No match was found by MSE, do you want to continue?\n1 = Yes, 0 = No\n")))
    ###else:  # if found at least one image that may be matches

    if is_continue:
        if is_empty:
            database_files = glob.glob(os.path.join(DBpath, STAR + IMG_TIF_TYPE))
            database_files = database_files[:3]
            read_files = [cv2.imread(database_file) for database_file in database_files]
            match_img_list = list(zip(database_files, read_files))

        match_list = []  # define a list for matches
        stitcher = Stitcher()  # define a variable of Stitcher class

        i = 0

        for match_img in match_img_list:
            img_name, img_data = match_img
            imagesList = [source_img, img_data]  # thresh_source_img  # define a list of source and destination images to stitch
            # if mse_after_threshold-mse_before_threshold <= 0:
            # stitch the images together to create a panorama
            (result, vis) = stitcher.stitch(imagesList, showMatches=True)
            # else:
            #    result = None

            if not (result is None):  # if succeed to find matches between the two images
                print("Match was found.")
                # cv2.imshow("VIS", vis)
                scipy.misc.imsave(f'vis_{i}' + IMG_TYPE, vis)

                i += 1
                # cv2.imshow("result", result)  # show result image (for check)
                img = Image.fromarray(result, 'RGB')
                # img.show()
                img2 = trim(img)
                # img2.show()
                # cv2.waitKey(0)
                match_list.append(img_name)  # add filename to matches list
            else:
                print("There are not enough matches.")

        print(f"\nFound {len(match_list)} matches as follow:")
        for img_name in match_list:
            print(img_name)


def CreateMatchImgListByMSE(source_img, dbPath=DBpath):
    print("Start")
    match_img_list = []
    mse_img_list = []
    i = ZERO

    for filename in glob.glob(os.path.join(dbPath, STAR + IMG_TIF_TYPE)):
        print(f"Filename: {filename}")
        current_filename = filename.split("\\")[-1]
        dest_img = cv2.imread(filename)  # read a new image
        mse_before_threshold = mse(source_img, dest_img)  # calculate MSE function
        print(f"MSE before threshold: {mse_before_threshold}")

        mse_img_list.append((current_filename, mse_before_threshold))

        print("index: ", i, "\n")
        i += 1
        #if i > 6:  # if condition to break loop due to runtime
        #    break
        print("----------------------------------------------")

        if mse_before_threshold < constants.THRESHOLD:
            match_img_list.append((filename, dest_img))  # thresh_dest_img

    print("End")
    return match_img_list, mse_img_list


def IsContinue(match_img_list):
    is_continue = True
    if len(match_img_list) < 1:  # if there is no match
        is_continue = tk.messagebox.askquestion("Is continue", "No match was found by MSE, do you want to continue?", icon="warning")
        if is_continue == "yes":
            is_continue = True
        else:
            is_continue = False
    return is_continue, len(match_img_list)


def CreateFullImgList():
    database_files = glob.glob(os.path.join(DBpath, STAR + IMG_TIF_TYPE))
    database_files = database_files[:3]
    read_files = [cv2.imread(database_file) for database_file in database_files]
    match_img_list = list(zip(database_files, read_files))
    return match_img_list


def CreateMatchImgListByStitcher(source_img, match_img_list):
    match_list = []  # define a list for matches
    stitcher = Stitcher()  # define a variable of Stitcher class
    i = 0

    for match_img in match_img_list:
        img_name, img_data = match_img
        imagesList = [source_img,
                      img_data]  # thresh_source_img  # define a list of source and destination images to stitch
        # stitch the images together to create a panorama
        (result, vis) = stitcher.stitch(imagesList, showMatches=True)

        if not (result is None):  # if succeed to find matches between the two images
            print("Match was found.")
            # cv2.imshow("VIS", vis)
            scipy.misc.imsave(f'vis_{i}' + IMG_TYPE, vis)

            i += 1
            # cv2.imshow("result", result)  # show result image (for check)
            img = Image.fromarray(result, 'RGB')
            # img.show()
            img2 = trim(img)
            # img2.show()
            # cv2.waitKey(0)
            match_list.append(img_name)  # add filename to matches list
        else:
            print("There are not enough matches.")

    return match_list


def PrintDetailsOfMatches(match_list):
    n = len(match_list)
    if n < 1:
        print("No match was found.")
        return
    elif n == 1:
        print("\nFound the next match:")
    else:
        print(f"\nFound {n} matches as follow:")
    for img_name in match_list:
        print(img_name)


def temp(source_img, dbPath=DBpath):
    kernel = np.ones((5, 5), np.uint8)
    i = ZERO
    is_continue = False

    match_img_list = []

    thresh_source_img = findThreshold(source_img)  # find threshold of source image

    print("Path: " + dbPath)

    for filename in glob.glob(os.path.join(dbPath, STAR + IMG_TIF_TYPE)):
        print("Filename: ", filename)
        dest_img = cv2.imread(filename)  # read a new image
        ###dest_img = cv2.morphologyEx(dest_img, cv2.MORPH_CLOSE, kernel)  # clean image by morphology method
        mse_before_threshold = mse(source_img, dest_img)  # calculate MSE function
        print("MSE before threshold: ", mse_before_threshold)

        thresh_dest_img = findThreshold(dest_img)  # find threshold of current image in DB
        mse_after_threshold = mse(thresh_source_img, thresh_dest_img)  # calculate MSE function
        print("MSE after threshold: ", mse_after_threshold)

        print("index: ", i, "\n")
        i += 1
        #if i > 6:  # if condition to break loop due to runtime
        #    break
        print("----------------------------------------------")

        if mse_before_threshold < THRESHOLD:
            match_img_list.append((filename, dest_img))  # thresh_dest_img

        continue  # break current iteration -prevents error of open-cv

    is_continue = True
    is_empty = False
    ###This if-else loop should be fixed!!!
    if len(match_img_list) < 1:  # if there is no match
        is_empty = True
        is_continue = bool(int(input("No match was found by MSE, do you want to continue?\n1 = Yes, 0 = No\n")))
    ###else:  # if found at least one image that may be matches

    if is_continue:
        if is_empty:
            database_files = glob.glob(os.path.join(DBpath, STAR + IMG_TIF_TYPE))
            database_files = database_files[:3]
            read_files = [cv2.imread(database_file) for database_file in database_files]
            match_img_list = list(zip(database_files, read_files))

        match_list = []  # define a list for matches, if will be
        stitcher = Stitcher()  # define a variable of Stitcher class
        i = 0

        for match_img in match_img_list:
            img_name, img_data = match_img
            imagesList = [source_img, img_data]  # thresh_source_img  # define a list of source and destination images to stitch
            # if mse_after_threshold-mse_before_threshold <= 0:
            # stitch the images together to create a panorama
            (result, vis) = stitcher.stitch(imagesList, showMatches=True)
            # else:
            #    result = None

            if not (result is None):  # if succeed to find matches between the two images
                print("Match was found.")
                # cv2.imshow("VIS", vis)
                scipy.misc.imsave(f'vis_{i}' + IMG_TYPE, vis)

                i += 1
                # cv2.imshow("result", result)  # show result image (for check)
                img = Image.fromarray(result, 'RGB')
                # img.show()
                img2 = trim(img)
                # img2.show()
                # cv2.waitKey(0)
                match_list.append(img_name)  # add filename to matches list
            else:
                print("There are not enough matches.")

        print(f"\nFound {len(match_list)} matches as follow:")
        for img_name in match_list:
            print(img_name)


def OpenFile():
    filename = filedialog.askopenfilename()  # open a dialog to get a path to image file
    if len(filename) == ZERO:
        sys.exit("There is no attached file.\nSystem is exit.")

    return filename
