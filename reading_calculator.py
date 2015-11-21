from dial import Dial

class ReadingCalculator: 
    """
    A class that takes in the position information of four dials and calculates
    the resulting ConEd reading using the dial reading information guide:
    http://www.coned.com/customercentral/meter-reading-written.asp
    """

    def __init__(self, dials):
        """
        Initialize from list of dials in order where leftmost is at position 0 
        in list and rightmost is at last position.
        """
        self.dials = dials

    def calculate(self): 
        reading_vals = []

        # read dials from right to left
        for idx, dial in enumerate(dials.reverse()): 
            # dial hand is between numbers
            # go with the lower number unless between 0 and 9:
            if dial.between_values: 
                if not dial.between_0_and_9: 
                    val = min(dail.values)
                else: 
                    val = 9

            # dial hand is directly on a number: look at dial on right (if any)
            # if value of dial on right is between 0 and 7, set value to 
            # one less than value
            else:
                val = dial.values[0]
                if not idx == len(dials)-1 and reading_vals[-1] >= 7: 
                        val = dial.values[0] - 1

            reading_vals.append(val);

        return ''.join(reading_vals())
