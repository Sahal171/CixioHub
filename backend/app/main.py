from fastapi import FastAPI
from app.database.db import engine, Base
from app.models.user import User
from app.auth.hashing import hash_password
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "CixioHub Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-hash/{password}")
def test_hash(password:str):
    return {
        "hashed": hash_password(password)
    }