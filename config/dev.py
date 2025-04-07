import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
