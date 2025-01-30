from sqlalchemy import create_engine , Column , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:dishu21@localhost:5432/diet_db"

engine =  create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
Base.metadata.create_all(engine) 