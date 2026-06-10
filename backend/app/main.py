from fastapi import FastAPI
from app.database.db import engine, Base
from app.models.user import User
from app.auth.hashing import hash_password
from app.routes.auth import router as auth_router
from app.models.note import Note
from app.routes.notes import router as notes_router
from app.models.task import Task
from app.routes.tasks import router as tasks_router
from app.models.document import Document
from app.routes.documents import router as documents_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

app.include_router(notes_router, prefix="/notes", tags=["Notes"])

app.include_router(tasks_router,prefix="/tasks",tags=["Tasks"])

app.include_router(documents_router,prefix="/documents",tags=["Documents"])

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


