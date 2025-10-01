from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

import uuid
import datetime
from sqlalchemy import ForeignKey

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    content: Mapped[str] = mapped_column(nullable=False)
    message_type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())