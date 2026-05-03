import bcrypt

from .auth_repository import AuthRepository
from .auth_exceptions import *
from .jwt_helper import generate_access_token
from .auth_models import LoginAuthModel

from ..users.users_models import UserCreateModel
from ..users.users_service import UsersService
from ..users.users_exceptions import NotFoundError

class AuthService():

    def __init__(self, repo: AuthRepository, users_service: UsersService):
        self.__repo = repo
        self.__users_service = users_service

    async def register_user_async(self, user: UserCreateModel) -> str:
        same_user_name = None
        same_email = None

        try:
            same_user_name = await self.__users_service.get_user_by_username(user.user_name)
        except NotFoundError:
            same_user_name = None

        try:
            same_email = await self.__users_service.get_user_by_email(user.email)
        except NotFoundError:
            same_email = None

        if same_user_name != None:
            raise UserNameAlreadyExistsError()
        
        if(same_email != None):
            raise EmailAlreadyExistsError()

        user.password = self.__hash_password(user.password)

        new_user = await self.__repo.save_user_async(user)

        access_token = generate_access_token({
            "sub": new_user.user_name,
            "id": new_user.id
        })

        return access_token
    
    async def login_user_async(self, user: LoginAuthModel) -> str:
        user_from_db = await self.__repo.find_user_for_login(user.username)

        if not user_from_db:
            raise CredentialsDontMatchError()

        isVerified = self.__verify_password(user.password, user_from_db.password)

        if not isVerified:
            raise CredentialsDontMatchError()
        
        access_token = generate_access_token({
            "sub": user_from_db.user_name,
            "id": user_from_db.id
        })

        return access_token 
    
    def __hash_password(self, password: str) -> str:
        encoded_password = password.encode('utf-8')
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(encoded_password, salt)

        return hashed_password.decode('utf-8')
    
    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        plain_password_encoded = plain_password.encode('utf-8')
        hashed_password_encoded = hashed_password.encode('utf-8')

        return bcrypt.checkpw(plain_password_encoded, hashed_password_encoded)