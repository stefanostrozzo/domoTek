import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "localhost"
MQTT_TOPIC = "home/living-room/temperature"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with code: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        client.publish(MQTT_TOPIC, "22.5")  # Simula sensore
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()