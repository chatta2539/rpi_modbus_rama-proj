from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRtu

from pymodbus.transaction import ModbusRtuFramer
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import urllib.request
import datetime

def readmodbus(ip, add):
    client = ModbusClient(ip, 502, framer=ModbusRtuFramer)
    client.connect()
    r1 = client.read_holding_registers(0, 10, unit= add)
    r2 = client.read_holding_registers(10, 10, unit= add)
    r3 = client.read_holding_registers(20, 2, unit= add)
    r4 = client.read_holding_registers(30, 10, unit= add)
    r5 = client.read_holding_registers(40, 3, unit= add)
    x = {
    "Va": r1.registers[0]*0.01,
    "Vb": r1.registers[1]*0.01,
    "Vc": r1.registers[2]*0.01,
    "Ia": r1.registers[9]*0.1,
    "Ib": r2.registers[0]*0.1,
    "Ic": r2.registers[1]*0.1,
    "Pa": r2.registers[4]*0.1,
    "Pb": r2.registers[6]*0.1,
    "Pc": r2.registers[8]*0.1,
    "Psum": r3.registers[0]*0.1,
    "PFa": r4.registers[8]*0.001,
    "PFb": r4.registers[9]*0.001,
    "PFc": r5.registers[0]*0.001,
    "PFsum": r5.registers[1]*0.001,
    "Hz": r5.registers[2]*0.01
    }
    y = json.dumps(x)
    return y

def readrtu(add):
    client = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)
    r1 = client.read_holding_registers(0, 10, unit= add)
    r2 = client.read_holding_registers(10, 10, unit= add)
    r3 = client.read_holding_registers(20, 2, unit= add)
    r4 = client.read_holding_registers(30, 10, unit= add)
    r5 = client.read_holding_registers(40, 3, unit= add)
    x = {
    "Va": r1.registers[0]*0.01,
    "Vb": r1.registers[1]*0.01,
    "Vc": r1.registers[2]*0.01,
    "Ia": r1.registers[9]*0.1,
    "Ib": r2.registers[0]*0.1,
    "Ic": r2.registers[1]*0.1,
    "Pa": r2.registers[4]*0.1,
    "Pb": r2.registers[6]*0.1,
    "Pc": r2.registers[8]*0.1,
    "Psum": r3.registers[0]*0.1,
    "PFa": r4.registers[8]*0.001,
    "PFb": r4.registers[9]*0.001,
    "PFc": r5.registers[0]*0.001,
    "PFsum": r5.registers[1]*0.001,
    "Hz": r5.registers[2]*0.01
    }
    y = json.dumps(x)
    return y

def task(sleep):
    try:
        mqttc.publish("raeh/rama/floor2/pwm", readmodbus('192.168.100.12', 20))
    except Exception as err:
        mqttc.publish("raeh/rama/floor2/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor3/pwm", readmodbus('192.168.100.13', 45))
    except Exception as err:
        mqttc.publish("raeh/rama/floor3/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor4/pwm", readmodbus('192.168.100.14', 70))
    except Exception as err:
        mqttc.publish("raeh/rama/floor4/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor5/pwm", readmodbus('192.168.100.15', 95))
    except Exception as err:
        mqttc.publish("raeh/rama/floor5/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor6/pwm", readmodbus('192.168.100.16', 120))
    except Exception as err:
        mqttc.publish("raeh/rama/floor6/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor7/pwm", readmodbus('192.168.100.17', 145))
    except Exception as err:
        mqttc.publish("raeh/rama/floor7/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/floor1/pwm", readrtu(2))
    except Exception as err:
        mqttc.publish("raeh/rama/floor1/pwm/err", str(err))
    time.sleep(sleep)

    try:
        mqttc.publish("raeh/rama/building4/pwm", readrtu(19))
    except Exception as err:
        mqttc.publish("raeh/rama/building4/pwm/err", str(err))
    time.sleep(sleep)

def internet_on():
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=2)
        return True
    except:
        return False
    
while True:

    while internet_on():
        try:
            mqttc = mqtt.Client()
            mqttc.connect("54.254.158.8", 1883, 60)
            mqttc.loop_start()
        except Exception as err:
            print("Internet connection: ", err)
        task(0.5)
        mqttc.disconnect()
    


