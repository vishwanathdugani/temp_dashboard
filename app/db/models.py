from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    """User ORM model. Represents a user in the system."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship with the Plant model
    plants = relationship("Plant", back_populates="owner")


class Plant(Base):
    """Plant ORM model. Represents a plant profile associated with a user."""
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String)

    # Relationship with the User model
    owner = relationship("User", back_populates="plants")

    # Relationship with the Sensor model
    sensors = relationship("Sensor", back_populates="plant")


class Sensor(Base):
    """Sensor ORM model. Represents a sensor associated with a plant."""
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # e.g., "temperature", "moisture", etc.
    unit = Column(String)  # e.g., "Celsius", "%", etc.
    plant_id = Column(Integer, ForeignKey("plants.id"))

    plant = relationship("Plant", back_populates="sensors")

    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    """SensorReading ORM model. Represents a reading from a sensor."""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)  # The reading value
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    sensor = relationship("Sensor", back_populates="readings")
