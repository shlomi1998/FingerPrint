
# import the necessary packages
import numpy as np
#from pyimagesearch.panorama import Stitcher
import argparse
import imutils
import cv2

import scipy.misc
#from panorama import Stitcher

class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()

    def get_interesting_points_by_path(self, filepath):
        img = cv2.imread(filepath)
        kps, features = self.detectAndDescribe(img)
        return kps, features

    def get_interesting_points_by_img(self, img):
        kps, features = self.detectAndDescribe(img)
        return kps, features

    def stitch_ips(self, kpsA, featuresA, kpsB, featuresB, ratio=0.75, reprojThresh=4.0, accuracyLevel=0.1):
        # match features between the two interesting points
        M = self.matchKeypoints(kpsB, kpsA,
                                featuresB, featuresA, ratio, reprojThresh, accuracyLevel)
        return M

    def get_result(self, imageA, imageB, H):
        print("111")
        result = cv2.warpPerspective(imageB, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        print("222")

        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageA

        print("333")
        return result

    def get_vis(self, imageA, imageB, kpsA, kpsB, matches, status):
        print("444")
        vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                                   status)
        print("555")
        return vis

    def get_ips_show(self, imageA, kpsA, matches, status):
            vis = self.drawInterestingPoints(imageA, kpsA, matches, status)
            return vis

    def stitch(self, images, ratio=0.75, reprojThresh=4.0,
               showMatches=False, showIP=False, getMatches=False, accuracyLevel=0.1):
        # unpack the images, then detect keypoints and extract
        # local invariant descriptors from them
        (imageA, imageB) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        # match features between the two images
        M = self.matchKeypoints(kpsB, kpsA,
                                featuresB, featuresA, ratio, reprojThresh, accuracyLevel)

        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M is None:
            return None, None, kpsA, featuresA

        # otherwise, apply a perspective warp to stitch the images
        # together
        (matches, H, status) = M
        result = cv2.warpPerspective(imageB, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageA

        # check to see if the keypoint matches should be visualized
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                                   status)

            # return a tuple of the stitched image and the
            # visualization
            return result, vis, kpsA, featuresA

        # check to see if the keypoint matches should be visualized
        if showIP:
            vis = self.drawInterestingPoints(imageA, kpsA, matches, status)

            # return a tuple of the stitched image and the
            # visualization
            return result, vis, kpsA, featuresA

        # check to see if the keypoint matches should be visualized
        if getMatches:
            vis = self.drawInterestingPoints(imageA, kpsA, matches, status)

            # return a tuple of the stitched image and the
            # visualization
            return result, vis, kpsA, (matches, status)

        # return the stitched image
        return result, None, kpsA, featuresA

    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we are using OpenCV 3.X
        if self.isv3:
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

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
                       ratio, reprojThresh, accuLevel):
        # compute the raw matches and initialize the list of actual matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)

        matches = []

        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

            # computing a homograph requires at least 4 matches -changed to have better results
            if len(matches) > accuLevel * len(rawMatches):
                # construct the two sets of points
                ptsA = np.float32([kpsA[i] for (_, i) in matches])
                ptsB = np.float32([kpsB[i] for (i, _) in matches])

                # compute the homograph between the two sets of points
                (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                                 reprojThresh)

                if H is not None:
                    # return the matches along with the homograph matrix
                    # and status of each matched point
                    return (matches, H, status)

        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
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

    def drawInterestingPoints(self, imageA, kpsA, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        vis = np.zeros((hA, wA, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA

        counter = 0
        # loop over the matches
        for ((queryIdx, trainIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                cv2.circle(vis, ptA, 2, (0, 255, 0), 1)
                counter += 1

        print(f'There are {counter} good matches')
        # return the visualization
        return vis
