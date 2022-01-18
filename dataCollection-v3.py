#
#  dataCollection-v3.py
#  Description: A program to collect data from Arduino and save to csv file
#  Author: Ken Yeh 475496
#  Date: 13-01-2021
#  Revision: 3.1.1
#
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2022 Ken Yeh (P.)

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import serial
import csv
import datetime
import math
import sys
import timeit
import time
import os
import threading
# Data input order: Temperature, accelerometer1 (Top), accelerometer2(Side), microphone1(Top left), microphone2(Top right), microphone3(bottom)
inputData_raw = []



def countdown(runtime):
    while time.time() < runtime:
     if(len(inputData_raw) > 0):
        raw = (inputData_raw[len(inputData_raw) - 1][1] << 8) | inputData_raw[len(inputData_raw) - 1][0]
        if(raw > 0 and raw < 1023):
            R1 = 10000
            c1 = float(1.129252142e-03)
            c2 = float(2.341083183e-04)
            c3 = float(0.8773267909e-07)
            R2 = R1 * (1023.0 / float(raw) - 1.0)
            logR2 = math.log(R2)
            temp = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
            print("[INFO] Time left: " + str(runtime - int(time.time())) + " Temp: "+ str(round((temp - 273.15), 1))  + "      ", end="\r")
        else:
            print("[INFO] Time left: " + str(runtime - int(time.time())) + " Temp: 0.00" +"   ", end="\r")
        


def readData(port, duration):
    try:
        # Define serial port, baud rate and timeout (Baudrate is ignored in SerialUSB)
        arduino = serial.Serial(port, 0, timeout=0.1)
    except IOError as e:
        print("[Error-DueIO] " + str(e))
        sys.exit(1)

    try:
        # inputData_raw = []
        print("[INFO] Collecting data...")
        runtime = time.time() + int(duration)
        x = threading.Thread(target=countdown, args=(int(runtime),))
        x.start()
        start = timeit.default_timer()
        while time.time() < runtime:
            # Collect raw data and store in the memory for further processing
            inputData_raw.append(list(arduino.read(2*6)))
        stop = timeit.default_timer()
        print("[INFO] Processing data...                                     ")
        filename = "Sensor_output_" + \
            datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + "_" + \
            str(round((stop - start), 4)) + '.csv'
        try:
            file = open(filename, 'w+', newline='')
        except IOError as e:
            print("[Error-csvIO] " + str(e))
            sys.exit(1)
        csv_writer = csv.writer(file)
        count = len(inputData_raw)
        invalid = 0
        for i in inputData_raw:
            toAppend = []
            index = 0
            while(index < len(i)):
                # Shift the bits to the right position
                raw = i[index+1] << 8 | i[index]
                if raw > 1023 or raw <= 0:
                    invalid += 1
                toAppend.append(i[index+1] << 8 | i[index])
                index += 2
            # Write processed data to output file
            csv_writer.writerow(toAppend)

        print("[INFO] Collected " + str(count) + " data in " +
              str(round((stop - start), 4)) + " second(s)" + " with " + str(invalid) + " invalid data.")
        return filename
    except Exception as e:
        print("[Error-Data] " + str(e))
        sys.exit(1)


print("========== DataCollection.py v3.1.1 BY Ken Yeh ==========")
try:
    print("[INFO] Program started\n[INFO] Port: " +
          sys.argv[1] + " Duration: " + sys.argv[2] + " second(s)")
    outputFile = readData(sys.argv[1], sys.argv[2])

except Exception as e:
    print("[Error-argv] Format dataCollection-v3.py [Port] [Duration]")
    sys.exit(1)
print("[INFO] Output file name: " + outputFile + "\n[INFO] Output file size: " +
      str(round(os.path.getsize(outputFile)/1024)) + " KB")
print("[INFO] Program terminated!")
