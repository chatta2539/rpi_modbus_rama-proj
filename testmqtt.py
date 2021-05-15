import paho.mqtt.client as mqtt
import time

def on_connect(mqttc, userdata, rc):
    print("Connected with result code "+str(rc))
    if rc!=0 :
        mqttc.reconnect()

def on_publish(mqttc, userdata, mid):
    print "Published"

def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        mqttc.reconnect()
    else :
        print "Disconnected successfully"

# Setup MQTT
# broker='test.mosquitto.org'
broker = '54.254.158.8'
broker_port=1883

# Create a client instance
mqttc=mqtt.Client(client_id="MyClient123")
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect

while 1:

    mqttc.connect(broker, broker_port, 60)

    try:
        topic = "this/is/a/test/topic"
        payload = "test_message"
        print "Publishing " + payload + " to topic: " + topic + " ..."
        mqttc.publish(topic, payload, 0)

    except Exception as e:
        print "exception"
        log_file=open("log.txt","w")
        log_file.write(str(time.time())+" "+e.__str__())
        log_file.close()

    mqttc.disconnect()
    print ""
    time.sleep(3)   