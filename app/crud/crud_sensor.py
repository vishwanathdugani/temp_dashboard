from sqlalchemy.orm import Session
from app.db.models import Sensor
from app.schemas.schemas import SensorCreate, SensorUpdate


def create_sensor(db: Session, sensor: SensorCreate) -> Sensor:
    """
    Create a new sensor record in the database.

    Parameters:
    - db: Session - The database session.
    - sensor: SensorCreate - The sensor data to create.

    Returns:
    - Sensor: The created Sensor object.
    """
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor(db: Session, sensor_id: int) -> Sensor:
    """
    Retrieve a sensor record by its ID.

    Parameters:
    - db: Session - The database session.
    - sensor_id: int - The ID of the sensor to retrieve.

    Returns:
    - Sensor: The Sensor object if found, None otherwise.
    """
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensors_by_plant(db: Session, plant_id: int) -> list[Sensor]:
    """
    Retrieve all sensor records associated with a specific plant.

    Parameters:
    - db: Session - The database session.
    - plant_id: int - The ID of the plant associated with the sensors.

    Returns:
    - list[Sensor]: A list of Sensor objects.
    """
    return db.query(Sensor).filter(Sensor.plant_id == plant_id).all()


def update_sensor(db: Session, sensor_id: int, sensor_update: SensorUpdate) -> Sensor:
    """
    Update an existing sensor record.

    Parameters:
    - db: Session - The database session.
    - sensor_id: int - The ID of the sensor to update.
    - sensor_update: SensorUpdate - The new sensor data.

    Returns:
    - Sensor: The updated Sensor object. Returns None if the sensor does not exist.
    """
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if db_sensor:
        update_data = sensor_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sensor, key, value)
        db.commit()
        db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db: Session, sensor_id: int):
    """
    Delete a sensor record by its ID.

    Parameters:
    - db: Session - The database session.
    - sensor_id: int - The ID of the sensor to delete.

    Note:
    - This function does not return any value.
    """
    db.query(Sensor).filter(Sensor.id == sensor_id).delete()
    db.commit()
