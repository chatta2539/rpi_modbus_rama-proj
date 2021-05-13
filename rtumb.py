import pymodbus
import time
import json

# import serial
# from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
# from pymodbus.transaction import ModbusRtuFramer

# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from


def readrtu(add):
    client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)
    r1 = client.read_holding_registers(164, 10, unit= add)
    r2 = client.read_holding_registers(180, 10, unit= add)
    r3 = client.read_holding_registers(188, 10, unit= add)
    r4 = client.read_holding_registers(124, 10, unit= add)
    r5 = client.read_holding_registers(418, 10, unit= add)
    # print(r1.registers)
    # print(r2.registers)
    # print(r3.registers)
    # print(r4.registers)
    # print(r5.registers)
    # print(r1.registers[0], r2.registers[0], r3.registers[0], r4.registers[0], r5.registers[0])
    x = {
    "Ia": r1.registers[0]*0.1,
    "Ib": r2.registers[0],
    "Ic": r5.registers[0]
    }
    y = json.dumps(x)
    return y

while True:
    try:
        print(readrtu(1))
    except Exception as err:
        print("Error", err)
    
    time.sleep(1)

#Closes the underlying socket connection
# client.close()