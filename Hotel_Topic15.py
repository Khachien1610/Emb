#import library
import RPi.GPIO as GPIO
#import pandas as pd
from gpiozero import Servo
from mfrc522 import SimpleMFRC522
import time
import csv
import asyncio

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
# New Import
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
from datetime import datetime 

# LCD
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
            if readKeypad():
                break
            lcd.text(str[i:i+15],line)
            sleep(delay)

# Function read id 
def readIdFromTag():
    reader = SimpleMFRC522()
    try:
        id, text = reader.read()
        return text
    finally:
        GPIO.cleanup()

# Read id from tag
scrollText('Hotel',0,1)
scrollText('Scan RFID', 0.1, 2)
print('Scan Tag...')
ID = readIdFromTag()
data = {}

#Define Keypad
# Row
ROW1 = 5
ROW2 = 6
ROW3 = 13
ROW4 = 19
# Column
COL1 = 12
COL2 = 16
COL3 = 20
COL4 = 21
#
ROW_Pin = [ROW1,ROW2,ROW3,ROW4]
#
COL_Pin = [COL1,COL2,COL3,COL4]
# 
KEY_map =  [["1" ,"2" ,"3" ,"A"],
            ["4" ,"5" ,"6" ,"B"],
            ["7" ,"8" ,"9" ,"C"],
            ["*" ,"0" ,"#" ,"D"]]

# ---------------------Init function-----------------------#
def Servo_init():
    servo = Servo(22)
def Keypad_Init():
    GPIO.setup(ROW1, GPIO.OUT)
    GPIO.setup(ROW2, GPIO.OUT)
    GPIO.setup(ROW3, GPIO.OUT)
    GPIO.setup(ROW4, GPIO.OUT)
    GPIO.setup(COL1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COL4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 
# ------------------Display function-----------------------#
def Display_Login():
    print('Enter password:')
    scrollText('Enter password', 0.5, 2)
def Display_Service():
    print("***********Service***********")
    print("1.Room Service")
    print("2.Outside Service")
    print("*.Logout")
    scrollText('Service', 0, 1)
    scrollText('1.Room Service 2.Outside Service *.Logout', 0.1, 2)
def Display_RoomService():
    print("********Room Service*********")
    print("1.Checkin")
    print("2.Checkout")
    print("3.Room Renewal")
    print("4.Incident Notify")
    print("5.Back")
    print("*.Logout")
    scrollText("Room Service",0,1)
    scrollText("1.Checkin 2.Checkout 3.Room Renewal 4.Incident Notify 5.Back *.Logout",0.1,2)
def Display_Checkin():
    print("**********Checkin************")
    scrollText('Checkin', 0, 2)
def Display_Checkout():
    print("**********Checkout************")
    scrollText('Checkout', 0, 2)
def Display_RoomRenewal():
    print("********Room Renewal*********")
    print("Choose a room renewal package")
    print("    Package            Cost ")
    print("1.    1 Day             15$  ")
    print("2.    5 Day             70$  ")
    print("3.   10 Day             130$ ")
    print("4.   15 Day             195$ ")
    print("5.Back")
    print("*.Logout")
    scrollText('Room Renewal', 0, 1)
    scrollText("1. 15$/1day 2. 70$/5day 3. 130$/10day 4. 195$/15day  5.Back *.Logout",0.1,2)
def Display_Payment(cost):
    print("The amount to be paid is",cost)
    print("Please pass your credit card through the card reader")
    scrollText('Payment', 0, 1)
    scrollText(f'Scan card to pay {cost}!',0.1,2)
def Display_Hotline(Hotline):
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("********Room Service*********")
    print("*******Incident Notify*******")
    print("Fix Electrical - Water:",Hotline[0])
    print("Staff:",Hotline[1])
    print("1.Back")
    print("*.Logout")
    scrollText('Incident Notify', 0, 1)
    scrollText(f'Fix Electrical - Water: {Hotline[0]} - Staff: {Hotline[1]}  1.Back 2.Logout',0.1,2)
def Display_Goodbyte():
    print("****Thank you for using the service. See you again!*******")
    timeLeft = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Left Time: ",timeLeft)
    scrollText('Receive Key!',1,2)
    scrollText(f'Left Time: {timeLeft}',0.2,2)
    scrollText('Thank you for using the service. See you again!', 0, 2)
def Display_OutsideService():
    print("****KIOSK SELF SERVICE*******")
    print("***********Service***********")
    print("******Outside Service********")
    print("1.Cleaning")
    print("2.Food and Drink")
    print("3.Send mail")
    print("4.Back")
    print("*.Logout")
    scrollText('Outside Service', 0, 1)
    scrollText('1.Cleaning 2.Food and Drink 3.Send mail 4.Back *.Logout', 0.1, 2)

# --------------------FSM function--------------------------#

#***********Login FSM*************#

def Get_password():
    Key_Login = ""
    Key_count = 0
    while(Key_count < 6 ):
        if(readKeypad()!=None):
            Key_Login += readKeypad()
            print(readKeypad(), end="")
            Key_count = Key_count + 1
            time.sleep(0.2)
            if(Key_count == 6):
                return Key_Login

def check_Login(Login_key):
    global data
    res = requests.post("https://embedded-hust.herokuapp.com/api/infos/auth", json = {"id": ID.strip(), "keyword": Login_key})
    if(res.status_code == 200):
        data = res.json()['data']
        print("\nIdentify successfully")
        scrollText('Identify successfully', 0, 2)
        return True
    else:
        print(" ")
        print("Invalid password. Please re-enter your password!")
        scrollText('Invalid password', 1, 2)
        time.sleep(1)
        return False


def Identification():
    global data
    print("")
    print("--------------------------------------------------------------")
    print("ID : ",data['id'])
    print("Welcome",data['user'])
    userName = data['user']
    timeStart = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Start Time: ",timeStart)
    scrollText(f'Welcome {userName}! Start Time: {timeStart}',0.2,2)
    time.sleep(1)

#**********Service FSM************#

def Service_Idle():
    Display_Service()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"

# Room Service Function
def ServiceRoom_Idle():
    Display_RoomService()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()=="5"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "5"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"

def Checkin():
    Display_Checkin()
    print("Waiting......")
    servo = Servo(22)
    servo.max()
    time.sleep(0.5)
    print("Provide Key Done!")
    scrollText('Provide Key Done!',0.2,2)
    time.sleep(2)

def Checkout():
    Display_Checkout()
    time.sleep(2)
    print("Waiting......")
    servo = Servo(22)
    servo.min()
    time.sleep(0.5)
    print("Receive Key!")
    Display_Goodbyte()
    time.sleep(2)
    
def RoomRenewal():
    Display_RoomRenewal()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()=="5"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "5"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"
            
def Payment(cost):
    Display_Payment(cost)
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    if(int(text)>=cost):
        return True
    else:
        return False
    
def Update_InformationRenewal(Package_Renewal,Payment_Valid):
    if(Payment_Valid):
        print("Completed payment!")
        scrollText('Completed payment!',0.1,2)
        time.sleep(1)
        print("")
    else:
        print("The payment failed because the card ran out of money. Please try again!")
        scrollText('The payment failed because the card ran out of money. Please try again!',0.1,2)
        time.sleep(1)
        print("")

# CSV
def IncidentNotify():
    with open("HotlineNumber.csv", "r") as f:
        file = csv.DictReader(f)
        Hotline = []
        for col in file:
            Hotline.append(col['Hotline'])
    Display_Hotline(Hotline)
            
# Outside Service Function
def ServiceOutside_Idle():
    Display_OutsideService()
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()=="2"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "2"
        elif(readKeypad()=="3"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "3"
        elif(readKeypad()=="4"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "4"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"


def Laundry_Cleaing():
    print("You have successfully booked the cleaning service!")
    print("1.Back")
    print("2.Logout")
    scrollText("You have successfully booked the cleaning service! 1.Back 2.Logout",0.2,2)
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"
def Food_Drink():
    print("You have successfully ordered food!")
    print("1.Back")
    print("2.Logout")
    scrollText("You have successfully ordered food! 1.Back 2.Logout",0.2,2)
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"
def Parcals_Mail():
    print("Call receptionist!")
    print("1.Back")
    print("2.Logout")
    scrollText("Call receptionist! 1.Back 2.Logout",0.2,2)
    Key_count = 0
    while(Key_count < 1):
        if(readKeypad()=="1"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "1"
        elif(readKeypad()== "*"):
            Key_count = Key_count + 1
            time.sleep(0.2)
            return "*"



# --------------------function--------------------------#
#             

def readKeypad():
    for i in range(len(ROW_Pin)):
        GPIO.output(ROW_Pin[i], GPIO.HIGH)
        for j in range(len(COL_Pin)):
            if(GPIO.input(COL_Pin[j]) == 1):
                GPIO.output(ROW_Pin[i], GPIO.LOW)
                return KEY_map[i][j]
        GPIO.output(ROW_Pin[i], GPIO.LOW)
        
#---------------------------------------------------------

FSM_State = 'Login'
#
Login_State = 'EnterPIN'
#
Service_State = 'Idle'

RoomService_State = 'Idle'

OutsideService_State = 'Idle'




#---------------------------------------------------------
if __name__ == '__main__':
    Servo_init()
    Keypad_Init()
    init = False
    while True:
        if(FSM_State == 'Login'):
            Key_Login = ""
            if(Login_State ==  'EnterPIN'):
                Display_Login()
                Key_Login = Get_password()
                Login_State = 'CheckPIN'
            if(Login_State ==  'CheckPIN'):
                Valid_key = check_Login(Key_Login)
                if(Valid_key == True):
                    Login_State =  'Identification'
                elif(Valid_key == False):
                    Login_State =  'EnterPIN'
            if(Login_State ==  'Identification'):
                Identification()
                FSM_State = "Service"
                Login_State =  'EnterPIN'
        if(FSM_State == 'Service'):
            if(Service_State == 'Idle'):
                Selection_Service = Service_Idle()
                if(Selection_Service == "1"):
                    Service_State = 'RoomService'
                if(Selection_Service == "2"):
                    Service_State = 'OutsideService'
                if(Selection_Service == "*"):
                    time.sleep(1)
                    FSM_State = 'Login'
            if(Service_State == 'RoomService'):
                if(RoomService_State == 'Idle'):
                    Selection_ServiceRoom = ServiceRoom_Idle()
                    if(Selection_ServiceRoom =="1"):
                        RoomService_State = 'Checkin'
                    elif(Selection_ServiceRoom =="2"):
                        RoomService_State = 'Checkout'
                    elif(Selection_ServiceRoom =="3"):
                        RoomService_State = 'RoomRenewal'
                    elif(Selection_ServiceRoom =="4"):
                        RoomService_State = 'IncidentNotify'
                    elif(Selection_ServiceRoom =="5"):
                        Service_State = 'Idle'
                    elif(Selection_ServiceRoom == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                if(RoomService_State == 'Checkin'):
                    Checkin()
                    RoomService_State = 'Idle'
                if(RoomService_State == 'Checkout'):
                    Checkout()
                    RoomService_State = 'Idle'
                    Service_State = 'Idle'
                    FSM_State = 'Login'
                if(RoomService_State == 'RoomRenewal'):
                    cost = 0
                    Selection_RoomRenewal = RoomRenewal()
                    if(Selection_RoomRenewal=="1"):
                        cost = 15
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="2"):
                        cost = 70
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="3"):
                        cost = 130
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="4"):
                        cost = 195
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_RoomRenewal,Payment_Valid)
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="5"):
                        RoomService_State = 'Idle'
                    elif(Selection_RoomRenewal=="*"):
                        RoomService_State = 'Idle'
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                if(RoomService_State == 'IncidentNotify'):
                    IncidentNotify()
                    Key_count = 0
                    while(Key_count < 1):
                        if(readKeypad()=="1"):
                            Key_count = Key_count + 1
                            time.sleep(0.2)
                            RoomService_State = 'Idle'
                        elif(readKeypad()=="*"):
                            Key_count = Key_count + 1
                            time.sleep(0.2)
                            RoomService_State = 'Idle'
                            Service_State = 'Idle'
                            FSM_State = 'Login'
            if(Service_State == 'OutsideService'):
                if init:
                        OutsideService_State = 'Idle'
                if(OutsideService_State == 'Idle'):
                    Selection_ServiceOutside = ServiceOutside_Idle()
                    if(Selection_ServiceOutside =="1"):
                        cost = 15
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_ServiceOutside,Payment_Valid)
                        OutsideService_State = 'Idle'
                    elif(Selection_ServiceOutside =="2"):
                        cost = 15
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_ServiceOutside,Payment_Valid)
                        OutsideService_State = 'Idle'
                    elif(Selection_ServiceOutside =="3"):
                        cost = 15
                        Payment_Valid = Payment(cost)
                        Update_InformationRenewal(Selection_ServiceOutside,Payment_Valid)
                        OutsideService_State = 'Idle'
                    elif(Selection_ServiceOutside =="4"):
                        Service_State = 'Idle'
                    elif(Selection_ServiceOutside == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                    
                if(OutsideService_State == 'Laundry_Cleaing'):
                    choiceClean = Laundry_Cleaing()
                    if(choiceClean == "1"):
                        Service_State = 'Idle'
                    elif(choiceClean == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                    else:
                        pass
                if(OutsideService_State == 'Food_Drink'):
                    choiceFood = Food_Drink()
                    if(choiceFood == "1"):
                        Service_State = 'Idle'
                    elif(choiceFood == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                    else:
                        pass
                if(OutsideService_State == 'Parcals_Mail'):
                    choiceMail = Parcals_Mail()
                    if(choiceMail == "1"):
                        Service_State = 'Idle'
                    elif(choiceMail == "*"):
                        Service_State = 'Idle'
                        FSM_State = 'Login'
                    else:
                        pass
        init = True
            