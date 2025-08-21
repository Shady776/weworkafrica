from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.background import P
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
from .. import models, schemas, utils
from ..database import get_db


    
router = APIRouter(
    prefix = "/users",
    tags=['users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User( 
        email=user.email,
        password=hashed_password,
        name=user.name,
        phone_number=user.phone_number
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=schemas.UserProfile)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user


# @router.get("/", response_model=List[schemas.User])    
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.User).all()
#     return posts

@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User with id: {id} does not exixt")
    return users

    