from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas
from ..database import get_db

    
router = APIRouter(
    prefix = "/spaces",
    tags=['spaces']
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Space)
def create_space(space: schemas.SpaceCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    existing_space = db.query(models.Space).filter(models.Space.address == space.address).first()
   
    if existing_space:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Space by this user already exist")
    
    
    new_space = models.Space(user_id = current_user.id, **space.dict())
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    
    return new_space

@router.get("/", response_model=List[schemas.SpaceOut])
def get_all_spaces(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
               limit: int = 15000, skip: int = 0, search: Optional[str] = ""):
    get_all_spaces = db.query(models.Space).filter(models.Space.title.contains(search)).limit(limit).offset(skip).all()
    return get_all_spaces




@router.get("/my-spaces", response_model=List[schemas.SpaceOut])
def get_user_spaces(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 15000,skip: int = 0,search: Optional[str] = ""):
    print("Current User ID:", current_user.id)
    user_spaces = db.query(models.Space).filter(models.Space.user_id == current_user.id).filter(
        models.Space.title.contains(search)).limit(limit).offset(skip).all()
    print("Spaces in DB for this user:", user_spaces)
    return user_spaces





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_space(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    space = db.query(models.Space).filter(models.Space.id == id)
    del_space = space.first()
    
    if del_space == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if del_space.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
        
    space.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Space)
def update_space(id: int, space: schemas.SpaceUpdate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #  cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))
    #  posts = cursor.fetchone()
    #  conn.commit()
     space_query = db.query(models.Space).filter(models.Space.id == id)
     spaces = space_query.first()
     if spaces == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
     if spaces.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

     space_query.update(space.dict(), synchronize_session=False)
     db.commit()
     return  space_query.first()
