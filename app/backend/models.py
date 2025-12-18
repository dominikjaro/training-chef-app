from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    weight_kg = Column(Float, nullable=True)
    ftp = Column(Integer, nullable=True)
    height_cm = Column(Integer, nullable=True)
    body_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
