from sqlalchemy.orm import Session
from app.db.models import SensorReading
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate


def create_sensor_reading(db: Session, sensor_reading: SensorReadingCreate, sensor_id: int) -> SensorReading:
    """
    Creates a sensor reading record in the database.

    Parameters:
    - db: Session - The database session.
    - sensor_reading: SensorReadingCreate - The data for the sensor reading to create.
    - sensor_id: int - The ID of the sensor associated with the reading.

    Returns:
    - SensorReading: The created SensorReading object.
    """
    db_reading = SensorReading(**sensor_reading.dict(), sensor_id=sensor_id)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


def get_sensor_reading(db: Session, reading_id: int) -> SensorReading:
    """
    Retrieves a sensor reading record by its ID.

    Parameters:
    - db: Session - The database session.
    - reading_id: int - The ID of the sensor reading to retrieve.

    Returns:
    - SensorReading: The SensorReading object if found, None otherwise.
    """
    return db.query(SensorReading).filter(SensorReading.id == reading_id).first()


def get_readings_by_sensor(db: Session, sensor_id: int) -> list[SensorReading]:
    """
    Retrieves all sensor reading records associated with a specific sensor ID.

    Parameters:
    - db: Session - The database session.
    - sensor_id: int - The ID of the sensor whose readings are to be retrieved.

    Returns:
    - list[SensorReading]: A list of SensorReading objects.
    """
    return db.query(SensorReading).filter(SensorReading.sensor_id == sensor_id).all()


def update_sensor_reading(db: Session, reading_id: int, reading_update: SensorReadingUpdate) -> SensorReading:
    """
    Updates a sensor reading record identified by its ID.

    Parameters:
    - db: Session - The database session.
    - reading_id: int - The ID of the sensor reading to update.
    - reading_update: SensorReadingUpdate - The updated data for the sensor reading.

    Returns:
    - SensorReading: The updated SensorReading object, or None if the reading does not exist.
    """
    db_reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
    if db_reading:
        update_data = reading_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reading, key, value)
        db.commit()
        db.refresh(db_reading)
        return db_reading
    return None


def delete_sensor_reading(db: Session, reading_id: int):
    """
    Deletes a sensor reading record by its ID.

    Parameters:
    - db: Session - The database session.
    - reading_id: int - The ID of the sensor reading to delete.

    Returns:
    - None
    """
    db.query(SensorReading).filter(SensorReading.id == reading_id).delete()
    db.commit()
