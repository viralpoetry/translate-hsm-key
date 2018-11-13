#!/usr/bin/python
import serial
from time import sleep


class HSM(object):
    def __init__(self, port, speed, tout):
        self.ser = serial.Serial(port, speed, timeout=tout)

    def to_hsm(self, data):
        self.ser.write("\r\n")  # windows version
        self.ser.write(data)
        sleep(0.5)

    def from_hsm(self):
        data = ""
        while True:
            bytesToRead = self.ser.inWaiting()
            ret = self.ser.read(bytesToRead)
            if len(ret) > 0:
                data += ret
                sleep(0.2)
            else:
                # if len(data) is not 0:
                break
        return data

    def close(self):
        self.ser.close()

    def __exit__(self):
        self.ser.close()
