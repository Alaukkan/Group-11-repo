import random
import utime
from machine import Pin, PWM
from mfrc522 import MFRC522

button_red = Pin(18, Pin.IN, Pin.PULL_UP)
button_green = Pin(17, Pin.IN, Pin.PULL_UP)
button_blue = Pin(16, Pin.IN, Pin.PULL_UP)
button_yellow = Pin(15, Pin.IN, Pin.PULL_UP)
button_purple = Pin(14, Pin.IN, Pin.PULL_UP)

red_pin = PWM(Pin(11, Pin.OUT))
green_pin = PWM(Pin(12, Pin.OUT))
blue_pin = PWM(Pin(13, Pin.OUT))
red_pin.freq(1000)
green_pin.freq(1000)
blue_pin.freq(1000)

# order for lists: red(0), green(1), blue(2), yellow(3), purple(4)
color = ["red", "green", "blue", "yellow", "purple"]
buttons = [button_red, button_green, button_blue, button_yellow, button_purple]
rgb = [red_pin, green_pin, blue_pin]

rgb_colors = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "purple" : (200, 0, 255),
    "white" : (255, 255, 255)
}

status = {
    "requesting_color" : "none",
    "requesting_RFID" : "none"
}

def output_color(icolor):
    red = icolor[0]
    green = icolor[1]
    blue = icolor[2]
    rgb[0].duty_u16(round(65535 * red / 255))
    rgb[1].duty_u16(round(65535 * green / 255))
    rgb[2].duty_u16(round(65535 * blue / 255))
    return

def led_off():
    rgb[0].duty_u16(0)
    rgb[1].duty_u16(0)
    rgb[2].duty_u16(0)
    return

def request_food():
    """
    A random number is generated which decides what food item the Robo Pet
    wants by accessing the element in the led list. Robopet
    indicates what food it wants by a colored LED. 
    """
    item = random.randint(0, len(color) - 1)
    status["requesting_color"] = color[item]
    print(f"requesting food: {color[item]}")
    utime.sleep(0.5)
    output_color(rgb_colors[color[item]])
    return

def check_food():
    """
    Checks if the food is correct.
    If it is, returns "correct", else "wrong".
    Has a 20 second timer, if it runs out, returns "timed out"
    """
    start_time = utime.time()
    while utime.time() - start_time < 20:  # 20 seconds timer
        utime.sleep(0.01)
        for i in range(0,5):
            if buttons[i].value() == 0:
                print(f"{color[i]} was pressed in {utime.time() - start_time} seconds")
                if color[i] == status["requesting_color"]:
                    return "correct"
                else:
                    return "wrong"
    print("Timed out")
    return "timed out"

def correct_food():
    """
    If the food is correct, led flashes white for 2 seconds
    """
    for i in range(3):
        led_off()
        utime.sleep(0.2)
        output_color(rgb_colors["white"])
        utime.sleep(0.2)
    status["requesting_color"] = "none"
    status["requesting_RFID"] = "none"
    led_off()
    return

def wrong_food():
    """
    If the Robo Pet is given the wrong food, 
    the requested led will flash for 2 seconds and will stay on
    """
    for i in range(3):
        led_off()
        utime.sleep(0.2)
        output_color(rgb_colors[status["requesting_color"]])
        utime.sleep(0.2)
    return

def timed_out():
    """
    If the Robo Pet times out, the led does a long white flash
    """
    output_color(rgb_colors["white"])
    utime.sleep(2)
    led_off()
    return

def timer(min, max):
    """
    Delays the excecution of the code by a random amount of time.
    min = shortest possible delay
    max = longest possible delay
    """
    delay = random.randint(min, max)
    print(f"timer: {delay}")
    utime.sleep(delay)
    return

def main():
    """
    The main function of the pet. Based on the timer the pet will get hungry
    and demand food. 
    """
    while True:
        timer(2, 5)
        request_food()
        while True:
            result = check_food()
            if result == "wrong":
                wrong_food()
            elif result == "correct":
                correct_food()
                break
            else:
                timed_out()
                break
    return

main()