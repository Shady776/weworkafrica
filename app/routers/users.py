from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


    
router = APIRouter(
    prefix = "/users",
    tags=['users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/", response_model=List[schemas.User])    
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts

@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User with id: {id} does not exixt")
        
    return users
    