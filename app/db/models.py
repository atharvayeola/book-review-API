from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    reviews: List["Review"] = Relationship(back_populates="user")

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    description: Optional[str] = None

    reviews: List["Review"] = Relationship(back_populates="book")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    rating: int = Field(ge=1, le=5)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")

    user: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")
