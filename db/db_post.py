from .models import DbPost
from router.schemas import PostBase
from sqlalchemy.orm import Session
from datetime import datetime,UTC


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