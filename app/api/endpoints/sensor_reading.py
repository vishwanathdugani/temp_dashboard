from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.crud.crud_sensor_reading import create_sensor_reading
from app.schemas.schemas import SensorReadingCreate, SensorReading
from app.db.models import User

router = APIRouter()


@router.post("/sensor-readings/", response_model=SensorReading)
def create_sensor_reading_endpoint(
    reading: SensorReadingCreate,
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SensorReading:
    """
    Create a sensor reading associated with a specific sensor.

    Parameters:
    - reading: SensorReadingCreate - The sensor reading data to create.
    - sensor_id: int - The ID of the sensor to which the reading belongs.
    - db: Session - Database session dependency.
    - current_user: User - The current authenticated user.

    Returns:
    - SensorReading: The created sensor reading record.

    Note: The function assumes verification that the sensor belongs to the current user
    is performed within the `create_sensor_reading` function or elsewhere.
    """
    return create_sensor_reading(db=db, reading=reading, sensor_id=sensor_id)
