# import the necessary packages
import cv2
from libs.stitch import Stitcher
from libs.findMatchLib import FindMatchLib
import glob
import itertools
from operator import itemgetter
import random

def main():
    # Initializing and empty list of images
    image_list = []

    # Loading all images in 'img' directory as cv.image format (numpy array in python)
    for filename in glob.glob('img/faces/*.jpg'):  # assuming jpg of same size!
        im = cv2.imread(filename)
        image_list.append(im)

    # Scrambling the order to make sure the list is not ordered beforehand :)
    random.shuffle(image_list)

    # Initializing the Stitcher calss
    stitcher = Stitcher()

    # Applying image stitching method in an order to go over all images
    while len(image_list) > 1:
        # Creating a range for search
        my_list = range(0, len(image_list))

        # Go over all pairs to find a correlation in the correct order
        for pair in itertools.combinations(my_list, r=2):
            imA = itemgetter(itemgetter(1)(pair))(image_list)
            imB = itemgetter(itemgetter(0)(pair))(image_list)

            # Stitch th pair together
            (this) = stitcher.stitch([imA, imB])

            # If a result exists then remove them from the image list and put the stitched image in
            if this.any():
                if len(image_list) > 1:
                    image_list.pop(itemgetter(0)(pair))
                    image_list.insert(0, this)
                    image_list.pop(itemgetter(1)(pair))
                else:
                    image_list.pop(itemgetter(0)(pair))
                    image_list.insert(0, this)
                break

    # Put the final result in a new variable
    result = itemgetter(0)(image_list)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # load the front-face detector Haar cascade, then detect faces
    # in the input image
    detector = cv2.CascadeClassifier('models/faces.xml')
    rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(10, 10))


    ####################################################################################
    ####################################################################################
    # Search the library (here only one template) to find it within the detected objects
    find_best = FindMatchLib()
    template = cv2.imread('template/template.jpg')
    value = []

    # expand the bounding boxes a little bit as they are very tight to work with
    # Canny edge feature matching method
    px_y = 10
    px_x = 10

    # Search over all bounding boxes and save the maximum correlation value
    for (x, y, w, h) in rects:
        if (y-px_y > 0) and (y+h+px_y < result.shape[1]) and (x-px_x > 0) and (y+h+px_x < result.shape[0]):
            value.append(find_best.findValue(result[y-px_y:y+h+px_y, x-px_x:x+w+px_x], template))
            this = cv2.rectangle(itemgetter(0)(image_list), (x, y), (x + w, y + h), (255, 0, 0), 5)
        else:
            value.append(find_best.findValue(result[y:y + h, x:x + w], template))
            this = cv2.rectangle(itemgetter(0)(image_list), (x, y), (x + w, y + h), (255, 0, 0), 5)

    # Select the maximum correlation index and load the related message
    (x, y, w, h) = rects[value.index(max(value))]
    this = cv2.rectangle(this, (x, y), (x + w, y + h), (255, 0, 255), 5)

    with open('template/template.txt', 'r') as myfile:
        data = myfile.read().replace('\n', '')

    cv2.putText(this, data, (y,x), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 1)

    # Show the final result
    cv2.imshow("Image Final Detection", this)
    cv2.waitKey(0)

    return 0

if __name__ == "__main__":
    main()