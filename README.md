# Reading A ConEd Meter From An Image

Takes an image of a Con Edison dial meter and outputs the number reading to give to your Con Edison representative.

### Usage

In the working directory, run: 

````
$ python read_meter.py -i sample-data/meter1.jpeg
````

Use flag `-i` or `--i` to indicate the path of the image. In this case, the path of the image is `sample-data/meter1.jpeg` 

### Image specifications and limitations

For accuracy in readings, images must be:

- scalable to either 480x640 or 640x480 without significant distortion

- 100% of the meter must be visible

- meter should be photographed head on and not from an angle, so that the dials still appear as circles in a straight horizontal row parallel to the top and bottom edges of the photograph.

Examples of good images can be found in the folder `sample-data`. Examples of bad images can be found `sample-data/unsupported`.

Currently only supports meters where dials are in a straight row, and not in an arc.