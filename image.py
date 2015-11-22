import cv2
import numpy as np
from itertools import groupby

IMG_DIMENSIONS = [640, 480]

class Image: 

    def __init__(self, **kwargs):
        fname = kwargs.get("image_fname")
        self.img = self.read_and_resize(fname)
        if len(self.img.shape) is 2: 
            self.gray = self.img.copy()
        else: 
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def read_and_resize(self, fname):
        img = cv2.imread(fname)
        width, length, colors = img.shape
        if width > length: 
            l, w= IMG_DIMENSIONS
        else: 
            w, l= IMG_DIMENSIONS
        return cv2.resize(img, (w,l))

    def find_dials(self, **kwargs):
        # Get kwargs for number of dials to look for
        num_dials = kwargs.get("num_dials", 4)

        # Get kwargs for Hough Circle Transform. Defaults are calibrated to sample-data image
        dp = kwargs.get("dp", 20)
        min_d = kwargs.get("min_dist", 30)
        min_r = kwargs.get("min_radius", 25)
        max_r = kwargs.get("max_radius", 60)

        # Find possible dials
        possible_dials = cv2.HoughCircles(self.gray, cv2.cv.CV_HOUGH_GRADIENT, dp, min_d,
                        minRadius=min_r, maxRadius=max_r)

        if possible_dials is None:
            return possible_dials
        else: 
            possible_dials = np.round(possible_dials[0, :]).astype('int')
            dials = self.get_dials(possible_dials, num_dials)

            # Draw dials on copy of image
            output = self.img.copy()
            for (x,y,r) in dials: 
                cv2.circle(output, (x,y), r, (0,255,0), 4)
                cv2.rectangle(output, (x-5, y-5), (x+5, y+5), (0, 127, 255), -1)

            # Display image in viewer, press any key to exit viewer
            cv2.imshow('output', np.hstack([self.img, output]))
            cv2.waitKey(0)

        return dials

    def get_dials(self, all_circles, num_dials=4): 
        # dials should be on same y-axis: sort group cicles by y axis value
        sorted_by_y = sorted(map(lambda x: x.tolist(), all_circles), key=(lambda (x,y,r): y))

        # filter out any groups with less than 4 in a row
        rows = []
        for y_val, circ in groupby(sorted_by_y, key=(lambda (x,y,r): y)):
            c = list(circ)
            if len(c) >= 4:
                rows.append(c)

        return all_circles
