from pyduino_mk.constants import *
from pyduino_mk import Arduino
print(1231/1)
arduino = Arduino(port = 'COM3')

while True:
    for i in range(1111):
        arduino.move(1,0)
    for i in range(1111):
        arduino.move(-1,0)
