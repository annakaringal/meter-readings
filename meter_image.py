import cv2
import numpy as np
from itertools import groupby
from collections import Counter

IMG_DIMENSIONS = [640, 480]

class MeterImage: 
    """
    Class that reads an image of a meter from a file and finds the positions
    and radii of the dials in the image.
    """

    def __init__(self, **kwargs):
        fname = kwargs.get("image_fname")
        self.img = self.read_and_resize(fname)
        if len(self.img.shape) is 2: 
            self.gray = self.img.copy()
        else: 
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def image(self): 
        return self.img

    def gray(self): 
        return self.gray

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
        threshold = kwargs.get("threshold", 360)

        # Find possible dials
        possible_dials = cv2.HoughCircles(self.gray, cv2.cv.CV_HOUGH_GRADIENT, dp, min_d,
                        param1=threshold, param2=threshold, minRadius=min_r, maxRadius=max_r)

        # Round dial coords & radii to ints and filter to remove non-dial circles
        if possible_dials is None:
            return possible_dials
        else: 
            possible_dials = np.round(possible_dials[0, :]).astype('int')
            dials = self.get_dials(possible_dials, num_dials)
        return dials

    def get_dials(self, all_circles, num_dials=4): 
        # dials should be on same y-axis: sort group cicles by y axis value
        sorted_by_y = sorted(map(lambda x: x.tolist(), all_circles), key=(lambda (x,y,r): y))

        # filter out any groups with less than 4 in a row
        rows = []
        for y_val, row in groupby(sorted_by_y, key=(lambda (x,y,r): y)):
            r = list(row)
            if len(r) >= num_dials:
                rows.append(sorted(r, key=(lambda (x,y,r): x)))

        # multiple rows found: do more filtering based on x coordinate & radius
        if len(rows) > 1: 
            rows_to_remove = []
            for idxr, r in enumerate(rows):
                radii_data = Counter(map(lambda x: x[2], r))
                most_common_radius = radii_data.most_common(1)[0][0]
                max_diff = (most_common_radius + most_common_radius/2) *2

                # if circle in row is too close to or too far awy from circle
                # to its right, remove from row
                circles_to_remove =[]
                for idxc, c in enumerate(r):
                    if idxc > 0:
                        diff = abs(r[idxc-1][0] - c[0])
                        if diff > max_diff: 
                            circles_to_remove.append(c)
                        if diff < c[2]+5: 
                            circles_to_remove.append(c)
                r = [c for c in r if c not in circles_to_remove]

                # if number of circles in row is less than the number of dials
                # you're looking for, remove row from list of possible dial rows
                if len(r) < num_dials: 
                    rows_to_remove.append(rows[idxr])

            # remove rows with circles too spread out
            rows =  [r for r in rows if r not in rows_to_remove]

        return rows[0]
