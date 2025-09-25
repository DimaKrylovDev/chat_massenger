from sdk.repositories.auth import AuthRepository
from sdk.repositories.session import SessionRepository


def get_auth_repository():
    return AuthRepository()

def get_session_repository():
    return SessionRepository()