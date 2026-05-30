from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.auth.jwt_handler import get_current_user

import os
import shutil

from app.models.document import Document

router = APIRouter()

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata to database
    new_document = Document(
        filename=file.filename,
        filepath=file_path,
        size=os.path.getsize(file_path),
        user_id=current_user.id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "File uploaded successfully",
        "document_id": new_document.id,
        "filename": new_document.filename
    }

@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()

    return documents

from fastapi import HTTPException

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }