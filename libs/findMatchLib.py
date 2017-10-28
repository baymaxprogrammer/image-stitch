# import necessary packages
import numpy as np
import imutils
import cv2

class FindMatchLib:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()

    def findValue(self, image, template):
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Using average color as the threshold for Canny edge detector
        average_color = template[:, :].mean()
        template = cv2.Canny(template, 0.33*average_color, 2*average_color)

        (tH, tW) = template.shape[:2]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        found = None

        # loop over different scales of the image to find a match
        for scale in np.linspace(0.05, 10.0, 50)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image

            # Using average color as the threshold for Canny edge detector
            average_color = resized[:, :].mean()
            edged = cv2.Canny(resized, 0.33 * average_color, 2 * average_color)

            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if a new maximum correlation value, then update
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)
        return maxVal