from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext

from crud.user import crud_user
from db.session import get_db
from schemas.user import User

# To generate a secret_key string as below run: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # token expires in 24h temporarily
REFRESH_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # token expires in 7 days temporarily

# Use to hash raw password to hashed password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Specify the login API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an expired access token from user data"""

    to_encode = data.copy()  # data to be encoded

    # Add expired time for the token
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode into an JWT access token (using secret_key)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=7)
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    """Create hashed password from plain/raw password"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify if the plain password matches with the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(email: str) -> User | None:
    with get_db() as db:
        status, user_model = crud_user.get_user_by_email(db=db, email=email)
        if not status or user_model is None:
            return None

        return User.model_validate(user_model.__dict__)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = token_payload.get("sub")
        if email is None:
            raise credential_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credential_exception

    user = get_user_by_email(email)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User | None:
    """Get the current active user"""
    return current_user


async def validate_token(token: str = Depends(oauth2_scheme)) -> User | None:
    user = get_current_user(token=token)
    return user


AuthenticatedUser = Depends(get_current_active_user)
