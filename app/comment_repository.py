from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Session, relationship
from .database import Base
from .user_repo import User
import datetime
from typing import List

class Comment_request(BaseModel):
    content : str | None = None

class Comment_response(BaseModel):
    comment_id : int
    user_id : int
    advert_id : int
    content : str
    created_at : str

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    advert_id = Column(Integer)
    content = Column(String)
    created_at = Column(String)
    
class Comment_repo():
    def add_comment(self, db : Session, user : User, advert_id : int, comment : Comment_request) -> None:
        time_now = str(datetime.datetime.now())
        comment = Comment(user_id = user.id, advert_id = advert_id, content = comment.content, created_at = time_now)
        db.add(comment)
        db.commit()
        
    def get_comments(self, db : Session, advert_id : int) -> List[Comment]:
        comments = db.query(Comment).filter(Comment.advert_id == advert_id).all()
        return comments
    
    def change_comment(self, db : Session, comment_id : int, user : User, advert_id : int, new_data_of_comment : Comment_request) -> bool:
        comment : Comment = db.query(Comment).filter(Comment.comment_id == comment_id, Comment.advert_id == advert_id, Comment.user_id == user.id).first()
        if comment != None:
            if comment.content != new_data_of_comment.content and new_data_of_comment.content != None:
                comment.content = new_data_of_comment.content
                db.commit()
            return False
        else:
            return True
    
    def delete_comment(self, db : Session, comment_id : int, advert_id : int, user : User) -> bool:
        comment = db.query(Comment).filter(Comment.comment_id == comment_id, Comment.advert_id == advert_id, Comment.user_id == user.id).first()
        if comment != None:
            db.delete(comment)
            db.commit()
            return False
        else:
            return True
    
    def get_count_of_comments(self, db : Session, advert_id : int) -> int:
        comments = self.get_comments(db, advert_id)
        count_of_comments = 0
        if comments != None:
            count_of_comments = len(comments)
        return count_of_comments