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

time.sleep(20)


# log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

# logFile = '/home/pi/Desktop/log/logfile.log'

# my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=999, encoding=None, delay=0)
# my_handler.setFormatter(log_formatter)
# my_handler.setLevel(logging.INFO)

# app_log = logging.getLogger('root')
# app_log.setLevel(logging.INFO)

# app_log.addHandler(my_handler)
mqttc = mqtt.Client()
mqttc.connect("54.254.158.8", 1883, 60)
mqttc.loop_start()

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
rtu = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'N', baudrate = 9600)
dataM = ""
data1 = ""
data3 = ""
data4 = ""
data5 = ""
data6 = ""
data7 = ""
dataMain = ""
list_data = [dataM, data1, data3, data4, data5, data6, data7, dataMain]
bk_mqtt = ["raeh/rama/building4/pwm", "raeh/rama/floor1/pwm", "raeh/rama/floor3/pwm", "raeh/rama/floor4/pwm",
"raeh/rama/floor5/pwm", "raeh/rama/floor6/pwm", "raeh/rama/floor7/pwm", "raeh/rama/MDB/pwm"]
bk_mqtt_err = ["raeh/rama/building4/pwm/err", "raeh/rama/floor1/pwm/err", "raeh/rama/floor3/pwm/err", "raeh/rama/floor4/pwm/err",
"raeh/rama/floor5/pwm/err", "raeh/rama/floor6/pwm/err", "raeh/rama/floor7/pwm/err", "raeh/rama/MDB/pwm/err"]
def readmodbus(server, add):
    r1 = server.read_holding_registers(0, 50, unit= add)
    x = {
    "Va": round(r1.registers[0]*0.01, 2),
    "Vb": round(r1.registers[1]*0.01, 2),
    "Vc": round(r1.registers[2]*0.01, 2),
    "Ia": round(r1.registers[9]*0.1, 2),
    "Ib": round(r1.registers[10]*0.1, 2),
    "Ic": round(r1.registers[11]*0.1, 2),
    "Pa": round(r1.registers[14]*0.1, 2),
    "Pb": round(r1.registers[16]*0.1, 2),
    "Pc": round(r1.registers[18]*0.1, 2),
    "Psum": round(r1.registers[20]*0.1, 2),
    "PFa": round(r1.registers[38]*0.001, 2),
    "PFb": round(r1.registers[39]*0.001, 2),
    "PFc": round(r1.registers[40]*0.001, 2),
    "PFsum": round(r1.registers[41]*0.001, 2),
    "Hz": round(r1.registers[42]*0.01, 2)
    }
    y = json.dumps(x)
    return y

def readrtu(add):
    r1 = rtu.read_holding_registers(0, 50, unit= add)
    x = {
    "Va": round(r1.registers[0]*0.01, 2),
    "Vb": round(r1.registers[1]*0.01, 2),
    "Vc": round(r1.registers[2]*0.01, 2),
    "Ia": round(r1.registers[9]*0.1, 2),
    "Ib": round(r1.registers[10]*0.1, 2),
    "Ic": round(r1.registers[11]*0.1, 2),
    "Pa": round(r1.registers[14]*0.1, 2),
    "Pb": round(r1.registers[16]*0.1, 2),
    "Pc": round(r1.registers[18]*0.1, 2),
    "Psum": round(r1.registers[20]*0.1, 2),
    "PFa": round(r1.registers[38]*0.001, 2),
    "PFb": round(r1.registers[39]*0.001, 2),
    "PFc": round(r1.registers[40]*0.001, 2),
    "PFsum": round(r1.registers[41]*0.001, 2),
    "Hz": round(r1.registers[42]*0.01, 2)
    }
    y = json.dumps(x)
    return y
def readmian():
    r1 = rtu.read_holding_registers(110, 20, unit= 1)
    x = {
    "Va": 0,
    "Vb": 0,
    "Vc": 0,
    "Ia": r1.registers[1],
    "Ib": r1.registers[2],
    "Ic": r1.registers[3],
    "Pa": r1.registers[7],
    "Pb": r1.registers[8],
    "Pc": r1.registers[9],
    "Psum": r1.registers[10],
    "PFa": 0,
    "PFb": 0,
    "PFc": 0,
    "PFsum": 0,
    "Hz": 0
    }
    y = json.dumps(x)
    return y
def taskModbus():
    try:
        list_data[0] = readrtu(19)
        print("Floor M : ", list_data[0])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/building4/pwm/err", str(err))
    try:
        list_data[1] = readrtu(2)
        print("Floor 1 : ", list_data[1])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor1/pwm/err", str(err))

    try:
        list_data[2] = readmodbus(floor3, 45)
        print("Floor 3 : ", list_data[2])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor3/pwm/err", str(err))
    try:
        list_data[3] = readmodbus(floor4, 70)
        print("Floor 4 : ", list_data[3])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor4/pwm/err", str(err))
    try:
        list_data[4] = readmodbus(floor5, 95)
        print("Floor 5 : ", list_data[4])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor5/pwm/err", str(err))
    try:
        list_data[5] = readmodbus(floor6, 120)
        print("Floor 6 : ", list_data[5])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor6/pwm/err", str(err))
    try:
        list_data[6] = readmodbus(floor7, 145)
        print("Floor 7 : ", list_data[6])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/floor7/pwm/err", str(err))
    try:
        list_data[7] = readmian()
        print("MDB : ", list_data[7])
    except Exception as err:
        print(err)
        mqttc.publish("raeh/rama/MDB/pwm/err", str(err))


def taskMQTT():
    for mq in range(len(list_data)):
        try:
            if list_data[mq] != "":
                mqttc.publish(bk_mqtt[mq], list_data[mq])
        except Exception as err:
            mqttc.publish(bk_mqtt_err[mq], str(err))


previous_time = time.time() 
while True:
    if time.time()-previous_time >= 15:
        previous_time = time.time()
        taskMQTT()
    else:
        taskModbus()
    time.sleep(1)
    
    
