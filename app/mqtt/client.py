import datetime
import time
import logging
import paho.mqtt.client as mqtt

from app.crud.temperature import create_temperature
from app.db.sessions import SessionLocal
from app.schemas.temperatureschema import TemperatureCreate

# Set up logging
logging.basicConfig(level=logging.INFO)

MQTT_BROKER = "217.120.251.115"
MQTT_PORT = 5683
MQTT_USERNAME = "lyvmqttuser"
MQTT_PASSWORD = "lyvmqttuser"


def on_connect(client: mqtt.Client, userdata, flags, rc: int) -> None:
    """Callback for when the client receives a CONNACK response from the server."""
    if rc == 0:
        logging.info(f"Connected to broker with result code {rc}")
        client.subscribe("device/#")  # Subscribe to device topics
    else:
        logging.error(f"Connection failed with result code {rc}")


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    """Callback for when a PUBLISH message is received from the server."""
    try:
        topic = msg.topic
        device_id = int(topic.split('/')[-1])
        temperature_value = float(msg.payload.decode())

        # Structure the data to match the TemperatureCreate schema
        temperature_data = {
            "temperature": temperature_value,
            "timestamp": datetime.datetime.now()  # Assuming you want to use the current time
        }

        db = SessionLocal()
        try:
            logging.info(f"Received data: {temperature_data}")
            create_temperature(db, TemperatureCreate(**temperature_data), device_id)
        except Exception as e:
            logging.error(f"Error saving temperature data to database: {e}")
        finally:
            db.close()

    except Exception as e:
        logging.error(f"Error processing message: {e}")


def on_disconnect(client: mqtt.Client, userdata, rc: int) -> None:
    """Callback for when the client disconnects from the server."""
    if rc != 0:
        logging.warning(f"Unexpected MQTT disconnection. Will auto-reconnect")


def start_mqtt_listener() -> None:
    """Start the MQTT listener."""
    client = mqtt.Client()
    try:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        while True:
            try:
                logging.info("Attempting to connect to MQTT broker...")
                client.connect(MQTT_BROKER, MQTT_PORT, 60)
                client.loop_forever()
            except Exception as e:
                logging.error(f"Error in MQTT main loop: {e}. Retrying in 5 seconds...")
                time.sleep(5)
    except Exception as e:
        logging.error(f"Error initializing MQTT client: {e}")


if __name__ == "__main__":
    start_mqtt_listener()
