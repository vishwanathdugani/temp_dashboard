from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Device
from app.db.sessions import get_db
from app.crud.temperature import (
    create_temperature,
    get_latest_temperatures,
    get_temperatures_by_device,
    get_temperatures_by_device_name
)
from app.schemas.temperatureschema import TemperatureCreate, TemperatureSchema
from app.api.deps import get_current_device

router = APIRouter()


@router.post("/temperatures/", response_model=TemperatureSchema)
def add_temperature(
    temperature: TemperatureCreate,
    db: Session = Depends(get_db),
    current_device: List[Device] = Depends(get_current_device)
) -> TemperatureSchema:
    """Add a new temperature reading for the current device."""
    device_id = current_device[0].id if current_device else None
    return create_temperature(db=db, temperature=temperature, device_id=device_id)


@router.get("/temperatures/latest/", response_model=TemperatureSchema)
def get_latest_temperature(
    db: Session = Depends(get_db),
    current_device: List[Device] = Depends(get_current_device)
) -> TemperatureSchema:
    """Get the latest temperature reading for the current device."""
    device_id = current_device[0].id if current_device else None
    return get_latest_temperatures(db=db, device_id=device_id)


@router.get("/temperatures/", response_model=List[TemperatureSchema])
def list_temperatures(
    db: Session = Depends(get_db),
    current_device: List[Device] = Depends(get_current_device)
) -> List[TemperatureSchema]:
    """List all temperature readings for the current device."""
    device_id = current_device[0].id if current_device else None
    return get_temperatures_by_device(db=db, device_id=device_id)


@router.get("/temperatures/by_device_id/{device_id}/", response_model=List[TemperatureSchema])
def list_temperatures_by_device_id(
        device_id: int,
        db: Session = Depends(get_db),
        current_device: List[Device] = Depends(get_current_device)) -> List[TemperatureSchema]:
    """List all temperature readings for a given device ID."""
    temps = get_temperatures_by_device(db, device_id)
    if not temps:
        raise HTTPException(status_code=404, detail="Temperatures not found for the given device ID")
    return temps


@router.get("/temperatures/by_device_name/{device_name}/", response_model=List[TemperatureSchema])
def list_temperatures_by_device_name(
        device_name: str,
        db: Session = Depends(get_db),
        current_device: List[Device] = Depends(get_current_device)) -> List[TemperatureSchema]:
    """List all temperature readings for a given device name."""
    temps = get_temperatures_by_device_name(db, device_name)
    if not temps:
        raise HTTPException(status_code=404, detail="Temperatures not found for the given device name")
    return temps
