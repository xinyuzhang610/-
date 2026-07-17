from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from config import settings
import os

# Detect Vercel serverless environment
_is_serverless = os.environ.get('VERCEL', False)

# Configure engine based on environment
if _is_serverless:
    # Serverless: use NullPool to avoid connection leaks across invocations
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        poolclass=NullPool,
        connect_args={"ssl": {"ca": "/etc/ssl/certs/ca-certificates.crt"}} if "mysql" in settings.DATABASE_URL else {}
    )
else:
    # Local development: use standard connection pool
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()