from datetime import datetime
import time
import random
import paho.mqtt.client as mqtt
from app.core.config import settings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create an MQTT client instance
client = mqtt.Client()

# Set MQTT username and password and connect to the broker
client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
client.connect(settings.MQTT_BROKER_URL, settings.MQTT_BROKER_PORT, 60)

# Start the loop
client.loop_start()

while True:
    current_time = datetime.utcnow()
    temperature_data = {
        "device_name": f"device_{random.randint(1, 3)}",
        "temperature": random.uniform(20, 30),
        "timestamp": current_time.isoformat()
    }

    temperature_str = str(temperature_data).replace("'", "\"")
    result = client.publish("temperature", temperature_str)

    # Check if the publish was successful
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        logger.info(f"Successfully published message: {temperature_str}")
    else:
        logger.error(f"Failed to publish message. Error code: {result.rc}")

    time.sleep(2)
