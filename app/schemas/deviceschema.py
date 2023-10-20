from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

# from app.db.models import Temperature
from app.schemas.temperatureschema import TemperatureBase


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class DeviceSchema(DeviceBase):
    id: int
    temperatures: List[TemperatureBase] = []

    class Config:
        from_attributes = True
