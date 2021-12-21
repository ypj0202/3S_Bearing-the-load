#
#  dataCollection-v3.py
#  Description: A program to collect data from Arduino and save to csv file
#  Author: Ken Yeh 475496
#  Date: 16-12-2021
#  Revision: 3.1.0
#
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


def countdown(t):
    while t:
        print("[INFO] Time left: " + str(t) + "   ", end="\r")
        time.sleep(1)
        t -= 1


def readData(port, duration):
    try:
        # Define serial port, baud rate and timeout (Baudrate is ignored in SerialUSB)
        arduino = serial.Serial(port, 0, timeout=0.1)
    except IOError as e:
        print("[Error-DueIO] " + str(e))
        sys.exit(1)

    try:
        inputData_raw = []
        print("[INFO] Collecting data...")
        runtime = time.time() + int(duration)
        x = threading.Thread(target=countdown, args=(int(duration),))
        x.start()
        start = timeit.default_timer()
        while time.time() < runtime:
            # Collect raw data and store in the memory for further processing
            inputData_raw.append(list(arduino.read(2*6)))
        stop = timeit.default_timer()
        print("[INFO] Processing data...")
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
                if raw > 1023:
                    raw = 1023
                    invalid += 1
                if index == 0:
                    # Temperature calculation
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
            # Write processed data to output file
            csv_writer.writerow(toAppend)

        print("[INFO] Collected " + str(count) + " data in " +
              str(round((stop - start), 4)) + " second(s)" + " Invalid data: " + str(invalid))
        return filename
    except Exception as e:
        print("[Error-Data] " + str(e))
        sys.exit(1)


print("========== DataCollection.py v3.1.0 BY Ken Yeh ==========")
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
