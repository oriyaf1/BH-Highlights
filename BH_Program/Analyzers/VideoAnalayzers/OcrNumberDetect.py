# BH_Program/Analyzers/VideoAnalayzers/OcrNumberDetect.py

import cv2
import numpy as np
import operator
import os

MIN_CONTOUR_AREA = 10
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30
FILE_TO_TEST = " "


class ContourWithData():
    npaContour = None  # contour
    boundingRect = None  # bounding rect for contour
    intRectX = 0  # bounding rect top left corner x location
    intRectY = 0  # bounding rect top left corner y location
    intRectWidth = 0  # bounding rect width
    intRectHeight = 0  # bounding rect height
    fltArea = 0.0  # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):  # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA: return False
        return True


class NumberOCR:

    def __init__(self, type='type0'):
        self.type = type
        self.npaClassifications = np.loadtxt("OcrFile/{0}classifications.txt".format(type),
                                             np.float32)  # read in training classifications
        self.npaFlattenedImages = np.loadtxt("OcrFile/" + type + "flattened_images.txt",
                                             np.float32)  # read in training images
        npaClassifications = self.npaClassifications.reshape(
            (self.npaClassifications.size, 1))  # reshape numpy array to 1d, necessary to pass to call to train
        self.kNearest = cv2.ml.KNearest_create()  # instantiate KNN object
        self.kNearest.train(self.npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    def imageToString(self, frameToStr):

        allContoursWithData = []  # declare empty lists,
        validContoursWithData = []  # we will fill these shortly

        imgGray = cv2.cvtColor(frameToStr, cv2.COLOR_BGR2GRAY)  # grayscale image
        imgBlurred = cv2.GaussianBlur(imgGray, (1, 1), 0)  # blur
        _, imgThresh = cv2.threshold(imgGray, 255, 255, cv2.THRESH_OTSU)
        imgThreshCopy = imgThresh.copy()  # this in necessary b/c findContours modifies the image

        imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for npaContour in npaContours:  # for each contour
            contourWithData = ContourWithData()  # instantiate a contour with data object
            contourWithData.npaContour = npaContour  # assign contour to contour with data
            contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)  # get the bounding rect
            contourWithData.calculateRectTopLeftPointAndWidthAndHeight()  # get bounding rect info
            contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)  # calculate the contour area
            allContoursWithData.append(contourWithData)  # list of all contours with data

        for contourWithData in allContoursWithData:  # for all contours
            if contourWithData.checkIfContourIsValid():  # check if valid
                validContoursWithData.append(contourWithData)  # if so, append to valid contour list

        validContoursWithData.sort(key=operator.attrgetter("intRectX"))  # sort contours from left to right
        strFinalString = ""

        for contourWithData in validContoursWithData:  # for each contour
            if __name__ == "__main__":
                # draw a green rect around the current char
                cv2.rectangle(frameToStr,  # draw rectangle on original testing image
                              (contourWithData.intRectX, contourWithData.intRectY),  # upper left corner
                              (contourWithData.intRectX + contourWithData.intRectWidth,
                               contourWithData.intRectY + contourWithData.intRectHeight),  # lower right corner
                              (0, 255, 0),  # green
                              1)  # thickness

            imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                     contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
            npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
            npaROIResized = np.float32(npaROIResized)

            retval, npaResults, neigh_resp, dists = self.kNearest.findNearest(npaROIResized, k=1)

            if (float(dists) < 4000000):
                strFinalString = strFinalString + str(chr(int(npaResults[0][0])))
        # end for

        if __name__ == "__main__":
            print("########\n" + strFinalString + "\n########")
            cv2.imshow('test image', frameToStr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return strFinalString


if __name__ == "__main__":
    my_ocr = NumberOCR('type1')
    #FILE_TO_TEST = cv2.imread("")
    #my_ocr.imageToString(FILE_TO_TEST)
    #FILE_TO_TEST = cv2.imread("")
    #my_ocr.imageToString(FILE_TO_TEST)
    #FILE_TO_TEST = cv2.imread("")

# end if
