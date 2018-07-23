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

    convert OFFSET_*.tif -evaluate-sequence median Bias.tif

## Flat images
The flat images capture some defects in the optical path. Vigneting or dust on the sensor for example.

### How to get them?
- Set the ISO as the planned one.
- Set the aperture to the planned one
- take between 10 and 20 images of a uniformly enlighted surface. 

### How to process all those images?
### Processing

## Dark images
### How to get them?
### How to process all those images?
### Processing

## Processing the images
### How to get them?
### How to process all those images?
### Processing

### Aligning the images

### merge all images
