import numpy as np
import imutils

class commons:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()

    def crop_image(self, img, tol=0):
        mask = img[:, :, 1] > tol
        return img[np.ix_(mask.any(1), mask.any(0))]
