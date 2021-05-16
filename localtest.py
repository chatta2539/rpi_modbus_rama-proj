from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRtu

from pymodbus.transaction import ModbusRtuFramer
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import urllib.request
import datetime

time.sleep(20)

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

bk_mqtt_tcp = ["raeh/rama/test2/pwm", "raeh/rama/test3/pwm"]
bk_mqtt_tcp_err = ["raeh/rama/test2/pwm/err", "raeh/rama/test2/pwm/err"]
add_mb_tcp = [1, 2]
ip_mb_tcp = ['192.168.137.1', '192.168.137.1']

add_mb_rtu = [1, 2]
bk_mqtt_rtu = ["raeh/rama/test4/pwm", "raeh/rama/test4/pwm"]
bk_mqtt_rtu_err = ["raeh/rama/test4/pwm/err", "raeh/rama/test4/pwm/err"]

for i in range(len(bk_mqtt_tcp)):
    print(bk_mqtt_tcp[i] + " " + bk_mqtt_tcp_err[i] + " " + str(add_mb_tcp[i]) + " : " + ip_mb_tcp[i])

def task(sleep):
    print(bk_mqtt_tcp[1])
    # print(readmodbus('192.168.137.1', 1))

    # print("Start loop")
    for x in range(len(bk_mqtt_tcp)):
        print(x)
        data = ""
        try:
            data = readmodbus(ip_mb_tcp[x], add_mb_tcp[x])
            print(data)
        except Exception as err:
            print(err) 
            mqttc.publish(bk_mqtt_tcp_err[x], str(err)) 
        
        if data != "":
            try:
                mqttc.publish(bk_mqtt_tcp[x], data)
            except Exception as err:
                mqttc.publish(bk_mqtt_tcp_err[x], str(err))
        time.sleep(sleep)

    for x in range(len(add_mb_rtu)):
        print(x)
        data_rtu = ""
        try:
            data_rtu = readrtu(add_mb_rtu[x])
            print(data_rtu)
        except Exception as err:
            print(err) 
            mqttc.publish(bk_mqtt_rtu_err[x], str(err))
        
        if data_rtu != "":
            try:
                mqttc.publish(bk_mqtt_rtu[x], data)
            except Exception as err:
                mqttc.publish(bk_mqtt_rtu_err[x], str(err))
    


    # try:
    #     mqttc.publish("raeh/rama/floor1/pwm", readrtu(2))
    # except Exception as err:
    #     mqttc.publish("raeh/rama/floor1/pwm/err", str(err))
    # time.sleep(sleep)

    # try:
    #     mqttc.publish("raeh/rama/building4/pwm", readrtu(19))
    # except Exception as err:
    #     mqttc.publish("raeh/rama/building4/pwm/err", str(err))
    # time.sleep(sleep)

def internet_on():
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=2)
        return True
    except:
        return False

mqttc = mqtt.Client()
mqttc.connect("54.254.158.8", 1883, 60)
mqttc.loop_start() 


while True:
    task(0.5)

