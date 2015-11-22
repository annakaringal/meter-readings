# Reading A ConEd Meter From An Image

Takes an image of a Con Edison dial meter and outputs the number reading to give to your Con Edison representative.

### Usage

In the working directory, run: 

````
$ python read_meter.py -i sample-data/meter2.jpg -d 5
````

Use flag `-i` or `--image` to indicate the path of the image. In this case, the path of the image is `sample-data/meter2.jpeg`.

Use flag `--dials` to indicate the number of dials you are looking for in the image. In this case, the number of dials is 5. If no flag is given, defaults to 4.

### Image specifications and limitations

For accuracy in readings, images must be:

- scalable to either 480x640 or 640x480 without significant distortion

- 100% of the meter must be visible

- meter should be photographed head on and not from an angle, so that the dials still appear as circles in a straight horizontal row parallel to the top and bottom edges of the photograph.

Examples of good images can be found in the folder `sample-data`. Examples of bad images can be found `sample-data/unsupported`.

Currently only supports meters where dials are in a straight row, and not in an arc.

### TODO: 

- support for meters with dials arranged in an arc
- refine circle filtering algorithm