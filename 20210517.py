from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRtu
from pymodbus.transaction import ModbusRtuFramer
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import urllib.request
import logging
from logging.handlers import RotatingFileHandler


# log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

# logFile = '/home/pi/Desktop/log/logfile.log'

# my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=999, encoding=None, delay=0)
# my_handler.setFormatter(log_formatter)
# my_handler.setLevel(logging.INFO)

# app_log = logging.getLogger('root')
# app_log.setLevel(logging.INFO)

# app_log.addHandler(my_handler)
floor2 = ModbusClient("192.168.100.12", 502, framer=ModbusRtuFramer)
floor2.connect()
floor3 = ModbusClient("192.168.100.13", 502, framer=ModbusRtuFramer)
floor3.connect()
floor4 = ModbusClient("192.168.100.14", 502, framer=ModbusRtuFramer)
floor4.connect()
floor5 = ModbusClient("192.168.100.15", 502, framer=ModbusRtuFramer)
floor5.connect()
floor6 = ModbusClient("192.168.100.16", 502, framer=ModbusRtuFramer)
floor6.connect()
floor7 = ModbusClient("192.168.100.17", 502, framer=ModbusRtuFramer)
floor7.connect()

rtu = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)
def readmodbus(server, add):
    
    r1 = server.read_holding_registers(0, 50, unit= add)
    x = {
    "Va": r1.registers[0]*0.01,
    "Vb": r1.registers[1]*0.01,
    "Vc": r1.registers[2]*0.01,
    "Ia": r1.registers[9]*0.1,
    "Ib": r1.registers[10]*0.1,
    "Ic": r1.registers[11]*0.1,
    "Pa": r1.registers[14]*0.1,
    "Pb": r1.registers[16]*0.1,
    "Pc": r1.registers[18]*0.1,
    "Psum": r1.registers[20]*0.1,
    "PFa": r1.registers[38]*0.001,
    "PFb": r1.registers[39]*0.001,
    "PFc": r1.registers[40]*0.001,
    "PFsum": r1.registers[41]*0.001,
    "Hz": r1.registers[42]*0.01
    }
    y = json.dumps(x)
    return y

def readrtu(add):
    client = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)
    r1 = client.read_holding_registers(0, 50, unit= add)
    x = {
    "Va": r1.registers[0]*0.01,
    "Vb": r1.registers[1]*0.01,
    "Vc": r1.registers[2]*0.01,
    "Ia": r1.registers[9]*0.1,
    "Ib": r1.registers[10]*0.1,
    "Ic": r1.registers[11]*0.1,
    "Pa": r1.registers[14]*0.1,
    "Pb": r1.registers[16]*0.1,
    "Pc": r1.registers[18]*0.1,
    "Psum": r1.registers[20]*0.1,
    "PFa": r1.registers[38]*0.001,
    "PFb": r1.registers[39]*0.001,
    "PFc": r1.registers[40]*0.001,
    "PFsum": r1.registers[41]*0.001,
    "Hz": r1.registers[42]*0.01
    }
    y = json.dumps(x)
    return y

client = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'N', baudrate = 9600)

while True:
    try:
        data2 = readmodbus(floor2, 20)
        print("Floor 2 : ", data2)
    except Exception as err:
        print(err)
    # try:
    #     data4 = readmodbus(floor4, 70)
    #     print("Floor 4 : ", data4)
    # except Exception as err:
    #     print(err)
    
    # time.sleep(0.1)

    #try:
    #    r1 = client.read_holding_registers(110, 15, unit= 1)
    #    print("Master")
     #   print(r1.registers)
     #   print(len(r1.registers))
   # except Exception as err:
    #    print(err)
   # try:
     #   r2 = client.read_holding_registers(0, 50, unit= 2)
    #    print("Floor 1")
   #     print(r2.registers)
  #      print(len(r2.registers))
 #   except Exception as err:
#        print(err)
    # time.sleep(0.1)

# client = ModbusClient("192.168.100.15", 502, framer=ModbusRtuFramer)
# client.connect()
# r1 = client.read_holding_registers(0, 10, unit= 90)
# print(r1.registers)


