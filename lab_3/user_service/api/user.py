from database import get_db
from db_models import User
from fastapi import APIRouter, Depends, HTTPException, Response
from schemas.auth import AuthResponse
from schemas.user import SearchUser, UserBase, UserCreate
from sqlalchemy import or_
from sqlalchemy.orm import Session
from utils import PasswordEngine, TokenEngine

from .token_utils import get_current_user

router = APIRouter()


@router.post(
    '/register',
    summary='Register new user',
    response_model=AuthResponse,
    responses={409: {'description': 'User already exists'}},
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == user.login).first()
    if existing_user:
        raise HTTPException(status_code=409, detail='User already exists')
    user.password = PasswordEngine.hash_password(user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    access_token = TokenEngine.create_access_token(user.login)
    return AuthResponse(access_token=access_token, token_type='bearer')


@router.get(
    '/info',
    summary='Get information about current user',
    response_model=UserBase,
    responses={401: {}, 404: {'description': 'User wasn`t found'}},
)
async def get_user_info(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == current_user).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail='User wasn`t found')
    return existing_user


@router.get('/list', summary='Get list of users', response_model=list[UserBase], responses={401: {}})
async def get_user_list(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.query(User).all())


@router.delete(
    '/delete',
    summary='Delete current user',
    response_class=Response,
    responses={401: {}, 404: {'description': 'User wasn`t found'}},
)
async def delete_user(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == current_user).first()
    if not existing_user:
        return HTTPException(status_code=404, detail='User wasn`t found')
    db.delete(existing_user)
    db.commit()
    return Response(status_code=200)


@router.post('/search', summary='Search user', response_model=list[UserBase])
async def search_user(searching: SearchUser, db: Session = Depends(get_db)):
    return (
        db.query(User).filter(or_(*[getattr(User, field).op('~')(searching.value) for field in searching.fields])).all()
    )
