# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.database import get_session
from app.db.models import Book
from app.schemas.book import BookCreate, BookRead
from app.core.security import verify_token

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
def list_books(db: Session = Depends(get_session)):
    return db.exec(select(Book)).all()


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_session)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post(
    "/",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book_in: BookCreate,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    book = Book.from_orm(book_in)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_in: BookCreate,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_in.title
    book.author = book_in.author
    book.description = book_in.description
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
