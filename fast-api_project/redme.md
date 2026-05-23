# 🚀 FastAPI CRUD Project

A clean, production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. This project follows best practices with a well-organized file structure that separates concerns clearly.

---

## 📁 Project Structure

```
fastapi_project/
├── main.py             # App entry point
├── database.py         # DB engine & session setup
├── models.py           # SQLAlchemy table definitions
├── crud.py             # All database operations
├── schemas.py          # Pydantic request/response models
├── dependencies.py     # Reusable FastAPI dependencies
├── config.py           # App settings & environment config
├── utils.py            # Helper/utility functions
├── requirements.txt    # Python package dependencies
└── routers/
    ├── __init__.py
    └── items.py        # HTTP route handlers
```

---

## 📄 File-by-File Explanation

---

### 1. `main.py` — App Entry Point

This is the **starting point** of the entire application.

**What it does:**
- Creates the FastAPI app instance with a title and description
- Calls `Base.metadata.create_all()` to auto-create database tables on startup
- Registers the `items` router under the `/items` URL prefix
- Defines a simple root `GET /` endpoint to confirm the API is running

**Think of it as:** The front door of the building — everything starts here.

```python
app = FastAPI(title="FastAPI CRUD App")
app.include_router(items.router, prefix="/items", tags=["Items"])
```

---

### 2. `database.py` — Database Connection

This file sets up the **connection to the database**.

**What it does:**
- Creates a SQLAlchemy `engine` that connects to the database (SQLite by default)
- Creates a `SessionLocal` factory — each request gets its own DB session
- Defines `Base` — the parent class that all ORM models inherit from

**Think of it as:** The plumbing — it connects your app to the actual database.

```python
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

---

### 3. `models.py` — Database Table Definition

This file defines **what your database tables look like**.

**What it does:**
- Defines the `Item` class that maps to the `items` table in the database
- Each class attribute = one column in the table
- Includes fields: `id`, `title`, `description`, `is_active`, `created_at`, `updated_at`
- SQLAlchemy uses this model to create and query the actual database table

**Think of it as:** The blueprint of your database table.

```python
class Item(Base):
    __tablename__ = "items"
    id    = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
```

---

### 4. `crud.py` — Database Operations

This file contains all **Create, Read, Update, Delete (CRUD)** logic.

**What it does:**
- `get_item()` — fetches a single item by ID
- `get_items()` — fetches a paginated list of all items
- `create_item()` — inserts a new item into the database
- `update_item()` — updates an existing item's fields
- `delete_item()` — removes an item from the database

**Think of it as:** The hands that actually touch the database — all DB logic lives here and nowhere else.

```python
def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    return db_item
```

---

### 5. `schemas.py` — Pydantic Models (Validation)

This file defines **what data looks like going in and coming out** of the API.

**What it does:**
- `ItemBase` — shared fields used by create and response models
- `ItemCreate` — schema for creating a new item (what the user sends in the request body)
- `ItemUpdate` — schema for updating an item (all fields are optional)
- `ItemResponse` — schema for what the API sends back (includes `id`, `created_at`, etc.)
- Pydantic **automatically validates** incoming data and raises errors if it's wrong

**Think of it as:** The security guard at the door — it checks that all data is correct before it enters or leaves.

```python
class ItemCreate(ItemBase):
    pass  # Inherits title, description, is_active

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True  # Allows reading SQLAlchemy objects
```

---

### 6. `dependencies.py` — Shared Dependencies

This file provides **reusable building blocks** that routes can plug into.

**What it does:**
- Defines `get_db()` — a generator function that opens a DB session for a request and closes it automatically after
- This is injected into route functions using FastAPI's `Depends()` system
- Ensures every request gets a fresh DB session and it's properly closed (even on errors)

**Think of it as:** A vending machine — route handlers ask for a DB session, this file gives it to them and cleans up after.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # Give the session to the route
    finally:
        db.close()    # Always close it when done
```

---

### 7. `config.py` — App Settings

This file manages all **configuration and environment variables**.

**What it does:**
- Uses Pydantic's `BaseSettings` to define app-wide settings
- Reads values from a `.env` file automatically (if present)
- Stores things like `DATABASE_URL`, `SECRET_KEY`, `DEBUG` mode, `API_PREFIX`
- A single `settings` object is imported across the whole app

**Think of it as:** The control panel — change one value here and it affects the whole app.

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str   = "change-this-in-production"
    class Config:
        env_file = ".env"
```

---

### 8. `routers/items.py` — HTTP Route Handlers

This file defines all the **API endpoints** for the Items resource.

**What it does:**
- `GET /items/` — returns a list of all items (with pagination)
- `GET /items/{id}` — returns a single item by ID
- `POST /items/` — creates a new item
- `PUT /items/{id}` — updates an existing item
- `DELETE /items/{id}` — deletes an item
- Each route calls the appropriate function from `crud.py`
- Uses `Depends(get_db)` to get a DB session automatically

**Think of it as:** The receptionist — it receives HTTP requests and forwards them to the right department (crud.py).

```python
@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)
```

---

### 9. `utils.py` — Helper Utilities

This file contains **reusable helper functions** used across the app.

**What it does:**
- `success_response()` — wraps data in a standard success envelope with a timestamp
- `error_response()` — wraps error messages in a standard format
- `paginate()` — calculates pagination metadata (total pages, current offset, etc.)
- Keeps the codebase DRY (Don't Repeat Yourself)

**Think of it as:** A toolbox — small, general-purpose tools that any part of the app can use.

```python
def success_response(data, message="Success"):
    return {"status": "success", "data": data, "timestamp": ...}
```

---

### 10. `requirements.txt` — Dependencies

This file lists all **Python packages** the project needs.

**What it does:**
- `fastapi` — the web framework
- `uvicorn` — the ASGI server that runs FastAPI
- `sqlalchemy` — the ORM for database interaction
- `pydantic` — data validation library
- `pydantic-settings` — for loading settings from `.env` files
- `python-dotenv` — reads `.env` files

**Think of it as:** The shopping list — run `pip install -r requirements.txt` and you get everything you need.

---

## 🔄 How All Files Work Together

```
HTTP Request
    │
    ▼
routers/items.py        ← Receives the request, validates URL/method
    │
    ├── schemas.py      ← Validates & parses the request body (Pydantic)
    ├── dependencies.py ← Provides a DB session via Depends(get_db)
    │
    ▼
crud.py                 ← Runs the actual database query
    │
    ├── models.py       ← Defines the DB table structure (SQLAlchemy)
    ├── database.py     ← Manages the DB connection/engine
    │
    ▼
schemas.py              ← Serializes the response back to JSON
    │
    ▼
HTTP Response
```

---

## ▶️ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Create a .env file
echo "DATABASE_URL=sqlite:///./app.db" > .env

# 3. Start the server
uvicorn main:app --reload
```

---

## 📖 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Health check |
| GET | `/items/` | Get all items (paginated) |
| GET | `/items/{id}` | Get a single item |
| POST | `/items/` | Create a new item |
| PUT | `/items/{id}` | Update an item |
| DELETE | `/items/{id}` | Delete an item |

---

## 🌐 Swagger UI

After running the server, open your browser at:

```
http://localhost:8000/docs
```

FastAPI auto-generates an interactive API documentation page where you can test all endpoints directly.

---

## 🧠 Key Concepts Used

| Concept | Where Used | Purpose |
|---------|-----------|---------|
| ORM (SQLAlchemy) | `models.py`, `crud.py` | Talk to DB using Python classes |
| Pydantic Validation | `schemas.py` | Validate request/response data |
| Dependency Injection | `dependencies.py` | Share DB sessions across routes |
| Environment Config | `config.py` | Manage settings via `.env` |
| Router Separation | `routers/items.py` | Keep routes organized by resource |

---

*Built with FastAPI — the modern, fast web framework for building APIs with Python.*