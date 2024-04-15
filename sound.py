# A simple way to implement sound output using piezo(buzzer).

# More functional sounds have been added.

from machine import Pin, PWM
from time import sleep_ms

#Define pin for piezo and init PWM.
piezo_pin = Pin(10, Pin.OUT)
piezo_PWM = PWM(piezo_pin)

# Notes are defined, either globally, or locally in function if memory needs to be saved.
# c = c and c_s = c sharp and so on. Frequencies are rounded to nearest int.
c = 262 * 2
c_s = 277 * 2
d = 294 * 2
d_s = 311 * 2
e = 330 * 2
f = 349 * 2
f_s = 370 * 2
g = 392 * 2
g_s = 415 * 2
a = 440 * 2
a_s = 466 * 2
b = 494 * 2
a_1 = 440

# Lists containing melodies are constructed using frequency, duration pairs.
# First comes the frequency and then the duration.
melody_AF = [d, 450, f, 300, d, 150, d, 150, g, 300, d, 200, c, 350,
          d, 450, a, 450, d, 150, d, 150, a_s, 250, a, 250, f, 250,
          d, 250, a, 300, d * 2, 350, d, 300, c, 200, c, 150,
          a_1, 350, e, 275, d, 1000]


def play_melody(melody):

    for notes in range(0, len(melody), 2):
        
        # The loop variable notes points to the frequency,
        # and notes + 1 points to the duration of the note.
        piezo_PWM.freq(melody[notes])
        piezo_PWM.duty_u16(25000)   # 40%ish powerlevel
        sleep_ms(melody[notes + 1])

        # Pause for 20ms
        piezo_PWM.duty_u16(0)
        sleep_ms(20)
    
    piezo_PWM.deinit()


def annoy_me():
    
    x = 0

    while x < 5:
        piezo_PWM.freq(c_s)
        piezo_PWM.duty_u16(25000)   # 40%ish powerlevel
        sleep_ms(500)

        piezo_PWM.freq(c)
        piezo_PWM.duty_u16(25000)   # 40%ish powerlevel
        sleep_ms(500)
        
        x += 1
    
    piezo_PWM.deinit()

play_melody(melody_AF)
