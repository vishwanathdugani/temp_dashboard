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
    # Ensure the sensor belongs to the current_user here
    return create_sensor_reading(db=db, reading=reading, sensor_id=sensor_id)
