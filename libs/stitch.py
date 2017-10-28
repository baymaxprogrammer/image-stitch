# import necessary packages
import numpy as np
import imutils
import cv2
from .commons import commons

Commons = commons()

'''This calss uses SIFT and RANSAC to calculate 
homography matrix H and put two images together'''

class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()

    def stitch(self, images, ratio=0.75, reprojThresh=4.0):
        (imageB, imageA) = images
        (result, flag) = self.stitch_two_images_without_restriction(imageA, imageB, ratio, reprojThresh)

        if flag:
            (result, flag) = self.stitch_two_images_without_restriction(imageB, imageA, ratio, reprojThresh)

        return result

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

            # extract features from the image using SIFT approach
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        # convert the keypoints from KeyPoint objects to NumPy arrays for ease of use
        kps = np.float32([kp.pt for kp in kps])

        # return a tuple of keypoints and features
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
                       ratio, reprojThresh):
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

        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                             reprojThresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)

        # otherwise, no homograpy could be computed
        return None

    def stitch_two_images_without_restriction(self, imageA, imageB, ratio=0.75, reprojThresh=4.0):

        bordersize = imageA.shape[1]
        imageB = cv2.copyMakeBorder(imageB, top=0, bottom=0, left=bordersize, right=bordersize,
                                    borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])

        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
                                featuresA, featuresB, ratio, reprojThresh)

        # If M is None then it means that there is no overlap between two images
        if M is None:
            return None
        # Otherwise, apply a perspective warp to stitch the images
        # together
        (matches, H, status) = M

        result = cv2.warpPerspective(imageA, H,
                                     ((imageA.shape[1] + imageB.shape[1]), 2*imageA.shape[0]))

        average_color = [result[0, 0:, i].mean() for i in range(result.shape[-1])]

        # Flag if the images are in the right oder
        if np.mean(average_color) != 0:
            flag = True
        else:
            flag = False

        # Add imgB to the stitched plane
        for x, y in np.ndindex((imageB.shape[0], imageB.shape[1])):
            if sum(result[x, y, :]) == 0:
                result[x, y] = imageB[x, y]

        # Remove the black border of the final image
        result = Commons.crop_image(result, 0)

        return result, flag

