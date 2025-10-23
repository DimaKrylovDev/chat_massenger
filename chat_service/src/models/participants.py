from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import ForeignKey
from sdk.enums.user_type import UserType

class Participants(Base):
    __tablename__ = "participants"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_type: Mapped[UserType] = mapped_column(nullable=False, default=UserType.USER)