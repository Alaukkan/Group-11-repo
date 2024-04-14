#A simple way to implement piezo functionality for sound output.

#More functional sounds will be added later.

from machine import Pin, PWM
from time import sleep_ms

#Define pin for piezo and init PWM
piezo_pin = Pin(10, Pin.OUT)
piezo_PWM = PWM(piezo_pin)

#Define notes for maximum irritation
note_c = 261
note_c_sharp = 277

def annoy_me():
    
    x = 0

    while x < 5:
        piezo_PWM.freq(note_c_sharp)
        piezo_PWM.duty_u16(25000)   # 40%ish powerlevel
        sleep_ms(500)

        piezo_PWM.freq(note_c)
        piezo_PWM.duty_u16(25000)   # 40%ish powerlevel
        sleep_ms(500)
        
        x += 1
    
    piezo_PWM.deinit()

annoy_me()