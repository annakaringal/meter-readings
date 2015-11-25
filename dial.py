import cv2
import numpy as np

from meter_image import MeterImage 

class Dial:
    def __init__(self, **kwargs):
        self.center = kwargs.get('center',0)
        self.radius = kwargs.get('radius',0)

        meter_img = kwargs.get('image')
        self.cropped = self.crop_dial(meter_img)
        self.threshold = self.threshold_img(self.cropped)

    def crop_dial(self, meter_img):
        x,y = self.center
        r = self.radius * 1.2
        return meter_img.image().copy()[y-r:y+r, x-r:x+r]

    def threshold_img(self, img): 
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 2)

    def between_values(self):
        return self.lval != self.rval

    def between_0_and_9(self):
        return (0 in self.values() and 9 in self.values())