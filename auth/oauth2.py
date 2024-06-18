from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime,timedelta,UTC
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
import os


oauth2scheme = OAuth2PasswordBearer('login')

SECRET_KEY = os.environ.get('FASTAPI_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({'exp': expire})

    encoded_jwt = jwt.encode(data,SECRET_KEY,ALGORITHM)

    return encoded_jwt


def get_current_user(token: str = Depends(oauth2scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        username = payload.get('username')
        if not username:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    user = db_user.get_user_by_username(db,username)
    if not user:
        raise credential_exception
    return user