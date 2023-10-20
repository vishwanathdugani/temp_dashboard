from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.schemas.token import TokenData
from app.crud import user as user_crud
from app.crud import device as device_crud
from app.core import config
from app.db.sessions import get_db
from app.db.models import User, Device

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.settings.API_V1_STR}/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Fetch the current authenticated user based on the JWT token.

    Args:
        db (Session): Database session.
        token (str): JWT token.

    Returns:
        User: Authenticated User ORM model instance.

    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_device(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Device:
    """
    Fetch the device associated with the authenticated user.

    Args:
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        Device: Device ORM model instance associated with the user.

    Raises:
        HTTPException: If no device is found for the user.
    """
    device = device_crud.get_devices_by_owner(db, owner_id=current_user.id)
    if not device:
        raise HTTPException(status_code=400, detail="No device found for this user")
    return device
