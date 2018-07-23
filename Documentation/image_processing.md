# Astro image processing

To process Astro Photographie several path are needed. Before compositing the images the offet, dark and flat must be treated.

## Offset images
The offset images (also callsed bias images) represent the minimum value the camera can deliver. The black value of a completly black image will be not 0.
The offset must be removed on all images.

### How to get them?
- Put a cache on the objectiv (all must be in black)
- Take beetween 10 and 20 photos with the shorter exposition time and the planned ISO setting.
- Note: the aperture is not relevant.

### How to process all those images?
Simply make a median of all images.

You obtained: the MasterOffset.

### Processing
With image magick the processing can be done with this command line:

    convert OFFSET_*.tif -evaluate-sequence median MasterOffset.tif

## Flat images
The flat images capture some defects in the optical path. Vigneting or dust on the sensor for example.

### How to get them?
- Set the ISO as the planned one.
- Set the aperture to the planned one
- take between 10 and 20 images of a uniformly enlighted surface. 

### How to process all those images?
- each flat images has to be substracted with the MasterOffset.
- a median is done with all resulting images

### Processing
In command line and with image magick this operation is possible:

    for i in FLAT*.tif; do echo $i; convert $i ./MasterOffset.tif -evaluate-sequence subtract CORRECTED_´basename $i´;done
    convert CORRECTED_FLAT*.tif -evaluate-sequence median MasterFlat.tif
    
## Dark images
The dark images (also called black) capture the noise of the camera during the long exposure. They are the less funny to get because the photos must have the same exposure than the target photos.

### How to get them?
- put the cache on the camera.
- take between 10 and 20 images with the ISO set to the target ISO and with the planned exposure time.
- The camera must be at the same temperature as the one during the images. The noise is very dependent of the temperature.

### How to process all those images?
It is the same process than the flat:
- each images are substracted to the MasterOffset
- a median is done with all resulting images

### Processing
We follow the same process than for the Flat. In command line and with ImageMagick:

    for i in DARK*.tif; do echo $i; convert $i ./MasterOffset.tif -evaluate-sequence subtract CORRECTED_´basename $i´;done
    convert CORRECTED_BLACK*.tif -evaluate-sequence median MasterBlack.tif

## Processing the images
### How to get them?
### How to process all those images?
### Processing

### Aligning the images

### merge all images
