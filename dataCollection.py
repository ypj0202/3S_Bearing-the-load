#Define how long the program will run
#Put output from Arduino into csv

from _typeshed import WriteableBuffer
import serial
import csv
import time
import schedule

def func():
    arduino_port = "COM3"
    baud = 115200
    fileName = "data.csv"

    ser = serial.Serial(arduino_port, baud)
    ser.flushInput()

    while True:
        ser_data = ser.readline().decode().strip().split(',')
    
        #convert to int
        new_ser_data = [int(i) for i in ser_data]
    
        with open(fileName, "a", newline='') as f:
            write = csv.writer(f, delimiter = ",")
            write.writerow([new_ser_data[0], new_ser_data[1], new_ser_data[2]])
            f.close()

schedule.every(10).second.do(func)

while True:
    schedule.run_pending()

