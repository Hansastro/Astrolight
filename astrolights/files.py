import os
import re
import xml.etree.ElementTree

def listAllFileinDir(path, regex='.*'):
    fileFilter = re.compile(regex)
    listFiles = [] 
    for f in os.listdir(path):
        if fileFilter.match(f):
            listFiles.append(path + '/' + f)
    return listFiles

def getFileName(fileName, removeExtention=False, removePath=True):
    '''
    get the name of a file from a string (can remove the extention or the complete path)
    
    parameters:
    fileName as a string. The name can include the path
    removeExtention as boolean. Default is False. This parameter remove the extention of the filename. (e.g: 'test.jpg'
    will become 'test')
    removePath as boolean. Default is True. If the complete path is given in the filename is it possible to remove it or not
    
    return value:
    the filename
    
    '''
    if removePath:
        fileName = os.path.basename(fileName)
    if removeExtention:
        re_catchFileName = re.compile('(.*)\..*$')
        catchFileNameResult = re_catchFileName.match(fileName)
        if catchFileNameResult:
            fileName = catchFileNameResult.group(1)

    return fileName

def categorifyRawImages(imageDirectory):
    '''
    Create a dictionary of the files in a directory. The category is the title and only photo with a rating greater than 2 will be treated
    '''
    
    xmpFileNamePattern = re.compile('^(.*\.CR2).xmp$')

    categories = {}


    def _parse_nsmap(file):
        '''
        Create a dictionary of xmlns tags
        '''
        NS_MAP = "xmlns:map"

        events = "start", "start-ns", "end-ns"

        root = None
        ns_map = []

        for event, elem in xml.etree.ElementTree.iterparse(file, events):
            if event == "start-ns":
                ns_map.append(elem)
            elif event == "end-ns":
                ns_map.pop()
            elif event == "start":
                if root is None:
                    root = elem
                elem.set(NS_MAP, dict(ns_map))

        return xml.etree.ElementTree.ElementTree(root)

    listFiles = os.listdir(imageDirectory)
    for f in listFiles:
        if xmpFileNamePattern.match(f):
            rawFileName = xmpFileNamePattern.match(f).group(1)
            #print('Parsing: {}'.format(f))
            #e = xml.etree.ElementTree.parse(imageDirectory + '/' + f).getroot()
            e = _parse_nsmap(imageDirectory + '/' + f).getroot()
            #print(e.tag)
            #print(e.attrib)
            for level2 in e:
                #print(level2.tag)
                for level3 in level2:
                    rating = level3.attrib['{{{}}}Rating'.format(level3.attrib['xmlns:map']['xmp'])]
                    rating = int(rating)
                    #print('Rating: {}'.format(rating))
                    for t in level3:
                        if t.tag == '{{{}}}title'.format(level3.attrib['xmlns:map']['dc']):
                            for elem in t:
                                for li in elem:
                                    title = li.text
                                    #print('Title: {}'.format(title))
            if rating >= 2:
                if title not in categories:
                    categories[title] = [imageDirectory + '/' + rawFileName]
                else:
                    categories[title].append(imageDirectory + '/' + rawFileName)

    return categories
