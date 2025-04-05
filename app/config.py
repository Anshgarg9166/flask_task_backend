# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Ansh9166@localhost:5432/task_db")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False



import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Ansh9166@localhost:5432/task_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"  # Change this in production
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
