# app/routers/reviews.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.database import get_session
from app.db.models import Review, User
from app.schemas.review import ReviewCreate, ReviewRead
from app.core.security import verify_token

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewRead])
def list_reviews(db: Session = Depends(get_session)):
    return db.exec(select(Review)).all()


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_session)):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post(
    "/",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    review_in: ReviewCreate,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    review = Review.from_orm(review_in)
    review.user_id = user.id
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_in: ReviewCreate,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # ensure only author can update
    user = db.exec(select(User).where(User.username == username)).first()
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")

    review.content = review_in.content
    review.rating = review_in.rating
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    username: str = Depends(verify_token),  # auth required
    db: Session = Depends(get_session),
):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # ensure only author can delete
    user = db.exec(select(User).where(User.username == username)).first()
    if review.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    db.delete(review)
    db.commit()
    return None
