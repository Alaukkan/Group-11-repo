import random
import sound
import utime
import _thread
from machine import Pin, PWM
from mfrc522 import MFRC522
from servo import Servo

servo_hatch = Servo(19)
servo_right_wing = Servo(20)
servo_left_wing = Servo(21)
servo_rotator = Servo(22)

red_pin = PWM(Pin(11, Pin.OUT))
green_pin = PWM(Pin(12, Pin.OUT))
blue_pin = PWM(Pin(13, Pin.OUT))
red_pin.freq(1000)
green_pin.freq(1000)
blue_pin.freq(1000)

rgb = [red_pin, green_pin, blue_pin]
rgb_colors = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 170, 0),
    "purple" : (200, 0, 255),
    "white" : (255, 255, 255)
}
                # pin numbers for RFID reader
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
tag_to_color = {
    "0X8020B7B21B4404" : "red",
    "0X8020B7B21B6304" : "green",
    "0X8020B7B21B5504" : "blue",
    "0X8020B7B21B4304" : "yellow",
    "0X8020B7B21A8704" : "purple"
}

status = {
    "available" : ["red", "green", "blue", "yellow", "purple"],
    "requesting_color" : "none",
    "failed" : 0,
    "timed out" : 0
}

def output_color(color):
    """
    takes the rgb values from given parameter tuple and
    outputs the color to the RGB led
    """
    red = color[0]
    green = color[1]
    blue = color[2]
    rgb[0].duty_u16(round(65535 * red / 255))
    rgb[1].duty_u16(round(65535 * green / 255))
    rgb[2].duty_u16(round(65535 * blue / 255))

def led_off():
    """Turns off the RGB led"""
    rgb[0].duty_u16(0)
    rgb[1].duty_u16(0)
    rgb[2].duty_u16(0)

def deinit_servos():
    """ 
    Deinitialises servos to prevent jittering when idle
    """
    utime.sleep_ms(500)
    servo_hatch.__motor.deinit()
    servo_left_wing.__motor.deinit()
    servo_right_wing.__motor.deinit()
    servo_rotator.__motor.deinit()

def request_food():
    """
    A random number is generated which decides what food item the Robo Pet
    wants by accessing the element in the led list. Robopet
    indicates what food it wants by a colored LED. 
    """
    random.seed(utime.time() - utime.time_ns())
    length = len(status["available"])
    if length > 1:
        item = random.randint(0, length - 1)
    else:
        item = 0
    status["requesting_color"] = status["available"][item]
    print(f"requesting food: {status["available"][item]}")
    output_color(rgb_colors[status["available"][item]])
    _thread.start_new_thread(sound.play_melody, ("requesting", 1))

def read_tag():
    """
    Found library for rfid reader on github:
    https://github.com/danjperron/micropython-mfrc522
    Reads the RFID tag and returns which tag was read.
    """
    start_time = utime.time()
    reader.init()
    while utime.time() - start_time < 20:

        (stat, tag_type) = reader.request(reader.REQIDL)
        print('request stat:',stat,' tag_type:',tag_type)

        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                tag_id = hex(int.from_bytes(bytes(uid),"little",False)).upper()
                print(f"{tag_to_color[tag_id]} tag detected")

                if tag_to_color[tag_id] == status["requesting_color"]:
                    return "correct"
                return "wrong"
            else:
                pass
        utime.sleep_ms(50)
    
    return "Timed out"

def correct_food():
    """
    If the food is correct, led flashes white for 2 seconds
    both wings lift up
    hatch opens and closes
    """
    _thread.start_new_thread(sound.play_melody, ("happy", 1))
    servo_hatch.move(-30)
    servo_right_wing.move(-70)
    servo_left_wing.move(70)
    deinit_servos()
    for i in range(3):
        led_off()
        utime.sleep_ms(300)
        output_color(rgb_colors["white"])
        utime.sleep_ms(300)
    led_off()
    servo_hatch.move(0)
    servo_right_wing.move(0)
    servo_left_wing.move(0)
    deinit_servos()
    status["available"].remove(status["requesting_color"])
    status["requesting_color"] = "none"
    status["timed out"] = 0

def wrong_food():
    """
    If the Robo Pet is given the wrong food, 
    the requested led will flash for 2 seconds and will stay on
    robopet rotates left and right
    wings move simultaniously opposite directions
    hatch opens "spitting" the food out and closes
    """
    _thread.start_new_thread(sound.play_melody, ("angry", 1))
    servo_hatch.move(30)
    deinit_servos()
    for i in range(3):
        led_off()
        for i in range(30):
            servo_right_wing.move(-1.5 * i)
            servo_left_wing.move(-1.5 * i)
            servo_rotator.move(i)
            utime.sleep_ms(10)
        output_color(rgb_colors[status["requesting_color"]])
        for i in range(60):
            servo_right_wing.move(-1.5 * (30 - i))
            servo_left_wing.move(-1.5 * (30 - i))
            servo_rotator.move(30 - i)
            utime.sleep_ms(10)
        for i in range(30):
            servo_right_wing.move(1.5 * (30 - i))
            servo_left_wing.move(1.5 * (30 - i))
            servo_rotator.move(i - 30)
            utime.sleep_ms(10)
    servo_right_wing.move(0)
    servo_left_wing.move(0)
    servo_hatch.move(0)
    servo_rotator.move(0)
    deinit_servos()
    status["failed"] += 1
    status["timed out"] = 0

def timed_out():
    """
    If the Robo Pet times out, the led does a long white flash
    hatch opens and closes (spits food out)
    """
    _thread.start_new_thread(sound.play_melody, ("timed out", 1))
    servo_hatch.move(30)
    deinit_servos()
    output_color(rgb_colors["white"])
    utime.sleep(2)
    led_off()
    utime.sleep(1)
    servo_hatch.move(0)
    deinit_servos()
    status["requesting_color"] = "none"
    status["timed out"] += 1

def ending():
    if len(status["available"]) == 0:
        _thread.start_new_thread(sound.play_melody, ("victory", 1))
        for i in range(0, 255, 5):
            output_color((i, 0, 0))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((255, i, 0))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((255-i, 255, 0))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((0, 255, i))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((0, 255-i, 255))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((i, 0, 255))
            utime.sleep_ms(9)
        for i in range(0, 255, 5):
            output_color((255, 0, 255-i))
            utime.sleep_ms(9)
    elif status["failed"] > 2:
        _thread.start_new_thread(sound.play_melody, ("defeat", 1))
        output_color(rgb_colors["red"])
        utime.sleep(1)
    elif status["timed out"] > 1:
        _thread.start_new_thread(sound.play_melody, ("power down", 1))
        for i in range(0, 255, 5):
            output_color((255, 255-i, 255-i))
            utime.sleep_ms(20)
    led_off()

def timer(min, max):
    """
    Delays the excecution of the code by a random amount of time.
    min = shortest possible delay
    max = longest possible delay
    """
    delay = random.randint(min, max)
    print(f"timer: {delay}")
    utime.sleep(delay)

def check_state():
    """
    Checks the game state. Returns false if:
    - all rfid tags have been read
    - 3 wrong rfid tags have been read
    - timed out 2 times in a row
    """
    return len(status["available"]) > 0 and status["failed"] < 3 and status["timed out"] < 2

def main():
    """
    The main function of the pet. Based on the timer the pet will get hungry
    and demand food. 
    """
    deinit_servos()
    while check_state():
        timer(2, 5)
        request_food()
        while check_state():
            result = read_tag()
            if result == "wrong":
                wrong_food()
            elif result == "correct":
                correct_food()
                break
            else:
                timed_out()
                break
    ending()

main()
