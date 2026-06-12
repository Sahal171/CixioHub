from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.auth.jwt_handler import get_current_admin

router = APIRouter()

@router.get("/users")
def get_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

@router.get("/admin-test")
def admin_test(
    admin: User = Depends(get_current_admin)
):
    return {
        "message": "Welcome Admin"
    }

@router.get("/pending-users")
def get_pending_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    users = db.query(User).filter(
        User.status == "pending"
    ).all()

    return users

@router.put("/approve/{user_id}")
def approve_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.status = "approved"

    db.commit()
    db.refresh(user)

    return {
        "message": f"{user.email} approved successfully"
    }