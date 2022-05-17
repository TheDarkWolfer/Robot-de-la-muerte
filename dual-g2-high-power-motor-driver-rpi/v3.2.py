from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import keyboard

# Define a custom exception to raise if a fault is detected.
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  


def avant(s):
    motors.motor1.setSpeed(-s)
    motors.motor2.setSpeed(-s)

def arriere(s):
    motors.motor1.setSpeed(s)
    motors.motor2.setSpeed(s)

def droite(s):
    motors.motor1.setSpeed(-s)
    motors.motor2.setSpeed(s)

def gauche(s):
    motors.motor1.setSpeed(s)
    motors.motor2.setSpeed(-s)

def arret()
    motors.motor1.setSpeed(0)
    motors.motor2.setSpeed(0)


while True:
    if keyboard.press("z"):
        avant(300)
    if keyboard.press("s"):
        arriere(300)
    if keyboard.press("q"):
        gauche(300)
    if keyboard.press("d"):
        droite(300)
    else:
        arret()
