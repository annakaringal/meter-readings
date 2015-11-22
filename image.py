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
            w, l = IMG_DIMENSIONS
        else: 
            l,w = IMG_DIMENSIONS
        return cv2.resize(img, (w,l))