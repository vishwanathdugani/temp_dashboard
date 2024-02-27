import threading
from fastapi import FastAPI
from fastapi import Request

from app.api.endpoints import login, users, plants, sensor, sensor_reading
from app.core import config
from app.db.base import Base
from app.db.sessions import engine
# from app.mqtt.client import start_mqtt_listener

app = FastAPI()

app.include_router(login.router, tags=["login"])
app.include_router(users.router, prefix=config.settings.API_V1_STR, tags=["users"])
app.include_router(plants.router, prefix=config.settings.API_V1_STR, tags=["temperature"])
app.include_router(sensor.router, prefix=config.settings.API_V1_STR, tags=["sensor"])
app.include_router(sensor_reading.router, prefix=config.settings.API_V1_STR, tags=["sensor-readings"])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the incoming request path
    print(f"Incoming request: {request.url.path}")
    response = await call_next(request)
    return response


# @app.on_event("startup")
# async def startup_event():
#     """
#     Event that gets triggered on application startup.
#     Starts the MQTT listener using a separate thread.
#     """
#     threading.Thread(target=start_mqtt_listener, daemon=True).start()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
