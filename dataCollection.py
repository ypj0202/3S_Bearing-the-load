#Define how long the program will run
#Put output from Arduino into csv

import time
import serial
import csv
import datetime

#function to count the total row in the csv file
def countRow(filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    lines = len(list(reader))
    return int(lines)

#connect to arduino
#collect output from arduino
#write data into the csv file
def readData(filename, port, baud, hour, minute, second):
    arduino = serial.Serial(port, baud, timeout = 0.01)
    runTime = time.time() + hour*3600 +minute*60 +second
    try:
        file = open(filename)
    except IOError:
        file = open(filename, "a+", newline='')
        csv_writer = csv.writer(file)
    while True:
        if round(runTime - time.time()) == 0: 
            break
        data = arduino.readline()[:-2].decode()
        data = data.split(',')  # use coma to seperate the values
        #datararray = data.decode().split(',')
        #temp = float(dataarray[0])
        #acc1 = int(dataarray[1])
        #mic1 = int(dataarray[3``])
        if data:
        #if data & len(data) == 6:
            #csv_writer.writerow([temp, acc1, mic1])
            csv_writer.writerow(data)
            print(data)
            file.flush()
            file.close()


now = datetime.datetime.now()
date_string = now.strftime("%d_%m_%Y_%H_%M_%S")
csv_file = "sensor_output_" + date_string + '.csv'
readData(csv_file, 'COM3', 115200, 0, 0, 5)

#count the total row from csv file at the end
rows = countRow(csv_file)
print("Total values in file:", rows)
