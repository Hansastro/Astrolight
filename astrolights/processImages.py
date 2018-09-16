import numpy as np
from astrolights import raw, operations

def calculateMedianFromFiles(fileList):
    RAWdata = raw.getRawDataFromFileList(fileList)
    result = operations.calculateMedian(RAWdata)
    
    return result

def correctImages(RawImage, masterOffset, masterDark, masterFlat):

    meanFlat = np.mean(masterFlat)

    RAWimageData = raw.getRawDataFromFileList([RawImage])[0]

    masterDark = masterDark.astype(np.float64, copy=False)
    masterOffset = masterOffset.astype(np.float64, copy=False)
    masterFlat = masterFlat.astype(np.float64, copy=False)
    image = RAWimageData.astype(np.float64, copy=False)

    image = ((image - masterDark) / (masterFlat - masterOffset)) * meanFlat
        
    return image

    
def stackImages(images, method='mean'):
    if method == 'mean':
        result = np.mean(images, axis=0)
    else:
        return -1
    
    return result
