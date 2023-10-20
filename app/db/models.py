from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    """User ORM model. Represents a user in the system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship with the Device model
    devices = relationship("Device", back_populates="owner")


class Device(Base):
    """Device ORM model. Represents a device associated with a user."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship with the User model
    owner = relationship("User", back_populates="devices")

    # Relationship with the Temperature model
    temperatures = relationship("Temperature", back_populates="device")


class Temperature(Base):
    """Temperature ORM model. Represents a temperature reading from a device."""

    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    device_id = Column(Integer, ForeignKey("devices.id"))

    # Relationship with the Device model
    device = relationship("Device", back_populates="temperatures")
