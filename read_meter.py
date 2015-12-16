import cv2
import numpy as np
import argparse

from meter_image import MeterImage
from dial import Dial
from reading_calculator import calculate_reading

# Add and getcommand line arguments and flags
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to image')
ap.add_argument('-d', '--dials', required=False, default='4', help='Number of dials in image')
ap.add_argument('-t', '--template', required=False, default='template/dial.jpg', help='Template of dial ')
cmd_args = vars(ap.parse_args())

# Get image from command line and make a copy for output visuals
meter_img = MeterImage(image_fname=cmd_args['image'])
output_img = meter_img.image().copy()

# Find positions of dials in image
dial_properties = meter_img.find_dials(num_dials=int(cmd_args['dials']))

# Read in the template image for the dial needle
template = cv2.imread(cmd_args['template'], 0)

dials = []
for (x,y,r) in dial_properties: 
    # Draw each dial on output image
    cv2.circle(output_img, (x,y), r, (0,255,0), 2)

    # Rightmost dial (dials[0]) is clockwise, then 
    # alternates clockwise and anti-clockwise
    dial_clockwise = (len(dials) % 2 == 1)

    # Create new Dial instance, determine position of hand, 
    # draw orientation on output image and add to list of dials
    d = Dial(center=(x,y), radius=r, image=meter_img, dial_template=template, clockwise=dial_clockwise)
    d.draw_needle_orientation(output_img)
    dials.append(d)

# Re-order dials from L to R
dials.reverse()

# Calculate and print meter reading to console
print "Meter Reading: ", calculate_reading(dials)

# Display image in viewer, press any key to exit viewer
cv2.imshow('found dials', np.hstack([output_img]))
cv2.waitKey(0)