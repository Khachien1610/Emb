from gpiozero import Servo
import time

def Servo_init():
    servo = Servo(22)
    servo.min()
    return servo

def Servo_on(servo):
    servo.min()
    time.sleep(0.5)
    servo.max()

def Servo_off(servo):
    servo.max()
    time.sleep(0.5)
    servo.min()

if __name__ == '__main__':
    servo = Servo_init()
    Servo_on(servo)
    Servo_off(servo)