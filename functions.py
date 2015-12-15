import math

def line_endpoint(start, angle, length ):
    """ Returns point at end of line with characteristics of given params """
    rads = math.radians(angle) 
    x0, y0 = start
    vx = math.cos(rads)
    vy = math.sin(rads)
    return (int(vx * length + x0), int(vy * length + y0))

def dot_product(a,b):
    """ Returns dot product of 2x1 matrices A and B) """
    return a[0] * b[0] + a[1] * b[1]

def vector(p1, p2): 
    """ Returns vector between 2D points p1 and p2 """ 
    return (p2[0]-p1[0], p2[1]-p1[1])