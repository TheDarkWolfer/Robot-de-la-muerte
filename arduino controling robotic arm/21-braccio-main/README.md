# Content
In 'my_keyboard' , I have produced the code to command the Arduino Braccio with a keyboard. 
'libraries' and 'testbraccio9060' were produced by the Arduino Team.

# Usage of keyboard commands
One first has to select the motor by clicking and submitting numbers from 1 to 6.
Then it is possible to move the motor with a given step size by clicking and sending either the letter 'a' (decrease angle) or the letter 's' (increase). 

I recommend the use of libraries commands instead of native commands because the arm is not capable of absorbing a fast movement of a single motor in one direction.
