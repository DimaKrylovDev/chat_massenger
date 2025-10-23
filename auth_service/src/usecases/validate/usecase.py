from usecases.validate.request import ValidateTokenRequest
from usecases.validate.response import ValidateTokenResponse
from core.dependencies import get_auth_repository
from core.settings import settings
from jose import jwt


class ValidateTokenUsecase:
    def __init__(self):
        self.auth_repository = get_auth_repository()

    async def __call__(self, request: ValidateTokenRequest) -> ValidateTokenResponse:

        payload = jwt.decode(
            request.access_token,
            settings.EE_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        user_id = payload.get("user_id")

        if not user_id:
            return ValidateTokenResponse(
                valid=False,
                user_id=None,
                error_message="Invalid token"
            )
        exp = payload.get("exp")

        if exp == 0:
            return ValidateTokenResponse(
                valid=False,
                user_id=None,
                error_message="Token expired"
            )
            
        return ValidateTokenResponse(
            valid=True,
            user_id=user_id,
            error_message=""
        )



