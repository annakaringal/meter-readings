import cv2
import numpy as np
import math

from meter_image import MeterImage 

class Dial:
    def __init__(self, **kwargs):
        self.center = kwargs.get('center',0)
        self.radius = kwargs.get('radius',0)

        meter_img = kwargs.get('image')
        self.cropped = self.crop_dial(meter_img)
        self.threshold = self.threshold_img(self.cropped)

        self.calculate_needle_properties()

    def crop_dial(self, meter_img):
        x,y = self.center
        r = self.radius * 1.2
        return meter_img.image().copy()[y-r:y+r, x-r:x+r]

    def threshold_img(self, img): 
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 2)

    def calculate_needle_properties(self):
        needle = self.find_needle_object()
        self.ellipse = cv2.fitEllipse(needle)
        (self.needle_x,self.needle_y),(self.MA, self.ma), self.orientation = self.ellipse
        self.orientation = self.orientation - 90

    def find_needle_object(self):
        (contours, _h) = cv2.findContours(self.threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = sorted(contours, key = cv2.contourArea, reverse=True)
        return conts[0]

    def needle_orientation(self):
        return self.orientation

    def draw_ellipse_with_orientation(self, **kwargs):
        ellipse_color = kwargs.get('ellipse_color', (147,20,255))
        line_color = kwargs.get('line_color', (0,255,0))
        line_width = kwargs.get('line_width', 2)

        rows, cols = self.cropped.shape[:2]
        o_rads = math.radians(self.needle_orientation()) 
        vx = math.cos(o_rads)
        vy = math.sin(o_rads)
        l = int((-self.needle_x * vy/vx) + self.needle_y)
        r = int(((cols - self.needle_x )* vy/vx)+ self.needle_y)

        copy = self.cropped.copy()
        cv2.ellipse(copy, self.ellipse, ellipse_color,line_width)
        cv2.line(copy, (cols-1,r),(0,l),line_color,line_width)
        return copy

    def values(self): 
        return [self.lval, self.rval]

    def between_values(self):
        return self.lval != self.rval

    def between_0_and_9(self):
        return (0 in self.values() and 9 in self.values())