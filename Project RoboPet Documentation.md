## Concept

Our product will be a (desktop) RoboPet (™, Ⓒ, Patent Pending), that is capable of simulating the most basic,
simple functions of a pet, namely the need for food and drink.
Product will be stationary and mounted on a rotating base, it will be able to turn left or right and move its arms
(other modes of movement might be implemented if there is time and/or resources).
Communication with the user will happen using coloured LEDs located in the torso and a buzzer located in the head.
For user interaction there will be an conveniently located on/off switch and a RFID-reader located in the mouth/head region.
RFID-reader is used to scan and recognize the different foodstuffs inserted.
A system for ingesting desired foodstuffs and discarding undesired ones will be implemented if there is time.

## Parts

* Raspberry Pi Pico W
* MFRC-522 RF-ID-Reader
* 5 RF-ID-Tags (13.56 MHz)
* 4 Servomotors (180 degree motion)
* 1 RGB LED
* Power Source (4.5V battery pack holding 3 AA batteries)
* 2 Breadboards
* Jumper Cables
* Resistors, capacitors
* 3D-Printed parts

## Tools and Software

* 3D-Printer (We used different versions of Ender-3)
* CAD Software (Fusion 360, FreeCAD, Blender with CAD Sketcher, etc.)
* Slicer Software (Cura, Slic3r, Simplify 3D, etc.)
* IDE (VS Code, Arduino IDE, Thonny, etc.)

## Functionality highlights

```Python
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


def correct_food():
    """
    If the food is correct, led flashes white for 2 seconds
    both wings lift up
    hatch opens and closes
    """
    _thread.start_new_thread(sound.play_melody, ("happy", 1))
    servo_hatch.move(-60)
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

```


## Source Code

Project is written and tested in [MicroPython](https://docs.micropython.org/en/latest/rp2/quickref.html) for RP2040 based
[Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w-and-pico-wh),
functionality with other micro controllers is not tested.

Source Code can be found in the [GitHub repository](https://github.com/Alaukkan/Group-11-repo).

