from fastapi import APIRouter, Depends

from core.security import JWTGetter
from core.settings import settings
from schemas.token import Token
from usecases.login.request import LoginRequest
from usecases.login.usecase import LoginUsecase
from usecases.logout.request import LogoutRequest
from usecases.logout.usecase import LogoutUsecase
from usecases.logout.response import LogoutResponse
from usecases.refresh.request import RefreshRequest
from usecases.refresh.usecase import RefreshUsecase
from usecases.signup.request import SignUpRequest
from usecases.signup.usecase import SignUpUsecase

jwt_getter = JWTGetter(settings.EE_SECRET_KEY)

router = APIRouter(prefix="/auth")

tags_metadata = [
    {
        "name": "Auth",
        "description": "User auth methods",
    }
]


@router.post("/signup", tags=["Auth"])
async def signup(request: SignUpRequest):
    usecase = SignUpUsecase()
    response = await usecase(request)
    return response

@router.post("/login", tags=["Auth"])
async def login(request: LoginRequest):
    usecase = LoginUsecase()
    response = await usecase(request)
    return response

@router.post("/refresh", tags=["Auth"])
async def refresh(token: Token = Depends(jwt_getter)):
    request = RefreshRequest(token=token)
    usecase = RefreshUsecase()
    response = await usecase(request)
    return response

@router.post("/logout", tags=["Auth"])
async def logout(token: Token = Depends(jwt_getter)):
    request = LogoutRequest(token=token)
    usecase = LogoutUsecase()
    response = await usecase(request)
    return response
