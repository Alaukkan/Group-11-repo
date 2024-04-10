## Concept

konsepti copipasta


## Parts

* Raspberry Pi Pico W
* MFRC-522 RF-ID-Reader
* RF-ID-Tags (13.56 MHz)
* 3 Servomotors (180 degree motion)
* 1 or 2 DC-Motors
* LEDs (RGB and/or coloured)
* Power Source (3.3 V for Pico, more for DC-motors (>5 V))
* H-Bridge (L293DNE, L293D, etc.)
* Breadboard
* Jumper Cables
* Resistors, capacitors
* 

## Tools and Software

* 3D-Printer
* CAD Software (Fusion 360, FreeCAD, etc.)
* Slicer Software (Cura, Slic3r, Simplify 3D, etc.)
* Laser cutter
* IDE (VS Code, Arduino IDE, Thonny, etc.)

## Functionality

```Python
def read_RFID_UID():
pass

def rgb_colour_8(colour):
pass

def servo_control(pin, angle):
pass

def motor_control(pin, direction, speed):
pass

```


## Source Code

Project is written and tested in [MicroPython](https://docs.micropython.org/en/latest/rp2/quickref.html) for RP2040 based
[Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w-and-pico-wh),
functionality with other micro controllers is not tested.

Source Code can be found in the [GitHub repository](https://github.com/Alaukkan/Group-11-repo).

