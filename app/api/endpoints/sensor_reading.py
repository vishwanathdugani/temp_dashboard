from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.crud_sensor_reading import (
    create_sensor_reading, get_sensor_reading, get_readings_by_sensor,
    update_sensor_reading, delete_sensor_reading
)
from app.db.sessions import get_db
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate, SensorReading

router = APIRouter()


@router.post("/sensor-readings/", response_model=SensorReading)
def create_sensor_reading_endpoint(
    reading: SensorReadingCreate, sensor_id: int, db: Session = Depends(get_db)
) -> SensorReading:
    """
    Create a sensor reading for a specified sensor.

    Parameters:
    - reading: SensorReadingCreate - The sensor reading data.
    - sensor_id: int - The ID of the sensor.
    - db: Session - The database session.

    Returns:
    - SensorReading: The created sensor reading.
    """
    return create_sensor_reading(db=db, sensor_reading=reading, sensor_id=sensor_id)


@router.get("/sensor-readings/{reading_id}/", response_model=SensorReading)
def read_sensor_reading_endpoint(
    reading_id: int, db: Session = Depends(get_db)
) -> SensorReading:
    """
    Retrieve a sensor reading by its ID.

    Parameters:
    - reading_id: int - The ID of the sensor reading to retrieve.
    - db: Session - The database session.

    Raises:
    - HTTPException: 404 error if the sensor reading is not found.

    Returns:
    - SensorReading: The requested sensor reading.
    """
    db_reading = get_sensor_reading(db, reading_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return db_reading


@router.get("/sensors/{sensor_id}/readings/", response_model=List[SensorReading])
def read_readings_by_sensor_endpoint(
    sensor_id: int, db: Session = Depends(get_db)
) -> List[SensorReading]:
    """
    Retrieve all sensor readings for a specified sensor.

    Parameters:
    - sensor_id: int - The ID of the sensor whose readings to retrieve.
    - db: Session - The database session.

    Returns:
    - List[SensorReading]: A list of sensor readings for the sensor.
    """
    return get_readings_by_sensor(db, sensor_id)


@router.put("/sensor-readings/{reading_id}/", response_model=SensorReading)
def update_sensor_reading_endpoint(
    reading_id: int, reading_update: SensorReadingUpdate, db: Session = Depends(get_db)
) -> SensorReading:
    """
    Update a sensor reading by its ID.

    Parameters:
    - reading_id: int - The ID of the sensor reading to update.
    - reading_update: SensorReadingUpdate - The new data for the sensor reading.
    - db: Session - The database session.

    Raises:
    - HTTPException: 404 error if the sensor reading is not found.

    Returns:
    - SensorReading: The updated sensor reading.
    """
    updated_reading = update_sensor_reading(db, reading_id, reading_update)
    if not updated_reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return updated_reading


@router.delete("/sensor-readings/{reading_id}/")
def delete_sensor_reading_endpoint(
    reading_id: int, db: Session = Depends(get_db)
):
    """
    Delete a sensor reading by its ID.

    Parameters:
    - reading_id: int - The ID of the sensor reading to delete.
    - db: Session - The database session.

    Returns:
    - Dict[str, bool]: Confirmation of deletion.
    """
    delete_sensor_reading(db, reading_id)
    return {"ok": True}
