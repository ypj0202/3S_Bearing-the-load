import serial
import csv
import datetime
import math
import sys
import timeit
import time
data = []

def readData(filename, port, baud, duration, samplingRate):
    try:
        arduino = serial.Serial(port, baud, timeout = 0.001)  
    except IOError as e:
        print("[Error-DueIO] " + str(e))
        sys.exit(1)
    try:
        file = open(filename, 'w+', newline='')   
    except IOError as e:
        print("[Error-csvIO] " +str(e))
        sys.exit(1)
    try:
        runtime = time.time() + int(duration) #TEMP
        start = timeit.default_timer()
        # while len(data) < int(duration) * int(samplingRate):
        while time.time() < runtime:
            inputData = arduino.readline().decode()
            inputData = inputData.replace('\r\n', '')
            inputData = inputData.split(',')
            if(inputData):
                data.append(inputData)
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
                x[0] = temp - 273.15
                csv_writer.writerow(x)

        print("[INFO] Collected data count: " + str(len(data)) + " in " + str(round((stop - start), 4)) + " seconds")
        print("[INFO] Program terminated!") 
    except Exception as e:
        print("[Error-Data] " + str(e)) 
        sys.exit(1)    


now = datetime.datetime.now()
date_string = now.strftime("%d_%m_%Y_%H_%M_%S")
csv_file = "Sensor_output_" + date_string + '.csv'
try:
    print("[INFO] Program started\n[INFO] Port: " + sys.argv[1] + " Duration: " + sys.argv[2] + " second(s) Sampling rate: " + sys.argv[3] )
    readData(csv_file, sys.argv[1], 0,sys.argv[2], sys.argv[3])
    
except Exception as e:
    print("[Error-argv] " + str(e))
    sys.exit(1)
