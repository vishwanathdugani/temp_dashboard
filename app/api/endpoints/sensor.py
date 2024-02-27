from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.crud.crud_sensor import (
    create_sensor, get_sensor, get_sensors_by_plant, update_sensor, delete_sensor
)
from app.schemas.schemas import SensorCreate, Sensor, SensorUpdate
from app.db.models import User

router = APIRouter()


@router.post("/sensors/", response_model=Sensor)
def create_new_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Sensor:
    """
    Create a new sensor record associated with a plant.

    Parameters:
    - sensor: SensorCreate - The sensor data to create.
    - db: Session - Database session dependency.
    - current_user: User - The current authenticated user.

    Returns:
    - Sensor: The created sensor record.
    """
    # Additional logic to verify plant_id ownership by current_user might be added here.
    return create_sensor(db=db, sensor=sensor)


@router.get("/sensors/{sensor_id}", response_model=Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)) -> Sensor:
    """
    Retrieve a sensor record by its ID.

    Parameters:
    - sensor_id: int - The ID of the sensor to retrieve.
    - db: Session - Database session dependency.

    Raises:
    - HTTPException: 404 error if the sensor is not found.

    Returns:
    - Sensor: The requested sensor record.
    """
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@router.get("/plants/{plant_id}/sensors/", response_model=list[Sensor])
def read_sensors_by_plant(plant_id: int, db: Session = Depends(get_db)) -> list[Sensor]:
    """
    Retrieve all sensors associated with a specific plant.

    Parameters:
    - plant_id: int - The ID of the plant.
    - db: Session - Database session dependency.

    Returns:
    - list[Sensor]: A list of sensors associated with the plant.
    """
    return get_sensors_by_plant(db, plant_id)


@router.put("/sensors/{sensor_id}", response_model=Sensor)
def update_sensor_data(
    sensor_id: int,
    sensor_update: SensorUpdate,
    db: Session = Depends(get_db)
) -> Sensor:
    """
    Update an existing sensor record.

    Parameters:
    - sensor_id: int - The ID of the sensor to update.
    - sensor_update: SensorUpdate - The new sensor data.
    - db: Session - Database session dependency.

    Raises:
    - HTTPException: 404 error if the sensor is not found.

    Returns:
    - Sensor: The updated sensor record.
    """
    db_sensor = update_sensor(db, sensor_id, sensor_update)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@router.delete("/sensors/{sensor_id}", response_model=None)
def delete_sensor_data(sensor_id: int, db: Session = Depends(get_db)):
    """
    Delete a sensor record by its ID.

    Parameters:
    - sensor_id: int - The ID of the sensor to delete.
    - db: Session - Database session dependency.

    Raises:
    - HTTPException: 404 error if the sensor is not found.

    Returns:
    - JSONResponse: Confirmation message of deletion.
    """
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    delete_sensor(db, sensor_id)
    return JSONResponse(status_code=200, content={"message": f"Sensor with ID {sensor_id} deleted successfully"})
