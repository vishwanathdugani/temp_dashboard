from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import sessions, SessionLocal
from app.schemas import temperature as temperature_schema
from app.crud import temperature as temperature_crud

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/temperature/")
def add_temperature(temperature: temperature_schema.Temperature, db: Session = Depends(sessions.SessionLocal)):
    return temperature_crud.create_temperature(db, temperature)


@router.get("/temperature/", response_model=List[temperature_schema.Temperature])
def get_all_temperatures(db: Session = Depends(get_db)):
    db_temperatures = temperature_crud.get_all_temperatures(db)
    return [temperature_schema.Temperature(**temp.__dict__) for temp in db_temperatures]


@router.get("/temperature/{temperature_id}")
def get_temperature(temperature_id: int, db: Session = Depends(get_db)):
    temp = temperature_crud.get_temperature_by_id(db, temperature_id)
    if not temp:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temp