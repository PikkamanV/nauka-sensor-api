from fastapi import FastAPI
from CO2Meter import CO2Meter
from typing import Dict
import threading
import serial
import time

co2meter = CO2Meter("/dev/hidraw0")

app = FastAPI()

environment_data = {}

def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def calc_crc(buf, length):
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1):
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return (bytearray([crcL, crcH]))


def update_environment_data():
    ser = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE)

    while True:
        command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
        command = command + calc_crc(command, len(command))

        ser.write(command)
        time.sleep(0.1)
        data = ser.read(ser.inWaiting())

        environment_data["Temperature"] = str(s16(int(hex(data[9]) + '{:02x}'.format(data[8], 'x'), 16)) / 100)
        environment_data["Relative humidity"] = str(int(hex(data[11]) + '{:02x}'.format(data[10], 'x'), 16) / 100)
        environment_data["Ambient light"] = str(int(hex(data[13]) + '{:02x}'.format(data[12], 'x'), 16))
        environment_data["Barometric pressure"] = str(int(hex(data[17]) + '{:02x}'.format(data[16], 'x')
                                                + '{:02x}'.format(data[15], 'x') + '{:02x}'.format(data[14], 'x'), 16) / 1000)
        environment_data["Sound noise"] = str(int(hex(data[19]) + '{:02x}'.format(data[18], 'x'), 16) / 100)
        environment_data["eTVOC"] = str(int(hex(data[21]) + '{:02x}'.format(data[20], 'x'), 16))
        environment_data["eCO2"] = str(int(hex(data[23]) + '{:02x}'.format(data[22], 'x'), 16))
        environment_data["Discomfort index"] = str(int(hex(data[25]) + '{:02x}'.format(data[24], 'x'), 16) / 100)
        environment_data["Heat stroke"] = str(s16(int(hex(data[27]) + '{:02x}'.format(data[26], 'x'), 16)) / 100)
        environment_data["Vibration information"] = str(int(hex(data[28]), 16))
        environment_data["SI value"] = str(int(hex(data[30]) + '{:02x}'.format(data[29], 'x'), 16) / 10)
        environment_data["PGA"] = str(int(hex(data[32]) + '{:02x}'.format(data[31], 'x'), 16) / 10)
        environment_data["Seismic intensity"] = str(int(hex(data[34]) + '{:02x}'.format(data[33], 'x'), 16) / 1000)
        environment_data["Temperature flag"] = str(int(hex(data[36]) + '{:02x}'.format(data[35], 'x'), 16))
        environment_data["Relative humidity flag"] = str(int(hex(data[38]) + '{:02x}'.format(data[37], 'x'), 16))
        environment_data["Ambient light flag"] = str(int(hex(data[40]) + '{:02x}'.format(data[39], 'x'), 16))
        environment_data["Barometric pressure flag"] = str(int(hex(data[42]) + '{:02x}'.format(data[41], 'x'), 16))
        environment_data["Sound noise flag"] = str(int(hex(data[44]) + '{:02x}'.format(data[43], 'x'), 16))
        environment_data["eTVOC flag"] = str(int(hex(data[46]) + '{:02x}'.format(data[45], 'x'), 16))
        environment_data["eCO2 flag"] = str(int(hex(data[48]) + '{:02x}'.format(data[47], 'x'), 16))
        environment_data["Discomfort index flag"] = str(int(hex(data[50]) + '{:02x}'.format(data[49], 'x'), 16))
        environment_data["Heat stroke flag"] = str(int(hex(data[52]) + '{:02x}'.format(data[51], 'x'), 16))
        environment_data["SI value flag"] = str(int(hex(data[53]), 16))
        environment_data["PGA flag"] = str(int(hex(data[54]), 16))
        environment_data["Seismic intensity flag"] = str(int(hex(data[55]), 16))

        time.sleep(1)

threading.Thread(target=update_environment_data, daemon=True).start()

@app.get("/api/environment")
async def get_environment_data() -> Dict:
    return environment_data

@app.get("/api/co2")
async def get_co2_data() -> Dict:
    co2_data = co2meter.get_data()

    return co2_data
