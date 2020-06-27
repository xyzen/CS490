import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

def blink(pin1, pin2):
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

while True:
    read_ser = str(ser.readline()).strip()
    if (read_ser[:3] == "MSG"):
        dist = int(read_ser[3:])
        if dist < 20:
            blink(11, 13)
        with open("./log.txt", "a") as file:
            year, mon, day, hour, min, sec, wday, yday, isdst \
                = time.gmtime()
            file.write(
                "{}/{}/{} {}:{}:{} ~ Distance: {}cm\n".format(
                    day, mon, year, hour, min, sec, dist
                 

   )
                )