#Libraries
import sys
import serial

#Libararies for twitter
#from twython import Twython

#Twitter Variables
#apiKey = "sQQEszZ8Gwy8SVnZeeuLMF40C"
#apiSecret = "GWdTgpS7p9t6P7ZCC3QdRFTMBl75NyTVQwodz20sOIV85n7ooo"
#accessToken = "1271178365219766272-R5eAnVIeIRDFdlYpp7namiweyFk3Zp"
#accessTokenSecret = "1XxHeiD9vL851hbbuuXoJHMuCTvPEqymbdtYCopQ1UxdG"

#api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

#Assignment Variables
ser = serial.Serial("/dev/ttyACM0", 9600) #Connect to serial
ser.baudrate = 9600 #Set baudrate

def get_data():
    read_ser = ser.readline()
    package = read_ser.decode('ASCII')
    if package[:3] == 'MSG':
        #tests for if data got from serial is valid if so breaks loop.   
        data = package[3:].split("|")
        data = [float(reading) for reading in data]
        print(data)

        #sends sensor data to twitter
        #api.update_status(status="Sensor Data:".format(package))

        #sends sensor data to file
        with open("sensor_data.csv", "w") as file:
            for entry in data:
                file.write(str(entry))
                file.write(",")
    else:
        print(package[:-1])

while True:
    get_data()
