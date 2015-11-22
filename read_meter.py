import argparse
from image import Image

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to image')
ap.add_argument('-d', '--dials', required=False, default='4', help='Number of dials in image')
cmd_args = vars(ap.parse_args())

img = Image(image_fname=cmd_args['image'])
dials = img.find_dials(num_dials=int(cmd_args['dials']))