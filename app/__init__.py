from fastapi import FastAPI
from app.api.endpoints import temperature

app = FastAPI()

app.include_router(temperature.router)
