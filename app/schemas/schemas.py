from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PlantBase(BaseModel):
    pass


class SensorBase(BaseModel):
    pass


class SensorReadingBase(BaseModel):
    pass


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    plants: List['Plant'] = []

    class Config:
        from_attributes = True


class PlantBase(BaseModel):
    name: str
    location: Optional[str] = None


class PlantCreate(PlantBase):
    pass


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class Plant(PlantBase):
    id: int
    user_id: int
    sensors: List['Sensor'] = []

    class Config:
        from_attributes = True


class SensorBase(BaseModel):
    type: str
    unit: str
    plant_id: int

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    type: Optional[str] = Field(None, description="Type of the sensor (e.g., 'temperature', 'humidity').")
    unit: Optional[str] = Field(None, description="Unit of measurement for the sensor readings (e.g., 'Celsius', '%').")

# Assuming SensorReading is defined elsewhere and imported correctly
class Sensor(SensorBase):
    id: int
    readings: List['SensorReading'] = []

    class Config:
        from_attributes = True  # Adjusted from 'from_attributes' to 'orm_mode'

class SensorReadingBase(BaseModel):
    value: float
    timestamp: datetime


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReadingUpdate(BaseModel):
    value: Optional[float] = Field(None, description="The new value of the sensor reading.")
    timestamp: Optional[datetime] = Field(None, description="The new timestamp for the sensor reading.")


class SensorReading(SensorReadingBase):
    id: int
    sensor_id: int

    class Config:
        from_attributes = True


User.model_rebuild()
Plant.model_rebuild()
Sensor.model_rebuild()
SensorReading.model_rebuild()
