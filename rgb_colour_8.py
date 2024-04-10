#Alternate way to implement common cathode RGB LED control

rgb_values = []

def rgb_colour_8(colour):
    """Provides the necessary combination of ones and zeroes to produce 7 colours and black (off),
    with a common cathode 4 legged RGB-LED into a list named rgb_values.
    Usage: 
    1. Define a global empthy list named rgb_values.
    2. Call rgb_colour_8() with the desired colour as string type argument, for example: rgb_colour_8("red").
    3. Assign the values to output pins connected to legs of RGB LED,
    for example: red_pin.value(rgb_values[0]) green_pin.value(rgb_values[1]), blue_pin.value(rgb_values[2])
    4. Enjoy the light show."""
    
    colours = {"red" : [1, 0, 0], "green" : [0, 1, 0], "blue" : [0, 0, 1], "white" : [1, 1, 1],
               "violet" : [1, 0, 1], "cyan" : [0, 1, 1], "yellow" : [1, 1, 0], "off" : [0, 0, 0]}
    
    if len(rgb_values) == 3:
    #Makes sure that the list is empthy when values are inserted
    #Used to prevent the list from growing wildly
        rgb_values.clear()
        
        if colour in colours:
            rgb_values.insert(0, colours[colour][0]) 
            rgb_values.insert(1, colours[colour][1]) 
            rgb_values.insert(2, colours[colour][2]) 
        else:
            print("Something went wrong, perhaps a wrong colour was chosen?")
    else:

        if colour in colours:
            rgb_values.insert(0, colours[colour][0]) 
            rgb_values.insert(1, colours[colour][1]) 
            rgb_values.insert(2, colours[colour][2]) 
        else:
            print("Something went wrong, perhaps a wrong colour was chosen?")
