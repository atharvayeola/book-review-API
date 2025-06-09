from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import database, models
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(database.get_session)):
    if db.get(models.User, user_in.username):
        raise HTTPException(400, "Username taken")
    user = models.User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    db.add(user); db.commit(); db.refresh(user)
    return user
