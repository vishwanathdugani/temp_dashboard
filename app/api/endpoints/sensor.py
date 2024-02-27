from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.crud.crud_sensor import create_sensor, get_sensor, get_sensors_by_plant, update_sensor, delete_sensor
from app.schemas.schemas import SensorCreate, Sensor, SensorUpdate
from app.db.models import User

router = APIRouter()


@router.post("/sensors/", response_model=Sensor)  # Adjusted to return Sensor instead of SensorCreate
def create_new_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Sensor:
    # Ensure the plant belongs to the current_user here
    # You might want to add logic to verify the plant_id belongs to the current_user
    return create_sensor(db=db, sensor=sensor)  # Adjust


@router.get("/sensors/{sensor_id}", response_model=Sensor)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)) -> Sensor:
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@router.get("/plants/{plant_id}/sensors/", response_model=list[Sensor])
def read_sensors_by_plant(plant_id: int, db: Session = Depends(get_db)) -> list[Sensor]:
    return get_sensors_by_plant(db, plant_id)


@router.put("/sensors/{sensor_id}", response_model=SensorUpdate)
def update_sensor_data(
    sensor_id: int, sensor_update: SensorUpdate, db: Session = Depends(get_db)
) -> Sensor:
    db_sensor = update_sensor(db, sensor_id, sensor_update)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@router.delete("/sensors/{sensor_id}", response_model=None)
def delete_sensor_data(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    delete_sensor(db, sensor_id)
    return JSONResponse(status_code=200, content={"message": f"Sensor with ID {sensor_id} deleted successfully"})
