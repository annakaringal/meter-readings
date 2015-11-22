import cv2
import numpy as np

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
        # Get kwargs
        dp = kwargs.get("dp", 20)
        min_d = kwargs.get("min_dist", 30)
        min_r = kwargs.get("min_radius", 25)
        max_r = kwargs.get("max_radius", 60)

        # Find possible dials
        possible_dials = cv2.HoughCircles(self.gray, cv2.cv.CV_HOUGH_GRADIENT, dp, min_d,
                        minRadius=min_r, maxRadius=max_r)

        if possible_dials is not None: 
            possible_dials = np.round(possible_dials[0, :]).astype('int')
            output = self.img.copy()
            for (x,y,r) in possible_dials: 
                print (x,y,r)
                cv2.circle(output, (x,y), r, (0,255,0), 4)
                cv2.rectangle(output, (x-5, y-5), (x+5, y+5), (0, 127, 255), -1)
            print len(possible_dials)
            cv2.imshow('output', np.hstack([self.img, output]))
            cv2.waitKey(0)

        else: 
            print "No dials found"