from pydantic import HttpUrl
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, JSON, func, DateTime, Time, Date, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
# from enum import Enum as PyEnum



# class BookingType(str, PyEnum):   
#     TEMPORARY = "Temporary booking"
#     PERMANENT = "Permanent booking" 


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    phone_number = Column(String, nullable=False)
    
    spaces = relationship("Space", back_populates="owner", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    
    

class Space(Base):
    __tablename__ = "spaces"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name_of_space = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    type = Column(JSON, nullable=False)
    price_per_day = Column(DECIMAL(10, 2), nullable=False)
    price_per_week = Column(DECIMAL(10, 2), nullable=False)
    price_per_month = Column(DECIMAL(10, 2), nullable=False)
    # availability = Column(JSON, nullable=False)
    rules = Column(JSON, server_default=text("'{}'::jsonb"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # map_link = Column(String, nullable=True)
    
    amenities = relationship("SpaceAmenity", back_populates="space", cascade="all, delete")
    availabilities = relationship("SpaceAvailability", back_populates="space", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="space", cascade="all, delete-orphan")
 
    owner = relationship("User", back_populates="spaces")
    
    
class SpaceAmenity(Base):
    __tablename__ = "space_amenities"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
    amenity = Column(String, nullable=False)

    space = relationship("Space", back_populates="amenities")
    



# class SpaceImage(Base):
#     __tablename__ = "space_images"

#     id = Column(Integer, primary_key=True, index=True)
#     space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
#     image_url = Column(Text, nullable=False)
#     image_order = Column(Integer)

#     space = relationship("Space", back_populates="images")
    
class SpaceAvailability(Base):
    __tablename__ = "space_availabilities"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    space = relationship("Space", back_populates="availabilities")






class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    # booking_type = Column(Enum(BookingType, name="booking_types"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    space = relationship("Space", back_populates="bookings")
    user = relationship("User", back_populates="bookings")

    
    
    
    
    


# class Space(Base):
#     __tablename__ = "spaces"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     name = Column(String, index=True)

#     __table_args__ = (
#         UniqueConstraint("user_id", "name", name="_user_space_uc"),
#     )
