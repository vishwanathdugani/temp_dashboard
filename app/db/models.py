from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base
from datetime import datetime


class TemperatureDB(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, index=True)
    temperature = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
