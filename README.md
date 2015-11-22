# Reading A ConEd Meter From An Image

Takes an image of a Con Edison dial meter and outputs the number reading to give to your Con Edison representative.

### Requirements

- Python 2.7.10
- NumPy 1.10.1
- OpenCV 2.4.12

### Setup

Create and activate a new virtualenv: 
````
$ virtualenv mr-env
$ source mr-env/bin/activate
````
Install requirements: 
````
$ pip install -r requirements.txt
````

Install OpenCV using Homebrew.
````
$ brew install opencv
````
(Pick the OpenCV command to install)

Navigate to `mr-env/lib/python2.7/site-packages` and create a symlink to your version of OpenCV's Python modules. The paths may change depending on the location of your Open CV python packages.
````
$ ln -s /usr/local/Cellar/opencv/2.4.12/lib/python2.7/site-packages/cv.py cv.py
$ ln -s /usr/local/Cellar/opencv/2.4.12/lib/python2.7/site-packages/cv2.so cv2.so
````

### Usage

First run your virtualenv, then run the program: 
````
$ source mr-env/bin/activate
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