from pydantic import BaseModel, conint
from datetime import datetime

class ReviewCreate(BaseModel):
    book_id: int
    content: str
    rating: conint(ge=1, le=5)

class ReviewRead(ReviewCreate):
    id: int
    user_id: int
    created_at: datetime
