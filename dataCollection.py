#Define how long the program will run
#Put output from Arduino into csv

from _typeshed import WriteableBuffer
import serial
import csv
import time
import schedule

# TODO Make sure you test with you own Arduino(Uno or DUE) by generating some random output test if you program can work efficiently

def func():
    arduino_port = "COM3" #TODO Should be taken as an argument
    baud = 115200 #TODO Should be taken as an argument
    fileName = "data.csv" #TODO File name should be named by the time it generats otherwise it may overwrite the original file(e.g sensor_output_2021_11_26_15_48_00.csv)
                          #TODO You should also check if the file already exist

    ser = serial.Serial(arduino_port, baud)
    ser.flushInput()

    while True:
        ser_data = ser.readline().decode().strip().split(',')
    
        #convert to int
        new_ser_data = [int(i) for i in ser_data] # TODO: Temperature data is in float format 
    
        with open(fileName, "a", newline='') as f:
            write = csv.writer(f, delimiter = ",")
            write.writerow([new_ser_data[0], new_ser_data[1], new_ser_data[2]]) 
            # TODO: 1)There are 6 sensors in total
            #       2)Be aware that there might be some dummy data or wrong data, make sure you filter it out
            f.close()
    #TODO Count the amount of data collected(How many rows) to check if it matches the sampling frequency 

schedule.every(10).second.do(func) #TODO If I understand correctly, your program runs every 10 seconds. 
                                   #The requirement is that the program will run for a custom time(e.g 10 seconds)
                                   #Which it should also be taken as an argument

while True:
    schedule.run_pending()

