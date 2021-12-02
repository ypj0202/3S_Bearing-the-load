#
#  dataCollection-v3.py
#  Description: A program to collect data from Arduino and save to csv file
#  Author: Ken Yeh 475496
#  Date: 02-12-2021
#  Revision: 3.0
#
import serial
import csv
import datetime
import math
import sys
import timeit
import time
# Data input order: Temp, accelerometer1, accelerometer1, microphone1, microphone2, microphone3


def readData(filename, port, duration):
    try:
        arduino = serial.Serial(port, 0, timeout=0.1)
    except IOError as e:
        print("[Error-DueIO] " + str(e))
        sys.exit(1)
    try:
        file = open(filename, 'w+', newline='')
    except IOError as e:
        print("[Error-csvIO] " + str(e))
        sys.exit(1)
    try:
        runtime = time.time() + int(duration)
        inputData_raw = []
        print("[INFO] Collecting data...")
        start = timeit.default_timer()
        while time.time() < runtime:
            inputData_raw.append(list(arduino.read(2*6)))
        stop = timeit.default_timer()
        csv_writer = csv.writer(file)
        count = len(inputData_raw)
        for i in inputData_raw:
            toAppend = []
            index = 0
            while(index < len(i)):
                raw = i[index+1] << 8 | i[index]
                if index == 0:
                    R1 = 10000
                    c1 = float(1.129252142e-03)
                    c2 = float(2.341083183e-04)
                    c3 = float(0.8773267909e-07)
                    R2 = R1 * (1023.0 / float(raw) - 1.0)
                    logR2 = math.log(R2)
                    temp = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
                    toAppend.append(str(temp - 273.15))
                else:
                    toAppend.append(i[index+1] << 8 | i[index])
                index += 2
            csv_writer.writerow(toAppend)

        print("[INFO] Collected: " + str(count) + " data in " +
              str(round((stop - start), 4)) + " second(s)")
    except Exception as e:
        print("[Error-Data] " + str(e))
        sys.exit(1)


print("========== DataCollection.py v3.0 BY Ken Yeh ==========")
csv_file_string = "Sensor_output_" + \
    datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
try:
    print("[INFO] Program started\n[INFO] Port: " +
          sys.argv[1] + " Duration: " + sys.argv[2] + " second(s)")
    readData(csv_file_string, sys.argv[1], sys.argv[2])

except Exception as e:
    print("[Error-argv] Format dataCollection-v3.py [Port] [Duration]")
    sys.exit(1)
print("[INFO] Program terminated!")
