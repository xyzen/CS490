#Libraries
import sys
import time
import serial
import urllib.request as urllib2,json
import RPi.GPIO as GPIO
from Adafruit_IO import RequestError, Client, Feed, Data

#initialize adafruit IO with client function
aio = Client('Levizzzle','aio_rteY67YQ8itPEiyn4tNNMA02ejtU')

#Thingspeak API data
READ_API_KEY='YP2XMIJDWOTSTWW4'
CHANNEL_ID=1090663

#Adafruit IO Dashboard data
ADAFRUIT_IO_USERNAME = "Levizzzle"
ADAFRUIT_IO_KEY = "aio_rteY67YQ8itPEiyn4tNNMA02ejtU"

#Assignment Variables
ser = serial.Serial("/dev/ttyACM1",9600) #Connect to serial
ser.baudrate = 9600 #Set baudrate

#Data/Alarms arrays
data = []
alarms = []
leds = [17,18,19,20,21,22]

#Raspberry Pi GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for x in leds()
    GPIO.setup(x,GPIO.OUT)

#Send data function, sends to Adafruit IO Dashboard
def send_data(data):
    feeds = aio.feeds() #Sets feeds from AIO
    
    for x in range(len(data)):
        aio.send_data(feeds[x].key, data[x]) #Send data to AIO
    
def pull_data():
    read_ser = ser.readline() #Read line
    package = read_ser.decode('ASCII') #Decode ASCII characters
    data = package.split('|') #Split package on '|'
    return data #Return the data array
    
def check_alarms(data):
    alarms = []
    sensThres = {'Temperature':27, 'Humidity':41.9, 'Pressure':978.5,
                 'Light':400, 'Dust':3805, 'Carbon Dioxide':4.1,
                 'Carbon Monoxide':8.1, 'Distance':22}
    x = 0
    for sens in(sensThres):
        if data[x] > sensThres[sens]
            alarms.append(x)
        x += 1
    return alarms

def set_alarming(alarms,leds):
    for loops in range(5)
        for x in alarms:
            GPIO.output(leds[x],GPIO.HIGH)
        time.sleep(1)
        for x in alarms:
            GPIO.output(leds[x],GPIO.LOW)             
        
def main():
    data = pull_data() #Calls pull_data function
    alarms = check_alarms(data) #Calls the check_alarms function
    if len(alarms) > 0:
        set_alarming(alarms)
    send_data(data) #Calls send data function
    
        
if __name__ == '__main__': #To initiate main function
    main()