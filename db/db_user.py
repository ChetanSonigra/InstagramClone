from sqlalchemy.orm import Session
from router.schemas import UserBase
from db.models import DbUser
from hashing import Hash


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


