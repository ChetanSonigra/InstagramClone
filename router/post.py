from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import PostDisplay,PostBase
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_post import create_post,get_all_posts
from typing import List

router = APIRouter(
    prefix="/post",
    tags=['post']
)

image_url_types = ['absolute','relative']

@router.post("",response_model=PostDisplay)
def create_a_post(request: PostBase,db: Session = Depends(get_db)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    return create_post(db,request)


@router.get("/all",response_model=List[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

