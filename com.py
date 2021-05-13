from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance

import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("54.254.158.8", 1883, 60)
mqttc.loop_start()

# host = '192.168.43.218'
# host1 = '192.168.100.1'
# port = 502 
# addNo = [10, 20, 30, 40, 50, 60] 
# # client = ModbusClient(host, port, framer=ModbusRtuFramer)
# # client.connect()

# # ip = host + '1'

# # print(ip)

# for i  in range(len(addNo)):
#     print(addNo[i])
#     i += 2
#     ip = host1 + str(i)
#     print(str(ip))
#     print(client.read_holding_registers(0x0000,50,unit=1))
def readmodbus(ip, add):
    client = ModbusClient(ip, 502, framer=ModbusRtuFramer)
    client.connect()
    rr = client.read_holding_registers(0x0000, 50,unit=add)
    print(rr)
    print(rr.registers)
    x = {
    "Ia": rr.registers[0],
    "Ib": rr.registers[1],
    "Ic": rr.registers[2]
    }
    y = json.dumps(x)
    return y

    
def readmodbusrtu(ip, add):
    client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)

    client.connect()
    rr = client.read_holding_registers(0x0000, 50,unit=add)
    print(rr)
    print(rr.registers)
    x = {
    "Ia": rr.registers[0],
    "Ib": rr.registers[1],
    "Ic": rr.registers[2]
    }
    y = json.dumps(x)
    return y


while True:
    try:
        print(readmodbus('192.168.1.139', 1))
        mqttc.publish("raeh/rama/md1/pwm", readmodbus('192.168.1.139', 1))
    except Exception as err:
        print("No 1",err)
        mqttc.publish("raeh/rama/md1/pwm/err", str(err))
    time.sleep(1)

    try:
        print(readmodbus('192.168.1.139', 2))
        mqttc.publish("raeh/rama/md2/pwm", readmodbus('192.168.1.139', 2))
    except Exception as err:
        print("No 2",err)
        mqttc.publish("raeh/rama/md2/pwm/err", str(err))
    time.sleep(1)
