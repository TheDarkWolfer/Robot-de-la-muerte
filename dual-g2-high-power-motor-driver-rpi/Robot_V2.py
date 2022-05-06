from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED

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
    
# Début
print("Motors forward")
avant(300)
time.sleep(2)

avant(0)
time.sleep(2)

print("Motors backward")

arriere(300)
time.sleep(2)

arriere(0)
time.sleep(2)

print("Motors right")
droite(300)
time.sleep(2)

droite(0)
time.sleep(2)

print("Motors left")

gauche(300)
time.sleep(2)

gauche(0)
time.sleep(2)
