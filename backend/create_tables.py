# backend/create_tables.py
from app.db.database import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")