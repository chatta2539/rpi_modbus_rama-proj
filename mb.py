from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import time
import json

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
    rr = client.read_holding_registers(0x0000,50,unit=add)
    print(rr)
    print(rr.registers)
    x = {
    "Ia": rr.registers[0],
    "Ib": rr.registers[1],
    "Ic": rr.registers[2]
    }
    y = json.dumps(x)
    return y

print(readmodbus('192.168.43.218', 2))

# while True:

    # rr = client.read_holding_registers(0x0000,50,unit=1)
    # print(rr)
    # print(rr.registers)
    
    # rr = client.read_holding_registers(0x0000,50,unit=2)
    # print(rr)
    # print(rr.registers)
    
    # time.sleep(1)