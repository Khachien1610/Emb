#!/usr/bin/env python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from time import sleep

lcd = LCD()

def safe_exit(signum, frame):
	exit(1)
	
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def scrollText(str, delay, line):
    if len(str) < 17:
        lcd.text(str,line)
    else:
        for i in range(0,len(str) - 16):
            lcd.text(str[i:i+15],line)
            sleep(delay)

scrollText('Hotel Anh Duy',0,1)
scrollText('Can anyone help me out to get the desired output as i want?', 0.1, 2)
sleep(10)
scrollText('Hello anh em hello anh em hello anh em hello anh em', 0.1, 2)
pause()
lcd.clear()
