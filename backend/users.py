from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
import logging
import traceback
from pydantic import BaseModel

from postgres_db import schemas
from postgres_db.database import get_db
from postgres_db import auth, models

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Password change schema
class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Attempting to create user: {user.username}")
        logger.debug(f"User data: chronic_condition={user.chronic_condition}, location={user.location}")
        
        # Check if user exists
        db_user = auth.get_user(db, username=user.username)
        if db_user:
            logger.warning(f"Username {user.username} already registered")
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Hash password
        logger.debug("Hashing password")
        hashed_password = auth.get_password_hash(user.password)
        
        # Create new user
        logger.debug("Creating new user in database")
        db_user = models.User(
            username=user.username, 
            password=hashed_password,
            chronic_condition=user.chronic_condition,
            location=user.location
        )
        
        # Add to database
        logger.debug("Adding user to database")
        db.add(db_user)
        
        # Commit changes
        logger.debug("Committing changes to database")
        db.commit()
        
        # Refresh to get the id
        logger.debug("Refreshing user object")
        db.refresh(db_user)
        
        logger.info(f"User {user.username} created successfully with id {db_user.id}")
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while creating user: {str(e)}"
        )

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Login attempt for user: {form_data.username}")
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug("Creating access token")
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        logger.info(f"User {form_data.username} logged in successfully")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during login: {str(e)}"
        )

@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user = Depends(auth.get_current_active_user)
):
    try:
        logger.debug(f"Getting user info for: {current_user.username}")
        return current_user
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving user info: {str(e)}"
        )

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Attempting to change password for user: {current_user.username}")
        
        # Verify current password
        if not auth.verify_password(password_data.current_password, current_user.password):
            logger.warning(f"Current password verification failed for user: {current_user.username}")
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Hash new password
        hashed_password = auth.get_password_hash(password_data.new_password)
        
        # Update user password in database
        current_user.password = hashed_password
        db.commit()
        
        logger.info(f"Password changed successfully for user: {current_user.username}")
        return {"detail": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while changing password: {str(e)}"
        )