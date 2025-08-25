from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas
from ..database import get_db

    
router = APIRouter(
    prefix = "/booking",
    tags=['booking']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookingBase)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # new_booking= models.Booking(user_id = current_user.id, **booking.dict())
    
    space =  db.query(models.Space).filter(models.Space.id == booking.space_id).first()
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    
    
    new_booking = models.Booking(
        **booking.dict(),
        user_id=current_user.id,
        # booking_type=booking.booking_type.value 
    )
    

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking



@router.get("/", response_model=List[schemas.BookingOut])
def get_all_bookings(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
               limit: int = 15000, skip: int = 0, search: Optional[str] = ""):
    get_all_bookings = db.query(models.Booking).filter(models.Space.name_of_space.contains(search)).limit(limit).offset(skip).all()
    return get_all_bookings


@router.get("/my-booking", response_model=List[schemas.BookingOut])
def get_user_booking(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 15000,skip: int = 0,search: Optional[str] = ""):
    user_booking = db.query(models.Booking).filter(models.Booking.user_id == current_user.id).filter(
        models.Space.name_of_space.contains(search)).limit(limit).offset(skip).all()
    return user_booking


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_space(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == id)
    del_booking = booking.first()
    
    if del_booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if del_booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
        
    booking.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
@router.put("/{id}", response_model=schemas.BookingBase)
def update_booking(id: int, booking: schemas.BookingBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
     booking_query = db.query(models.Booking).filter(models.Booking.id == id)
     book = booking_query.first()
     if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Booking with id: {id} does not exist")
     if book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

     booking_query.update(booking.dict(), synchronize_session=False)
     db.commit()
     return  booking_query.first()

    