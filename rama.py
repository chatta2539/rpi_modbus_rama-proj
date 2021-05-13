from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRtu #initialize a serial RTU client instance

from pymodbus.transaction import ModbusRtuFramer
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("54.254.158.8", 1883, 60)
mqttc.loop_start()

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
        print(readmodbus('192.168.1.139', 1))
        mqttc.publish("raeh/rama/md1/pwm", readmodbus('192.168.1.139', 1))
    except Exception as err:
        print("No 1",err)
        mqttc.publish("raeh/rama/md1/pwm/err", str(err))
    time.sleep(sleep)

    try:
        print(readmodbus('192.168.1.139', 2))
        mqttc.publish("raeh/rama/md2/pwm", readmodbus('192.168.1.139', 2))
    except Exception as err:
        print("No 2",err)
        mqttc.publish("raeh/rama/md2/pwm/err", str(err))
    time.sleep(sleep)

    try:
        print(readrtu(1))
        mqttc.publish("raeh/rama/md3/pwm", readrtu(1))
    except Exception as err:
        mqttc.publish("raeh/rama/md3/pwm/err", str(err))
    time.sleep(sleep)
    
while True:

    task(1)
    


