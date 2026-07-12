import os

os.environ.setdefault("APP_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
os.environ.setdefault("APP_ENVIRONMENT", "test")
os.environ.setdefault("APP_ALLOWED_HOSTS", "localhost,testserver")
