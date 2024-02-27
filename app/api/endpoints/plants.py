from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.db.sessions import get_db
from app.api.deps import get_current_user
from app.crud.crud_plant import (
    create_plant, get_plants_by_user, get_plant, update_plant, delete_plant
)
from app.schemas.schemas import PlantCreate, Plant, PlantUpdate
from app.db.models import User

router = APIRouter()


@router.post("/plants/", response_model=Plant)
def create_new_plant(
    plant: PlantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Plant:
    """
    Create a new plant record in the database for the current user.

    Parameters:
    - plant: PlantCreate - The plant data to be created.
    - db: Session - Database session dependency.
    - current_user: User - The current user obtained via dependency.

    Returns:
    - Plant: The created plant record.
    """
    return create_plant(db=db, plant_create=plant, user_id=current_user.id)


@router.get("/plants/", response_model=List[Plant])
def read_plants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Plant]:
    """
    Retrieve a list of plant records for the current user.

    Parameters:
    - db: Session - Database session dependency.
    - current_user: User - The current user obtained via dependency.

    Returns:
    - List[Plant]: A list of plant records.
    """
    return get_plants_by_user(db=db, user_id=current_user.id)


@router.get("/plants/{plant_id}", response_model=Plant)
def read_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Plant:
    """
    Retrieve a single plant record by its ID for the current user.

    Parameters:
    - plant_id: int - The ID of the plant to retrieve.
    - db: Session - Database session dependency.
    - current_user: User - The current user obtained via dependency.

    Raises:
    - HTTPException: 404 error if the plant is not found or does not belong to the current user.

    Returns:
    - Plant: The requested plant record.
    """
    plant = get_plant(db=db, plant_id=plant_id)
    if plant is None or plant.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.put("/plants/{plant_id}", response_model=Plant)
def update_existing_plant(
    plant_id: int,
    plant_update: PlantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Plant:
    """
    Update an existing plant record in the database for the current user.

    Parameters:
    - plant_id: int - The ID of the plant to update.
    - plant_update: PlantUpdate - The updated plant data.
    - db: Session - Database session dependency.
    - current_user: User - The current user obtained via dependency.

    Raises:
    - HTTPException: 404 error if the plant is not found or does not belong to the current user.

    Returns:
    - Plant: The updated plant record.
    """
    db_plant = get_plant(db=db, plant_id=plant_id)
    if db_plant is None or db_plant.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plant not found")
    return update_plant(db=db, plant_id=plant_id, plant_update=plant_update)


@router.delete("/plants/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_plant(
    plant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Delete an existing plant record in the database for the current user.

    Parameters:
    - plant_id: int - The ID of the plant to delete.
    - db: Session - Database session dependency.
    - current_user: User - The current user obtained via dependency.

    Raises:
    - HTTPException: 404 error if the plant is not found or does not belong to the current user.

    Returns:
    - Response: HTTP response with a success message.
    """
    db_plant = get_plant(db=db, plant_id=plant_id)
    if db_plant is None or db_plant.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plant not found")
    delete_plant(db=db, plant_id=plant_id)
    return Response(content="Plant deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
