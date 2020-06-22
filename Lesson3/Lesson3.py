import serial
import RPi.GPIO as GPIO
import time
import urllib2

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

while True:
    read_ser = str(ser.readline()).strip()
    print(read_ser)
    if (read_ser[:3] == "MSG"):
        blink(11)
        url = "http://api.thingspeak.com/update?api_key=V19MI61PTBSDDYJF"
        url += read_ser[3:]
        link = urllib2.urlopen(url)
        link.read()
        link.close()