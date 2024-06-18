from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import Comment,CommentBase, UserAuth
from db.database import get_db
from db.db_comment import get_all,create
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

@router.get("/all/{post_id}",response_model=List[Comment])
def get_comments(post_id: int,db: Session = Depends(get_db)):
    return get_all(db,post_id)


@router.post("/new",response_model=Comment)
def create_comment(request:CommentBase ,db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
    return create(db,request)