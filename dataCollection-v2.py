#
#  dataCollection-v2.py
#  Description: A program to collect data from Arduino and save to csv file
#  Author: Ken Yeh 475496
#  Date: 01-12-2021
#  Revision: 2.0-Alpha 
# 
import serial
import csv
import datetime
import math
import sys
import timeit
import time
data = []

def readData(filename, port, duration, samplingRate):
    try:
        arduino = serial.Serial(port, 0, timeout = 0.001)  
    except IOError as e:
        print("[Error-DueIO] " + str(e))
        sys.exit(1)
    try:
        file = open(filename, 'w+', newline='')   
    except IOError as e:
        print("[Error-csvIO] " +str(e))
        sys.exit(1)
    try:
        runtime = time.time() + int(duration)
        inputData = []
        start = timeit.default_timer()
        while time.time() < runtime:
            inputData = arduino.read(arduino.in_waiting)
            inputData = inputData.decode('utf-8')
            inputData = inputData.splitlines()            
            if(inputData):
                # if(len(inputData) > 1):
                    for x in inputData:
                        toAppend = ""
                        for y in x:
                            toAppend += y
                        
                        data.append(toAppend.split(','))
                # else:
                #     data.append(inputData.split(','))
        stop = timeit.default_timer()
        csv_writer = csv.writer(file)
        for x in data:
            if(len(x) != 1):  
                raw = int(float(x[0]))
                R1 = 10000;
                c1 = float(1.129252142e-03) 
                c2 = float(2.341083183e-04)
                c3 = float(0.8773267909e-07)
                R2 = R1 * (1023.0 / raw - 1.0)
                logR2 = math.log(R2)
                temp = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
                x[0] = str(temp - 273.15)
                csv_writer.writerow(x)

        print("[INFO] Collected: " + str(len(data)) + " data in " + str(round((stop - start), 4)) + " second(s)")
        print("[INFO] Program terminated!") 
    except Exception as e:
        print("[Error-Data] " + str(e)) 
        sys.exit(1)    


# now = datetime.datetime.now()
# date_string = now.strftime("%d_%m_%Y_%H_%M_%S")
csv_file_string = "Sensor_output_" + datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
try:
    print("[INFO] Program started\n[INFO] Port: " + "COM6" + " Duration: " + "1" + " second(s) Sampling rate: " + "20000" )
    readData(csv_file_string, 'COM6', 1, 20000)
    # readData(csv_file, sys.argv[1],sys.argv[2], sys.argv[3])
    
except Exception as e:
    print("[Error-argv] " + str(e))
    sys.exit(1)
