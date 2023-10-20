from sqlalchemy.orm import Session

from app.db.models import Temperature, Device
from app.schemas.temperatureschema import TemperatureCreate


def create_temperature(db: Session, temperature: TemperatureCreate, device_id: int) -> Temperature:
    """
    Create a new temperature reading.

    Args:
        db (Session): Database session.
        temperature (TemperatureCreate): Temperature creation schema.
        device_id (int): ID of the associated device.

    Returns:
        Temperature: Created Temperature ORM model instance.
    """
    db_temperature = Temperature(**temperature.model_dump(), device_id=device_id)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_latest_temperatures(db: Session, device_id: int) -> Temperature:
    """
    Fetch the latest temperature reading for a given device.

    Args:
        db (Session): Database session.
        device_id (int): ID of the device.

    Returns:
        Temperature: Latest Temperature ORM model instance for the given device.
    """
    return db.query(Temperature).filter(Temperature.device_id == device_id).order_by(Temperature.timestamp.desc()).first()


def get_temperatures_by_device(db: Session, device_id: int) -> list[Temperature]:
    """
    Fetch all temperature readings for a given device.

    Args:
        db (Session): Database session.
        device_id (int): ID of the device.

    Returns:
        List[Temperature]: List of Temperature ORM model instances for the given device.
    """
    return db.query(Temperature).filter(Temperature.device_id == device_id).all()


def get_temperatures_by_device_name(db: Session, device_name: str) -> list[Temperature]:
    """
    Fetch all temperature readings for a device by its name.

    Args:
        db (Session): Database session.
        device_name (str): Name of the device.

    Returns:
        List[Temperature]: List of Temperature ORM model instances for the given device name.
    """
    device = db.query(Device).filter(Device.name == device_name).first()
    if not device:
        return None
    return db.query(Temperature).filter(Temperature.device_id == device.id).all()
