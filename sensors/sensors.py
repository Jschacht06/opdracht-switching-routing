import json, random, time
import paho.mqtt.client as mqtt


BROKER = "mosquitto"  # moet internal docker ip worden
PORT = 1883
TOPIC_BATHROOM = "/home/sensors/bathroom"
TOPIC_BEDROOM = "/home/sensors/bedroom"
TOPIC_SERVER_ROOM = "/home/sensors/server_room"

mqttc = mqtt.Client()
mqttc.connect(BROKER, PORT)

# Function to randomly add abnormal values with a certain chance
def error(value, bad_min, bad_max, chance=0.05): # 5% chance to produce an error
    if random.random() < chance:
        return round(random.uniform(bad_min, bad_max), 2)
    return value

while True:
    # Bathroom
    bath_temp = round(random.uniform(290.00, 302.50), 2)
    bath_humi = round(random.uniform(0.50, 0.85), 2)

    bath_temp = error(bath_temp, 235.00, 255.00)
    bath_humi = error(bath_humi, 1.10, 1.50)

    msg = {'temperature': bath_temp, 'humidity': bath_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BATHROOM, msg_string)

    # Bedroom
    bed_temp = round(random.uniform(282.50, 297.50), 2)
    bed_humi = round(random.uniform(0.40, 0.55), 2)

    bed_temp = error(bed_temp, 330.00, 380.00)
    bed_humi = error(bed_humi, 0.95, 1.15)

    msg = {'temperature': bed_temp, 'humidity': bed_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_BEDROOM, msg_string)

    # Server room
    server_temp = round(random.uniform(295.50, 320.00), 2)
    server_humi = round(random.uniform(0.30, 0.45), 2)

    server_temp = error(server_temp, 350.00, 380.00)
    server_humi = error(server_humi, 0.95, 1.15)

    msg = {'temperature': server_temp, 'humidity': server_humi}
    msg_string = json.dumps(msg)
    mqttc.publish(TOPIC_SERVER_ROOM, msg_string)

    # Global wait
    time.sleep(5)