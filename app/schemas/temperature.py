from pydantic import BaseModel
from datetime import datetime


class Temperature(BaseModel):
    device_name: str
    temperature: float
    timestamp: datetime
