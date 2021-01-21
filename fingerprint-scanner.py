import time
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as gpio

#LCD Setup
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)



#Button Setup
enroll=16
delete=12
increase=1
decrease=7
release=8
magnet=25

buttonPress = True
enrollButton = True
deleteButton = True
increaseButton = True
decreaseButton = True

#GPIO Setup
gpio.setmode(gpio.BCM)
gpio.setup(enroll, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(delete, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(increase, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(decrease, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(release, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(magnet, gpio.OUT)


#Scan Finger
try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0X00000000)

        if (f.verifyPassword()==False):
                raise ValueError('The given fingerprint sensor password is wrong!')


except Exception as e:
        print('Exception message: ' + str(e))
        exit(1)

def searchFinger():
        try:
                gpio.output(magnet, gpio.HIGH)
                lcd.message('Please scan\n')
                lcd.message('for access...')
                sleep(0.001)
                while (f.readImage() == False):
                        #pass
                        return
                f.convertImage(0x01)
                result=f.searchTemplate()
                positionNumber=result[0]
                accuracyScore=result[1]
                if positionNumber == -1:
                        lcd.clear()
                        lcd.message('ACCESS DENIED!')
                        sleep(2)
                        return
                else:
                        lcd.clear()
                        lcd.message('ACCESS GRANTED!')
                        gpio.output(magnet, gpio.LOW)
                        sleep(5)
                        return
                finally:
                        return

def enrollFinger():
    lcd.clear()
    lcd.message("Place Finger\n to Enroll")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        lcd.clear()
        lcd.message("Finger Already\n")
        lcd.message("Exists")
        time.sleep(2)
        return
    print('Remove finger...')
    lcd.clear()
    lcd.message("Remove Finger")
    time.sleep(2)
    print('Waiting for same finger again...')
    lcd.clear()
    lcd.message("Place Finger\n")
    lcd.message("   Again    ")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x02)
    if ( f.compareCharacteristics() == 0 ):
        print ("Fingers do not match")
        lcd.clear()
        lcd.message("Finger Did Not\n")
        lcd.message("   Match   ")
        time.sleep(2)
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    lcd.clear()
    lcd.message("Stored at Pos: ")
    lcd.message(str(positionNumber) + "\n")
    lcd.message("successfully")
    print('New template position #' + str(positionNumber))
    time.sleep(2)

while 1:
        buttonPress=gpio.input(release)
        enrollButton=gpio.input(enroll)
        if enrollButton==False:
                enrollFinger()
        elif buttonPress==False:
                gpio.output(magnet, gpio.LOW)
                sleep(5)
        else:
                searchFinger()
                sleep(0.001)
