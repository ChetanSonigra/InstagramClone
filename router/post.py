from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from .schemas import PostDisplay,PostBase, UserAuth
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_post import create_post,get_all_posts, delete_post
from typing import List
from auth.oauth2 import get_current_user
import random, string, shutil

router = APIRouter(
    prefix="/post",
    tags=['post']
)

image_url_types = ['absolute','relative']

@router.post("",response_model=PostDisplay)
def create_a_post(request: PostBase,db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    return create_post(db,request)


@router.get("/all",response_model=List[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f"_{random_str}."
    filename = new.join(image.filename.rsplit('.',1))
    filepath = f"images/{filename}"
    with open(filepath, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"File uploaded: {filepath}"


