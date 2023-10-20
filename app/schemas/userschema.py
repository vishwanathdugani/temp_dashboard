from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

# from app.db.models import Device
from app.schemas.deviceschema import DeviceSchema


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    devices: List[DeviceSchema] = []

    class Config:
        from_attributes = True
