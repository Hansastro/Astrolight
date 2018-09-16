import cv2
import numpy as np
import pandas as pd

def ajustWhiteBalance(BGR_image):
    '''
    Ajust the white balance of an BGR image.

    The algorithm used is the greyworld algorithm.
    The mean of each channel are aligned on the mean of all of them.

    Paramaters:
    - BGR_image: an opencv BGR image
    
    returned value:
    - the corrected image
    '''

    blue, green, red = cv2.split(BGR_image)

    # Calculates the mean of each channel
    blueMean = blue.mean()
    greenMean = green.mean()
    redMean = red.mean()

    # Calculates the mean of all channels
    overallMean = (blueMean + greenMean + redMean ) / 3

    # Correct the values for each channel
    newBlue = blue + (overallMean - blueMean)
    newGreen = green + (overallMean - greenMean)
    newRed = red + (overallMean - redMean)

    # cut the values to have only a 16bits bitdepth.
    newBlue[newBlue < 0] = 0
    newBlue[newBlue > 65535] = 65535
    newGreen[newGreen < 0] = 0
    newGreen[newGreen > 65535] = 65535
    newRed[newRed < 0] = 0
    newRed[newRed > 65535] = 65535


    # Remerge the 3 channels in one image
    newImage = cv2.merge((newBlue, newGreen, newRed))

    return newImage

def normalizeHistogram(BGR_image, methode='statistic', sigma=3, sigma1=None, sigma2=None):
    '''
    Normalize the histogram of an image
    '''
    def process(elem, normalization):
        if elem < normalization[0]:
            return normalization[0]
        elif elem > normalization[1]:
            return normalization[1]
        else:
            return elem

    # Convert the image in Lab format and split per channel
    BGR_image = BGR_image.astype(np.float32, copy=False)
    BGR_image /= BGR_image.max()
    lab_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2LAB);
    l, a, b = cv2.split(lab_image)

    if sigma1 == None:
        sigma1 = sigma
    if sigma2 == None:
        sigma2 = sigma
    dataMean = l.mean()
    dataStd = l.std()
    normalizationRange = (dataMean - dataStd*sigma1, dataMean + dataStd*sigma2)
    res = np.array([[process(elem, normalizationRange) for elem in line] for line in l])
    res = res - res.min()
    res = res * 100/res.max()
    res = res.astype(np.float32, copy=False)
    lab_image = cv2.merge((res,a,b))
    BGR_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR);
    BGR_image *= 2**16 - 1

    return BGR_image

def shiftHistorgram(BGR_image, shift):
    '''
    Shift the histogram

    parameters:
    shift: single value or list of 3 values one for each channel
    
    returns:
    a GBR image with shifted histogram
    '''
    
    B, G, R = cvs.split(BGR_image)
    if len(shift) == 3:
        B += shift[0]
        G += shift[1]
        R += shift[2]
    else:
        B += shift
        G += shift
        R += shift

    B[B<0] = 0
    B[B>65535] = 65535
    G[G<0] = 0
    G[G>65535] = 65535
    R[R<0] = 0
    R[R>65535] = 65535
    
    return cv2.merge((B, G, R))
    
    
