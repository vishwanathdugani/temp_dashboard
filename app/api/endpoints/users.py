from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.crud.user import get_user_by_username, create_user
from app.schemas.schemas import UserCreate, User

router = APIRouter()


@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> User:

    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)
