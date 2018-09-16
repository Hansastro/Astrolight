import os
import cv2
import numpy as np

from astrolights import files, raw

def getRawDataFromFileList(filesList):
    RAWfiles = raw.uncompressRawFiles(filesList)
    RAWdata = raw.getRAWdata(RAWfiles)

    return RAWdata

def uncompressRawFiles(rawFileList):
    '''
    Generate a pgm file from a raw file.
    
    Parameters:
    rawFileList as a list of strings. this parameter is the list of some filenames of camera RAW files.
    
    return value:
    a list of the generated files (with their path)
    '''
    generatedFiles = []
    for file in rawFileList:
        # Extract Raw data in a PGM file with dcraw
        print('dcraw -d -4 -t 0 ' + file)
        os.system('dcraw -d -4 -t 0 ' + file)
        generatedFiles.append(files.getFileName(file, removeExtention=True, removePath=False) + '.pgm')

    #print(generatedFiles)
    return generatedFiles



def getRAWdata(rawFileList):
    '''
    Get the image raw data from a list of pgm files
    
    Parameters:
    rawFileList as a list of string. each element of the list is a string of the filname of a pgm file containing the raw data.
    
    Return Value:
    an array of array containing all images RAW data. Each element is an image.
    '''
    fileList = rawFileList[:]
    fileName = fileList[0]
    image = _correctImageOrientation(cv2.imread(fileList.pop(0), flags=cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYDEPTH), fileName = fileName)
    stackList = [image]

    for file in fileList:
        image = _correctImageOrientation(cv2.imread(file, flags=cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYDEPTH), fileName = file)
        stackList.append(image)
    
    stack = np.stack(stackList)
    
    return stack

def _correctImageOrientation(image, fileName='Unknown'):
    if image.shape[0] > image.shape[1]:
        print('Reorient image: {}'.format(fileName))
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image
        #return image[::-1].T
    else:
        return image
