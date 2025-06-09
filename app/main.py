from fastapi import FastAPI
from app.db.database import init_db
from app.routers import auth, users, books, reviews

app = FastAPI(title="Book Review API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(reviews.router)
