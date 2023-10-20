import time
import random
import paho.mqtt.publish as publish

MQTT_BROKER = "217.120.251.115"
MQTT_PORT = 5683
MQTT_USERNAME = "lyvmqttuser"
MQTT_PASSWORD = "lyvmqttuser"

# List of valid device IDs from your table
VALID_DEVICE_IDS = [11, 13, 14, 15]


def generate_temperature() -> float:
    """
    Generate a random temperature value between 20 and 30.

    Returns:
        float: Random temperature value.
    """
    return random.uniform(20, 30)


def main():
    """Main loop for sending random temperature values for random devices to the MQTT broker."""
    while True:
        device_id = random.choice(VALID_DEVICE_IDS)  # Choose a random device from the valid list
        temp = generate_temperature()
        topic = f"device/{device_id}"
        publish.single(
            topic,
            payload=str(temp),
            hostname=MQTT_BROKER,
            port=MQTT_PORT,
            auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
        )
        time.sleep(60)


if __name__ == "__main__":
    main()
