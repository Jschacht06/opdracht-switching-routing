import json, random, time
import paho.mqtt.client as mqtt


BROKER = "localhost" #moet internal docker ip worden
PORT = 1883
TOPIC_BATHROOM = "/home/sensors/bathroom"
TOPIC_BEDROOM = "/home/sensors/bedroom"

mqttc = mqtt.Client()
mqttc.connect(BROKER, PORT)

while True:
#Bathroom
    bath_temp = random.randint(10, 35)
    bath_humi = random.randint(30, 70)

    msg = {'temperature': bath_temp, 'humidity': bath_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BATHROOM, msg_string)
    time.sleep(5)

#Bedroom
    bed_temp = random.randint(10, 35)
    bed_humi = random.randint(30, 70)

    msg = {'temperature': bed_temp, 'humidity': bed_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BEDROOM, msg_string)
    time.sleep(5)