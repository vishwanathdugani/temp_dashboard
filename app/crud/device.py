from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Device
from app.schemas.deviceschema import DeviceCreate


def get_device(db: Session, device_id: int) -> Device:
    """
    Fetch a device by its ID.

    Args:
        db (Session): Database session.
        device_id (int): ID of the device.

    Returns:
        Device: Device ORM model instance.
    """
    return db.query(Device).filter(Device.id == device_id).first()


def get_devices_by_owner(db: Session, owner_id: int) -> list[Device]:
    """
    Fetch all devices owned by a given user.

    Args:
        db (Session): Database session.
        owner_id (int): ID of the device owner.

    Returns:
        List[Device]: List of Device ORM model instances owned by the user.
    """
    return db.query(Device).filter(Device.user_id == owner_id).all()


def create_device(db: Session, device: DeviceCreate, owner_id: int) -> Device:
    """
    Create a new device. Raises an error if a device with the same name already exists for the user.

    Args:
        db (Session): Database session.
        device (DeviceCreate): Device creation schema.
        owner_id (int): ID of the device owner.

    Returns:
        Device: Created Device ORM model instance.

    Raises:
        HTTPException: If device with this name already exists for the user.
    """
    existing_device = db.query(Device).filter_by(name=device.name, user_id=owner_id).first()
    if existing_device:
        raise HTTPException(status_code=400, detail="Device with this name already exists for the user.")

    db_device = Device(**device.model_dump(), user_id=owner_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
