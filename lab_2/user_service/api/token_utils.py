from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils import TokenEngine

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    if (user := TokenEngine.get_user_from_token(token)) is None:
        raise credentials_exception
    return user
