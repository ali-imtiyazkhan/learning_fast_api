from database import SessionLocal

def get_db():
    """
    Yields a DB session and ensures it closes after each request.
    Inject this using FastAPI's Depends().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
