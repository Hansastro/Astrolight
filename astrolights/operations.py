import numpy as np

def calculateMedian(RAWdataList):
    '''
    Calculate the median of a stack of RAW images
    
    Parameters:
    RAWdataList as an array of array of all images.
    
    Return value:
    The median of each pixel of the image stack
    '''
        
    #offsetStack = np.stack(offsetStackList)
    result = np.median(RAWdataList, axis=0)
    
    return result
