from sqlalchemy.orm import Session
from router.schemas import CommentBase
from db.models import DbComment
from datetime import datetime, UTC

def get_all(db: Session, post_id: int):
    comments = db.query(DbComment).filter(DbComment.post_id==post_id).all()
    return comments
    

def create(db: Session,request: CommentBase):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        timestamp = datetime.now(UTC),
        post_id = request.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment