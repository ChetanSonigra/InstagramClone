from fastapi import APIRouter, Depends, HTTPException, status
from .oauth2 import get_current_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import DbUser
from hashing import Hash
from .oauth2 import create_access_token

router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Credentials!'
        )
    if not Hash.verify(request.password, user.password):
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = 'Incorrect password!'
        )
    
    access_token = create_access_token(data={'username': user.username})

    return {
           "access_token": access_token,
           'token_type': 'bearer',
           'user_id': user.id
    }

