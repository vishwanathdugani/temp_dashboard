from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.db.sessions import get_db
from app.crud.device import create_device, get_devices_by_owner
from app.schemas.deviceschema import DeviceCreate, DeviceSchema
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/devices/", response_model=DeviceSchema)
def create_new_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DeviceSchema:
    """
    Create a new device for the authenticated user.

    Args:
        device (DeviceCreate): Device creation schema.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        DeviceSchema: Created device's schema.

    Raises:
        HTTPException: If a device with the same name already exists for the user.
    """
    try:
        return create_device(db=db, device=device, owner_id=current_user.id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Device with this name already exists for the user.")


@router.get("/devices/", response_model=List[DeviceSchema])
def list_devices(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> List[DeviceSchema]:
    """
    List all devices owned by the authenticated user.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        List[DeviceSchema]: List of devices owned by the user.
    """
    return get_devices_by_owner(db=db, owner_id=current_user.id)
