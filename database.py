from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine("postgresql://postgres:7982@localhost:5432/savdo", echo=True)
Base = declarative_base()
Session = sessionmaker()