from pydantic import BaseModel

import datetime


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    bio: str
    created_at: datetime.datetime
    updated_at: datetime.datetime