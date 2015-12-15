import cv2
import numpy as np
import math

from meter_image import MeterImage 
from functions import *

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
        # Find needle object by fitting ellipse to largest object in cropped image
        needle = self.find_needle_object()
        self.ellipse = cv2.fitEllipse(needle)
        self.needle_center,(self.MA, self.ma), self.orientation = self.ellipse

        # Calculate vector between dial center & needle center
        dial_center = tuple(map(lambda x: x/2, self.cropped.shape[:2]))
        dial_center_to_needle_center = vector(dial_center, self.needle_center)

        # Calculate vecotr between dial center and point on line
        point_on_line = line_endpoint(dial_center, self.orientation-90, self.radius)
        dial_center_to_point_on_line = vector(dial_center, point_on_line)

        # If dot product of two vectors is -1, recalculate needle  orientaiton
        if dot_product(dial_center_to_needle_center, dial_center_to_point_on_line) < 0:
            self.orientation = self.orientation + 180

    def find_needle_object(self):
        # Erode the boundaries of thresholded cropped image
        kernel = np.ones((3,3),np.uint8)
        erode_boundaries = cv2.erode(self.threshold, kernel, iterations=1)

        # Find contours of all objects
        (contours, _h) = cv2.findContours(erode_boundaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Needle is largest object 
        conts = sorted(contours, key=cv2.contourArea, reverse=True)
        return conts[0]

    def needle_orientation(self):
        return self.orientation

    def draw_needle_orientation(self, image, **kwargs): 
        """
        Draws line of needle orientation onto image
        """
        line_color = kwargs.get('line_color', (147,20,255))
        line_width = kwargs.get('line_width', 2)

        endpoint = line_endpoint(self.center, self.needle_orientation()-90, self.radius)
        cv2.line(image,self.center,endpoint,line_color,line_width)

    def draw_ellipse_with_orientation(self, **kwargs):
        """
        Returns copy of cropped grayscale image of dial with ellipse of fit 
        and ellipse orientation line drawn onto it
        """
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
