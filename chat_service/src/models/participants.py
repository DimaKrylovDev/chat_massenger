from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
import uuid
import datetime
from sqlalchemy import ForeignKey

class Participants(Base):
    __tablename__ = "participants"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    added_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())