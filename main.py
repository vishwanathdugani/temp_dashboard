import logging
import threading
from fastapi import FastAPI
from app.api.endpoints import temperature
from app.mqtt.client import start_mqtt_client

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(temperature.router)


from sqlalchemy import create_engine
from app.db.sessions import engine  # Import the engine you've already defined
from app.db.base import Base  # Import the Base you've defined

def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting MQTT client in a background thread...")
    thread = threading.Thread(target=start_mqtt_client, daemon=True)
    thread.start()
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
