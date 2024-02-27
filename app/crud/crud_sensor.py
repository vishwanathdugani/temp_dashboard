from sqlalchemy.orm import Session
from app.db.models import Sensor
from app.schemas.schemas import SensorCreate, SensorUpdate


def create_sensor(db: Session, sensor: SensorCreate) -> Sensor:
    db_sensor = Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor(db: Session, sensor_id: int) -> Sensor:
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensors_by_plant(db: Session, plant_id: int) -> list[Sensor]:
    return db.query(Sensor).filter(Sensor.plant_id == plant_id).all()


def update_sensor(db: Session, sensor_id: int, sensor_update: SensorUpdate) -> Sensor:
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if db_sensor:
        update_data = sensor_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sensor, key, value)
        db.commit()
        db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db: Session, sensor_id: int):
    db.query(Sensor).filter(Sensor.id == sensor_id).delete()
    db.commit()
