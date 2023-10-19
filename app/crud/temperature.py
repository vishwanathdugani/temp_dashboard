from sqlalchemy.orm import Session
from app.db import models
from app.schemas.temperature import Temperature

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_temperature(db: Session, temperature: Temperature):
    logging.info(f"-----------------{temperature.model_dump()}")
    db_temperature = models.TemperatureDB(**temperature.dict())  # Use .dict() instead of .model_dump()
    logging.info(f"-----------------{db_temperature.temperature}{db_temperature.device_name}")
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_all_temperatures(db: Session):
    return db.query(models.TemperatureDB).all()


def get_temperature_by_id(db: Session, temperature_id: int):
    return db.query(models.TemperatureDB).filter(models.TemperatureDB.id == temperature_id).first()
