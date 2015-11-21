from dial import Dial

"""
Module that takes in the position information of four dials and calculates
the resulting ConEd reading using the dial reading information guide:
http://www.coned.com/customercentral/meter-reading-written.asp

"""

def calculate_reading(dials): 
    reading_vals = []

    # read dials from right to left
    for idx, dial in enumerate(reversed(dials)): 
        # dial hand is between numbers
        # go with the lower number unless between 0 and 9:
        if dial.between_values(): 
            if not dial.between_0_and_9(): 
                val = min(dial.values())
            else: 
                val = 9

        # dial hand is directly on a number: look at dial on right (if any)
        # if value of dial on right is between 0 and 7, set value to 
        # one less than value
        else:
            print idx, len(dials)-1, reading_vals[-1] >= 7
            if idx != len(dials)-1 and reading_vals[-1] >= 7: 
                print "here"
                val = dial.values()[0] - 1
            else:
                val = dial.values()[0]

        reading_vals.append(val);

    return ''.join(reading_vals())
