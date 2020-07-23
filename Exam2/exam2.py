#Libraries
import sys
import time
import serial
import RPi.GPIO as GPIO

#Libararies for twitter
from twython import Twython
from time import sleep

#Twitter Variables
apiKey = "sQQEszZ8Gwy8SVnZeeuLMF40C"
apiSecret = "GWdTgpS7p9t6P7ZCC3QdRFTMBl75NyTVQwodz20sOIV85n7ooo"
accessToken = "1271178365219766272-R5eAnVIeIRDFdlYpp7namiweyFk3Zp"
accessTokenSecret = "1XxHeiD9vL851hbbuuXoJHMuCTvPEqymbdtYCopQ1UxdG"

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)


#file name variable
file = open("Sensordata.txt","w+")


#Assignment Variables
ser = serial.Serial("/dev/ttyACM0",9600) #Connect to serial
ser.baudrate = 115200 #Set baudrate



def get_data(){
    repeat = True

    while repeat:
        read_ser = ser.readline()
        package = read_ser.decode('ASCII')
        print(package[:-1])
        if package[:3] == 'MSG':
            #tests for if data got from serial is valid if so breaks loop.
            repeat = False
            data = package[3:].split("|")
            data = [float(reading) for reading in data]
            print(data)

            #sends sensor data to twitter
            api.update_status(status="Sensor Data:".format(package))
            #sends sensor data to file
            file.write(package)

}


#starts data processing
get_data()
file.close()
