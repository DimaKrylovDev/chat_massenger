from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
import uuid
import datetime
from sqlalchemy import ForeignKey

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    chat_name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())