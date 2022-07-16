# GPIO setup and imports omitted
import RPi.GPIO as GPIO
import time

state1 = 0
state2 = 0
state3 = 0
state4 = 0

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    global state1
    global state2
    global state3
    global state4
    
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1 and state1 == 0):
        print(characters[0])
    if(GPIO.input(C2) == 1 and state2 == 0):
        print(characters[1])
    if(GPIO.input(C3) == 1 and state3 == 0):
        print(characters[2])
    if(GPIO.input(C4) == 1 and state4 == 0):
        print(characters[3])
    
    state1 = GPIO.input(C1)
    state2 = GPIO.input(C2)
    state3 = GPIO.input(C3)
    state4 = GPIO.input(C4)
    GPIO.output(line, GPIO.LOW)
    
try:
    while True:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")