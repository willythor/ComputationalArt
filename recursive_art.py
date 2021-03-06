""" Willem Thorbecke
	Computational Art of the Bokeh-y Variety 
	Feb, 2016
"""

from __future__ import division
import random
from PIL import Image
import math



def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
        
    """
    #this function was tested through displaying it in the generate_art function
    #added the building blocks sum and difference 
    building_blocks = ["prod", "avg", "sum", "dif", "sin_pi", "cos_pi"]

    depth_midpoint = float((max_depth - min_depth))/2

    if max_depth == 1:
    	if .5 < random.random():
    		return ["x"]
    	else:
    		return ["y"]
    elif min_depth == 1:
    	if depth_midpoint < random.uniform(min_depth, max_depth):
    		if .5 < random.random():
    			return ["x"]
    		else:
    			return ["y"]
    	else:
    		return build_random_function(min_depth - 1, max_depth - 1)

    i = random.randint(0,5) #the range (0,3) [excluding trig functions] produces a much calmer, more bokeh-y image 


    z = build_random_function(min_depth - 1, max_depth - 1)

    if i in [0,1,2,3]:
    	return [building_blocks[i], z, build_random_function(min_depth - 1, max_depth - 1)]
    else:
    	return [building_blocks[i], z]	
     	


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['sin_pi', ['y']],10,3.14)
        -0.42577929156507327
        >>> evaluate_random_function(['avg', ['y'], ['x']],10,8)
        9.0
        >>> evaluate_random_function(['avg', ['y'], ['sin_pi', ['y']]],10,8)
        3.9999999999999996
      

    """
    	#purpose/works of each function:
    	#x*y = prod
    	#(x+y)/2.0 = avg
    	#math.sin(pi*x)
    	#math.cos(pi*x)
    	#a + b for sum
    	#a - b for difference, where a and b are the following items in the function list

    if f[0][0] == "x":
    	return x
    elif f[0][0] == "y":
    	return y
    elif f[0] == "cos_pi":
     	return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    elif f[0] == "sin_pi":
    	return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    elif f[0] == "avg":
    	return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))/2.0
    elif f[0] == "prod":
    	return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == "sum":
    	return evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)
    elif f[0] == "dif":
     	return evaluate_random_function(f[1], x, y) - evaluate_random_function(f[2], x, y)
   


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    a = val - float(input_interval_start) 
    b = float(input_interval_end) - val
    ratio_input = a/(a+b)
    difference_output = output_interval_end - output_interval_start
    new_val = ratio_input*difference_output + output_interval_start
    return new_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    # red_function = ["x"]
    # green_function = ["y"]
    # blue_function = ["x"]

    red_function = build_random_function(7, 9)
   #the print statement below was used to test build_random_function
   #print red_function
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()


    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")
   

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    test_image("noise.png")
