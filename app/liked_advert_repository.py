from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Session, relationship
from .database import Base
from .user_repo import User
from .advertisement_repo import Advert
from typing import List

class LikedAdvertResponse(BaseModel):
    advert_id : int
    address : str

class add_liked_advert_response(BaseModel):
    user_id : int
    advert_id : int
    address : str

class LikedAdvert(Base):
    __tablename__ = "liked_adverts"
    liked_advert_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    advert_id = Column(Integer)
    address = Column(String)
    

class Liked_advert_repo():
    
    def save_liked_advert(self, db : Session, user_id : int, advert : Advert) -> LikedAdvert:
        liked_advert = LikedAdvert(
            user_id=user_id,
            advert_id=advert.advert_id,
            address=advert.address            
        )
        db.add(liked_advert)
        db.commit()
        return liked_advert
    
    def get_liked_advert(self, db : Session, user : User) -> List[LikedAdvert]:
        return db.query(LikedAdvert).filter(LikedAdvert.user_id == user.id).all()
        
    def delete_liked_adv(self, db : Session, user : User, advert_id : int) -> bool:
        liked_advert = db.query(LikedAdvert).filter(LikedAdvert.advert_id == advert_id, LikedAdvert.user_id == user.id).first()
        if liked_advert != None:
            db.delete(liked_advert)
            db.commit()
            return False
        else:
            return True
        
    
    
    