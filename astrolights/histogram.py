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

    def cut(e):
        if e < 0:
            return 0
        elif e > 65535:
            return 65535
        else:
            return e

    def cutRow(r):
        vfunc = np.vectorize(cut)
        r = vfunc(r)
        return r


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

    # Transform the data in pandas dataframes
    newBlue_df = pd.DataFrame(newBlue)
    newGreen_df = pd.DataFrame(newGreen)
    newRed_df = pd.DataFrame(newRed)
    
    # cut the values to have only a 16bits bitdepth.
    newBlue_cut = newBlue_df.apply(cutRow).values
    newGreen_cut = newGreen_df.apply(cutRow).values
    newRed_cut = newRed_df.apply(cutRow).values

    # Remerge the 3 channels in one image
    newImage = cv2.merge((newBlue_cut, newGreen_cut, newRed_cut))

    return newImage

def normalizeHistogram(BGR_image, methode='statisitc'):
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

    sigmaMult = 3
    dataMean = l.mean()
    dataStd = l.std()
    normalizationRange = (dataMean - dataStd*sigmaMult, dataMean + dataStd*sigmaMult)
    res = np.array([[process(elem, normalizationRange) for elem in line] for line in l])
    res = res - res.min()
    res = res * 100/res.max()
    res = res.astype(np.float32, copy=False)
    lab_image = cv2.merge((res,a,b))
    BGR_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR);
    BGR_image *= 2**16 - 1

    return BGR_image
