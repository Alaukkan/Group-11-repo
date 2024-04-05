import random
import time
from machine import Pin

button_red = Pin(18, Pin.IN, Pin.PULL_UP)
button_green = Pin(17, Pin.IN, Pin.PULL_UP)
button_blue = Pin(16, Pin.IN, Pin.PULL_UP)

LED_RED = Pin(11, Pin.OUT)
LED_GREEN = Pin(12, Pin.OUT)
LED_BLUE = Pin(13, Pin.OUT)

buttons = [button_red, button_green, button_blue]
led = [LED_RED, LED_GREEN, LED_BLUE]
color = ["red", "green", "blue"]

status = {
    "requesting" : "none"
}

def request_food():
    """
    A random number is generated which decides what food item the Robo Pet
    wants by accessing the element in the led list. Robopet
    indicates what food it wants by a colored LED. 
    """
    item = random.randint(0, len(led) - 1)
    status["requesting"] = led[item]
    print(f"requesting food: {color[item]}")
    time.sleep(0.5)
    status["requesting"].high()
    return

def check_food():
    """
    Checks if the food is correct.
    If it is, returns "correct", else "wrong".
    Has a 20 second timer, if it runs out, returns "timed out"
    """
    start_time = time.time()
    while time.time() - start_time < 20:  # 20 seconds timer
        time.sleep(0.01)
        for i in range(0,3):
            if buttons[i].value() == 0:
                print(f"{color[i]} was pressed in {time.time() - start_time} seconds")
                if led[i] == status["requesting"]:
                    return "correct"
                else:
                    return "wrong"
    print("Timed out")
    return "timed out"
    
def check_food_2():
    """
    Checks if the food is correct.
    If it is, returns "correct", else "wrong".
    Has a 20 second timer, if it runs out, returns "timed out"
    """
    start_time = time.time()
    while time.time() - start_time < 20:  # 20 seconds timer
        time.sleep(0.01)
        if buttons[0].value() == 0 and status["requesting"] == led[0]:
            print(f"Red was pressed in {time.time() - start_time} seconds")
            return "correct"
        elif buttons[1].value() == 0 and status["requesting"] == led[1]:
            print(f"Green was pressed in {time.time() - start_time} seconds")
            return "correct"
        elif buttons[2].value() == 0 and status["requesting"] == led[2]:
            print(f"Blue was pressed in {time.time() - start_time} seconds")
            return "correct"
    print("Timed out")
    return "timed out"

def correct_food():
    """
    If the food is correct, all leds flash for 2 seconds
    """
    status["requesting"].low()
    for i in range(5):
        LED_RED.toggle()
        LED_GREEN.toggle()
        LED_BLUE.toggle()
        time.sleep(0.2)
    status["requesting"] = "none"
    LED_RED.low()
    LED_GREEN.low()
    LED_BLUE.low()
    return

def wrong_food():
    """
    If the Robo Pet is given the wrong food, 
    the requested led will flash for 2 seconds and will stay on
    """
    for i in range(6):
        status["requesting"].toggle()
        time.sleep(0.2)
    status["requesting"].high()
    return

def timer(min, max):
    """
    Delays the excecution of the code by a random amount of time.
    min = shortest possible delay
    max = longest possible delay
    """
    delay = random.randint(min, max)
    print(f"timer: {delay}")
    time.sleep(delay)
    return

def main():
    """
    The main function of the pet. Based on the timer the pet will get hungry
    and demand food. 
    """
    while True:
        timer(2, 5)
        request_food()
        while check_food() == "wrong":
            wrong_food()
        correct_food()
    return

main()
