from pyduino_mk.constants import *
from pyduino_mk import Arduino
print(1231/1)
arduino = Arduino(port = 'COM3')

while True:
    print("asdw")
    for i in range(1111):
        arduino.move(55,0)
    for i in range(1111):
        arduino.move(-55,0)
