from schemas.auth.token import Token
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

oauth2_scheme = HTTPBearer(auto_error=False)

class JWTGetter:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def __call__(self, token: HTTPAuthorizationCredentials | None= Depends(oauth2_scheme)) -> Token:
        try:
            token_data = jwt.decode(token.credentials, self.secret_key, algorithms=["HS256"])
            return Token(**token_data, jwt_string=token.credentials)
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Unauthorized")

