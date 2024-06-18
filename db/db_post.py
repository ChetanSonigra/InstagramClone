from .models import DbPost
from router.schemas import PostBase
from sqlalchemy.orm import Session
from datetime import datetime,UTC
from fastapi import HTTPException, status


def create_post(db: Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        user_id = request.creator_id,
        timestamp = datetime.now(UTC)
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(db: Session):
    posts = db.query(DbPost).all()
    return posts


def delete_post(id: int,db: Session, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found."
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only post creator can delete a post"
        )
    db.delete(post)
    db.commit()
    return f"Post with id {id} deleted."