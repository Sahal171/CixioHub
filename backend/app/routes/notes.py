from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.note import Note
from app.schemas.note_schema import NoteCreate
from app.auth.jwt_handler import get_current_user

from sqlalchemy import or_

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    new_note = Note(
        title=note.title,
        content=note.content,
        tags=note.tags,
        owner_id=current_user.id
    )

    db.add(new_note)

    db.commit()

    db.refresh(new_note)

    return {
        "message": "Note created successfully",
        "note": new_note
    }

#Getting All notes
@router.get("/")
def get_notes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).all()

    return notes

#Searching
@router.get("/search")
def search_notes(
    keyword: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notes = db.query(Note).filter(
        Note.owner_id == current_user.id,
        or_(
            Note.title.contains(keyword),
    Note.tags.contains(keyword)
        )
    ).all()
    return notes

#GET Note by id
@router.get("/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note

#Updating the Note by note_id
@router.put("/{note_id}")
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()
    db.refresh(note)

    return {
        "message": "Note updated successfully",
        "note": note
    }

#Deleting note by note_id
@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)

    db.commit()

    return {
        "message": "Note deleted successfully"
    }

