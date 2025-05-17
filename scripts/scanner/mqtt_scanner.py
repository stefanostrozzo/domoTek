import paho.mqtt.client as mqtt

def scan():
    devices = []
    
    def on_message(client, userdata, msg):
        devices.append({
            'topic': msg.topic,
            'payload': msg.payload.decode(),
            'qos': msg.qos
        })
    
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("#")
    client.loop_start()
    time.sleep(10)  # Durata scansione
    client.loop_stop()
    
    return {
        "protocol": "mqtt",
        "timestamp": datetime.now().isoformat(),
        "devices": devices
    }