from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from app.db.models import Plant, Sensor
from app.schemas.schemas import PlantCreate, PlantUpdate


def create_plant(db: Session, plant_create: PlantCreate, user_id: int) -> Plant:
    existing_plant = db.query(Plant).filter(Plant.name == plant_create.name, Plant.user_id == user_id).first()
    if existing_plant:
        raise HTTPException(status_code=400, detail="A plant with this name already exists for the current user")
    db_plant = Plant(name=plant_create.name, location=plant_create.location, user_id=user_id)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


def get_plant(db: Session, plant_id: int) -> Plant:
    return db.query(Plant).filter(Plant.id == plant_id).first()


def get_plants_by_user(db: Session, user_id: int) -> List[Plant]:
    return db.query(Plant).filter(Plant.user_id == user_id).all()


def update_plant(db: Session, plant_id: int, plant_update: PlantUpdate) -> Plant:
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant_update.name:
        duplicate_name = db.query(Plant).filter(Plant.id != plant_id,
                                                Plant.name == plant_update.name,
                                                Plant.user_id == db_plant.user_id).first()
        if duplicate_name:
            raise HTTPException(status_code=400, detail="A plant with this name already exists for the current user")
    if plant_update.name is not None:
        db_plant.name = plant_update.name
    if plant_update.location is not None:
        db_plant.location = plant_update.location
    db.commit()
    db.refresh(db_plant)
    return db_plant


def delete_plant(db: Session, plant_id: int):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    # Optionally, handle or delete related sensors before deleting the plant
    db.query(Sensor).filter(Sensor.plant_id == plant_id).delete()
    db.delete(db_plant)
    db.commit()
