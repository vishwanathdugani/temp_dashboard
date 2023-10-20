from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    temperature: float
    timestamp: datetime


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureSchema(TemperatureBase):
    id: int
    device_id: int

    class Config:
        from_attributes = True
