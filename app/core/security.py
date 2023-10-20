from datetime import datetime, timedelta
from typing import Dict, Union
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hashed version.

    Args:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed version of the password.

    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password.

    Args:
        password (str): The plaintext password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Union[str, int]], expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (Dict[str, Union[str, int]]): Data to be encoded into the token.
        expires_delta (timedelta, optional): Token expiration duration. Defaults to 15 minutes.

    Returns:
        str: JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
