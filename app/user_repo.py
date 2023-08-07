import jwt
from pydantic import BaseModel, validator
from attrs import define
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from .database import Base
import re

class UserChangeRequest(BaseModel):
    name : str | None = None
    surname : str | None = None
    city : str | None = None
    phone : str | None = None

class UserRequest(BaseModel):
    email: str | None = None
    name : str | None = None
    surname : str | None = None
    password : str | None = None
    city : str | None = None
    phone : str | None = None 

    @validator("email")
    def validate_email(cls, email):
        pattern = r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"
        if re.search(pattern, email):
            return email
        else:
            raise ValueError("Not correct email")
    
    @validator("password")
    def validate_password(cls, password):
        pattern = r"^.{6,20}$"
        if re.search(pattern, password):
            return password
        else:
            raise ValueError("Not correct password, password is too easy, imagine more difficult password, write the password which length is more than 6 symbbols")
    
    @validator("name")
    def validate_name(cls, name):
        pattern = r"^[a-zA-Z]+(?:[-\s][a-zA-Z]+)*$"
        if re.search(pattern, name):
            return name
        else:
            raise ValueError("Not correct name")
    
    @validator("surname")
    def validate_surname(cls, surname):
        pattern = r"^[a-zA-Z]+(?:[-\s][a-zA-Z]+)*$"
        if re.search(pattern, surname):
            return surname
        else:
            raise ValueError("Not correct surname")  
    
    @validator("phone")
    def validate_phone(cls, phone):
        pattern = r"^\+\d{1,3}\d{4,14}$"
        if re.search(pattern, phone):
            return phone
        else:
            raise ValueError("Not correct phone")
    
class UserResponse(BaseModel):
    email: str
    name : str
    surname : str
    city : str
    phone : str
    id: int = 0
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    city = Column(String)
    phone = Column(String)
    

    
class UsersRepository:
    def create_user(self, db : Session, user : UserRequest) -> UserRequest:
        user = User(email = user.email, name = user.name, surname = user.surname, 
                    password = self.encode_email(user.password), city = user.city, phone = user.phone)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self, db : Session,  email : str) -> User:
        return db.query(User).filter(User.email == email).first()
        
    def encode_email(self, email) -> str:
        key = "Ramazan_the_best"
        algorithm = "HS256"
        shifr_email = jwt.encode(payload={"email" : email}, key=key, algorithm=algorithm)
        return shifr_email
        
    def decode_token(self, token) -> dict:
        key = "Ramazan_the_best"
        algorithm = "HS256"
        email = jwt.decode(jwt=token, key=key, algorithms=algorithm)
        return email
    
    def update_data(self, db : Session, email_of_user : str, new_data_of_user : UserChangeRequest) -> None:
        user : User = self.get_user_by_email(db, email=email_of_user)
        if new_data_of_user.name != None:
            user.name = new_data_of_user.name
        if new_data_of_user.surname != None:
            user.surname = new_data_of_user.surname
        if new_data_of_user.city != None:
            user.city = new_data_of_user.city
        if new_data_of_user.phone != None:
            user.phone = new_data_of_user.phone
        db.commit()
        return None
        
                                                                                                                                                                                                                                                                                                    