#Libraries
import sys
import serial

# Establish serial connection with Arduino
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600 #Set baudrate

def get_data():
    read_ser = ser.readline()
    package = read_ser.decode('ASCII').strip()
    if package[:3] == 'MSG':
	# split flagged messages into data entries
        data = package[3:].split("|")
        data = [float(entry) for entry in data]
        print(data)

        # write sensor data to comma-separated-value file
        with open("sensor_data.csv", "w") as file:
            for entry in data[:-1]:
                file.write(str(entry))
                file.write(",")
            file.write(str(data[-1]))
    else:
        print(package)

if __name__ == "__main__":
    while True:
        get_data()
