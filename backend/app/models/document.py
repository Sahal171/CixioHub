from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database.db import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    filepath = Column(String)

    size = Column(Integer)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )