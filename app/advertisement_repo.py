from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, or_
from sqlalchemy.orm import Session, relationship
from .database import Base
from .user_repo import User
from typing import List
INF = 9999999
class Advert_request(BaseModel):
    type : str | None = None
    price : int | None = None
    address : str | None = None
    area : float | None = None
    rooms_count : int | None = None
    description : str | None = None

class Advert_response(BaseModel):
    type : str | None = None
    price : int | None = None
    address : str | None = None
    area : float | None = None
    rooms_count : int | None = None
    description : str | None = None
    total_comments : int = 0

class Advert_info_response(BaseModel):
    advert_id : int
    type : str
    price : int
    address : str
    area : float
    rooms_count : int

class Advert(Base):
    __tablename__ = "adverts"
    advert_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(String)
    price = Column(Integer)
    address = Column(String)
    area = Column(Float)
    rooms_count = Column(Integer)
    description = Column(String)
    creating_order = Column(Integer, autoincrement=True)

class Search_advert_response(BaseModel):
    total : int = 0
    objects : List[Advert_info_response] = []
    
class Adverts_repository():
    def add_advert(self, db : Session, advert : Advert_request, user : User) -> Advert:
        advertisement = Advert(
            user_id = user.id, type = advert.type,
            price = advert.price, address = advert.address, area = advert.area,
            rooms_count = advert.rooms_count, description = advert.description
        )
        db.add(advertisement)
        db.commit()
        db.refresh(advertisement)
        return advertisement
    
    def get_advert(self, db : Session, advert_id : int) -> Advert | None:
        advert = db.query(Advert).filter(Advert.advert_id == advert_id).first()
        return advert
    
    def change_advert(self, db : Session, advert_id : int, user : User, new_data_of_advert : Advert_request) -> bool:
        advert : Advert = db.query(Advert).filter(Advert.advert_id == advert_id).first()
        if advert.user_id == user.id:
            if advert.type != new_data_of_advert.type and new_data_of_advert.type != None:
                advert.type = new_data_of_advert.type
            
            if advert.price != new_data_of_advert.price and new_data_of_advert.price != None:
                advert.price = new_data_of_advert.price
            
            if advert.address != new_data_of_advert.address and new_data_of_advert.address != None:
                advert.address = new_data_of_advert.address
            
            if advert.area != new_data_of_advert.area and new_data_of_advert.area != None:
                advert.area = new_data_of_advert.area
            
            if advert.rooms_count != new_data_of_advert.rooms_count and new_data_of_advert.rooms_count != None:
                advert.rooms_count = new_data_of_advert.rooms_count
            
            if advert.description != new_data_of_advert.description and new_data_of_advert.description != None:
                advert.description = new_data_of_advert.description

            db.commit()
            return False
        else:
            return True
        
    def delete_advert(self, db : Session, advert_id : int, user : User) -> bool:
        advert : Advert = self.get_advert(db, advert_id)
        if advert.user_id == user.id:
            db.delete(advert)
            db.commit()
            return False
        else:
            return True
    
    def searhc_advert(
            self, 
            db : Session,
            limit : int = INF,
            offset : int = 0, 
            type_1 : str = "sell",
            type_2 : str = "rent",
            main_type : str | None = None,
            rooms_cnt1 : int = 0,
            rooms_cnt2 : int = INF,
            main_rooms_cnt : int | None = None,
            price_from : int = 0,
            price_until : int = INF 
    ) -> Search_advert_response:    
        if main_type != None:
            type_1 = main_type
            type_2 = main_type
            
        if main_rooms_cnt != None:
            rooms_cnt1 = main_rooms_cnt
            rooms_cnt2 = main_rooms_cnt
        list_of_advert = (
            db.query(Advert)
            .filter(or_(Advert.type == type_1, Advert.type == type_2), 
                    Advert.price >= price_from, Advert.price <= price_until, 
                    Advert.rooms_count >= rooms_cnt1, Advert.rooms_count <= rooms_cnt2
            )
            .order_by(Advert.creating_order.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        cl = Search_advert_response()
        cl.total = len(list_of_advert)
        cl.objects = list_of_advert
        return cl
        
    
        
        