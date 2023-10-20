from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.models import User
from app.schemas.userschema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_user(db: Session, user_id: int) -> User:
    """
    Fetch a user by ID.

    Args:
        db (Session): Database session.
        user_id (int): User ID.

    Returns:
        User: User ORM model instance.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    """
    Fetch a user by username.

    Args:
        db (Session): Database session.
        username (str): Username.

    Returns:
        User: User ORM model instance.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.

    Args:
        db (Session): Database session.
        user (UserCreate): User creation schema.

    Returns:
        User: Created User ORM model instance.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
