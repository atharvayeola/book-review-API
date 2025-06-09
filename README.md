# Book Review API

A simple RESTful service for managing users, books and reviews.  
Built with FastAPI, SQLModel, SQLite, and JWT-based authentication.

---

## Features

- **User registration & authentication**  
- **JWT tokens** for stateless, secure access  
- **CRUD operations** for books and reviews  
- **Role enforcement**: only authors can edit/delete their own reviews  
- **Auto-generated API docs** via Swagger UI and ReDoc  

---

## Tech Stack

- **FastAPI** — high-performance web framework  
- **SQLModel** — ORM + Pydantic models  
- **SQLite** — lightweight file-based database  
- **python-jose** — JWT creation & validation  
- **Passlib (bcrypt)** — password hashing  
- **python-dotenv** — environment variable loader  
- **Uvicorn** — ASGI server  

---

## Repository Structure

```book-review-api/
├── app/
│ ├── core/ ← configuration & security helpers
│ ├── db/ ← database engine & models
│ ├── routers/ ← route handlers by resource
│ ├── schemas/ ← Pydantic request/response schemas
│ └── main.py ← application entrypoint
├── .env ← SECRET_KEY and other env vars
├── requirements.txt
└── README.md
```


---

## Prerequisites

- Python 3.9+  
- Git (optional, to clone the repo)  

---

## Quick Start

1. **Clone & enter project**  
   ```
   git clone https://github.com/your-username/book-review-api.git
   cd book-review-api
  
2. **Create & activate virtual environment**

```
python3 -m venv env-book-review
source env-book-review/bin/activate     # macOS/Linux
.\env-book-review\Scripts\activate.bat  # Windows
```
3. **Install dependencies**

```
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a UTF-8 .env file in project root:
```
SECRET_KEY=your_super_secret_key_here
```
5. **Initialize the database**

``` 
python -c "from app.db.database import init_db; init_db()"
```

6. **Run the server**
```
uvicorn app.main:app --reload
```

*Usage Examples*
-> Register a user
```
POST /users/
{
  "username": "alice",
  "password": "password123"
}
```

-> Obtain a token
```
POST /auth/token
form-data: username=alice, password=password123
→ { "access_token": "...", "token_type": "bearer" }
```

-> Create a book (authenticated)
```
POST /books/
Authorization: Bearer <token>
{
  "title": "1984",
  "author": "George Orwell",
  "description": "Dystopian classic"
}
```
-> Create a review (authenticated)
```
POST /reviews/
Authorization: Bearer <token>
{
  "book_id": 1,
  "content": "A haunting vision of the future.",
  "rating": 5
}
```
