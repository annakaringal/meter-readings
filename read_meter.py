import cv2
import numpy as np
import argparse
from meter_image import MeterImage

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to image')
ap.add_argument('-d', '--dials', required=False, default='4', help='Number of dials in image')
cmd_args = vars(ap.parse_args())

meter_img = MeterImage(image_fname=cmd_args['image'])
output = meter_img.image().copy()

# Find positions of image
dial_properties = meter_img.find_dials(num_dials=int(cmd_args['dials']))

dials = []
for (x,y,r) in dial_properties: 
    # Draw dials on output image
    cv2.circle(output, (x,y), r, (0,255,0), 2)



# Display image in viewer, press any key to exit viewer
cv2.imshow('output', np.hstack([meter_img.image(), output]))
cv2.waitKey(0)

