from models.user import User
from sdk.repositories.base import BaseRepository

class AuthRepository(BaseRepository):
    model = User

    