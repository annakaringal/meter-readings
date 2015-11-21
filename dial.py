class Dial:

    def __init__(self, **args):
        self.lval = lval
        self.rval = rval

    def values(self): 
        return [self.lval, self.rval]

    def between_values(self):
        return self.lval != self.rval

    def between_0_and_9(self):
        return (0 in self.values and 9 in self.values)