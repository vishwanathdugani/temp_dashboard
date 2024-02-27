from sqlalchemy.orm import Session
from app.db.models import SensorReading
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate


def create_sensor_reading(db: Session, sensor_reading: SensorReadingCreate, sensor_id: int) -> SensorReading:
    db_reading = SensorReading(**sensor_reading.dict(), sensor_id=sensor_id)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


def get_sensor_reading(db: Session, reading_id: int) -> SensorReading:
    return db.query(SensorReading).filter(SensorReading.id == reading_id).first()


def get_readings_by_sensor(db: Session, sensor_id: int) -> list[SensorReading]:
    return db.query(SensorReading).filter(SensorReading.sensor_id == sensor_id).all()


def update_sensor_reading(db: Session, reading_id: int, reading_update: SensorReadingUpdate) -> SensorReading:
    db_reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
    if db_reading:
        update_data = reading_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reading, key, value)
        db.commit()
        db.refresh(db_reading)
    return db_reading


def delete_sensor_reading(db: Session, reading_id: int):
    db.query(SensorReading).filter(SensorReading.id == reading_id).delete()
    db.commit()
