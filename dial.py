from meter_image import MeterImage 

class Dial:
    def __init__(self, **kwargs):
        self.center = kwargs.get('center',0)
        self.radius = kwargs.get('radius',0)

    def values(self): 
        return [self.lval, self.rval]

    def between_values(self):
        return self.lval != self.rval

    def between_0_and_9(self):
        return (0 in self.values() and 9 in self.values())