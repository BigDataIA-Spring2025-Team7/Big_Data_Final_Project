from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    chronic_condition = Column(String)
    location = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Use server_default for created_at to ensure it works with PostgreSQL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # updated_at can be nullable since it will only be set when records are updated
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)