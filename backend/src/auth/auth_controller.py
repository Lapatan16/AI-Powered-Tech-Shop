from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from .auth_dependencies import get_auth_service
from .auth_service import AuthService
from .auth_exceptions import EmailAlreadyExistsError, UserNameAlreadyExistsError, CredentialsDontMatchError
from .auth_models import AccessTokenResponseModel, LoginAuthModel
from ..users.users_models import UserCreateModel

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@router.post(
    "/register",
    response_model=AccessTokenResponseModel,
    status_code=status.HTTP_201_CREATED
)
async def register(
    request: UserCreateModel,
    auth_service: AuthServiceDependency
) -> AccessTokenResponseModel:
    try:
        access_token = await auth_service.register_user_async(request)

        return AccessTokenResponseModel(access_token=str(access_token))
    except UserNameAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, {
            "error": "user_name is already taken."
        })
    except EmailAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, {
            "error": "email is already taken."
        })
    
@router.post(
    "/login",
    response_model=AccessTokenResponseModel,
    status_code=status.HTTP_200_OK
)
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDependency
) -> AccessTokenResponseModel:
    try:
        login_data = LoginAuthModel(username=request.username, password=request.password)
        access_token = await auth_service.login_user_async(login_data)

        return AccessTokenResponseModel(access_token=str(access_token))
    except CredentialsDontMatchError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, {
            "error": "credentials don't match."
        })