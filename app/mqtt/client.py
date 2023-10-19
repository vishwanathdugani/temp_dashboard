import paho.mqtt.client as mqtt
from app.core.config import settings
from app.schemas.temperature import Temperature
from sqlalchemy.orm import Session
from app.db import sessions
from app.crud.temperature import create_temperature


import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    client.subscribe("temperature")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        temperature_data = Temperature.model_validate_json(payload)

        with sessions.SessionLocal() as db:
            create_temperature(db, temperature_data)
        # logger.info(f"Processed temperature data: {temperature_data}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


def start_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(username=settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    logger.info(f"starting to listen to temperature data")
    client.connect(settings.MQTT_BROKER_URL, settings.MQTT_BROKER_PORT, 60)
    client.loop_forever()
