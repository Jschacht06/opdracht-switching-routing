import json, random, time
import paho.mqtt.client as mqtt


BROKER = "mosquitto" #moet internal docker ip worden
PORT = 1883
TOPIC_BATHROOM = "/home/sensors/bathroom"
TOPIC_BEDROOM = "/home/sensors/bedroom"
TOPIC_SERVER_ROOM = "/home/sensors/server_room"

mqttc = mqtt.Client()
mqttc.connect(BROKER, PORT)

while True:
#Bathroom
    bath_temp = random.randint(270.00, 302.50)
    bath_humi = random.randint(0.50, 0.85)

    msg = {'temperature': bath_temp, 'humidity': bath_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BATHROOM, msg_string)

#Bedroom
    bed_temp = random.randint(282.50, 297.50)
    bed_humi = random.randint(0.40, 0.55)

    msg = {'temperature': bed_temp, 'humidity': bed_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BEDROOM, msg_string)

#Server room
    server_temp = random.randint(290.00, 320.00)
    server_humi = random.randint(0.30, 0.45)

    msg = {'temperature': server_temp, 'humidity': server_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_SERVER_ROOM, msg_string)
    
#Global wait
    time.sleep(5)