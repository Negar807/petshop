import os


class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/petshop_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False