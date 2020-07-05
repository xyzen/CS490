#Libraries
import sys
import time
import serial
import RPi.GPIO as GPIO
from Adafruit_IO import RequestError, Client, Feed, Data

#Adafruit IO Dashboard data
ADAFRUIT_IO_USERNAME = "xyzen"
ADAFRUIT_IO_KEY = "aio_amUu18Y4TPMvDoUyD5Syu6VN09B3"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

GPIO.setmode(GPIO.BOARD)
outputs = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24]
pairs = [(3, 7), (5, 8), (10, 12), (11, 13), (15, 18), (16, 19), (21, 23), (22, 24)]
[GPIO.setup(pin, GPIO.OUT) for pin in outputs]
[GPIO.output(pin, GPIO.LOW) for pin in outputs]

#Assignment Variables
ser = serial.Serial("/dev/ttyACM0",9600) #Connect to serial
ser.baudrate = 115200 #Set baudrate

def check_alarms(data):
    sensThres = [28, 43, 981, 500, 3805, 10, 15, 22]
    for i in range(8):
        if data[i] > sensThres[i]:
            GPIO.output(pairs[i][0], GPIO.HIGH)
            GPIO.output(pairs[i][1], GPIO.LOW)
        else:
            GPIO.output(pairs[i][0], GPIO.LOW)
            GPIO.output(pairs[i][1], GPIO.HIGH)

#Send data function, sends to Adafruit IO Dashboard
def send_data(data):
    feeds = aio.feeds() #Sets feeds from AIO
    for x in range(len(data)):
        aio.send_data(feeds[x].key, data[x]) #Send data to AIO

wait = 15
timer = time.time()-15
while True:
    read_ser = ser.readline()
    package = read_ser.decode('ASCII')
    print(package[:-1])
    if package[:3] == "MSG":
        data = package[3:].split("|")
        data = [float(reading) for reading in data]
        print(data)
        check_alarms(data)
        try:
            elapsed = time.time() - timer
            if elapsed > wait:
                send_data(data)
                timer = time.time()
                wait = 15
                print("Success!\n")
            else:
                print("Waiting for AIO Dashboard", wait - elapsed, "\n")
        except:
            timer = time.time()
            wait = 60
            print("Failed to update AIO Dashboard\n")

