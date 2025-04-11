import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt


class TokenEngine:
    SECRET_KEY = os.environ.get('TOKEN_SECRET_KEY', 'ojgoRcVBL0VmN+hg1SuKhfX/f5BpsreC9OfuJGLLXgdyICY3mdwUEyXnMWJ9ohzE')
    TTL = int(os.environ.get('TOKEN_TTL_MINUTES', '60'))
    ALGORITHM = 'HS256'

    @staticmethod
    def create_access_token(login: str):
        data = {'login': login, 'exp': datetime.utcnow() + timedelta(minutes=TokenEngine.TTL)}
        return jwt.encode(data, TokenEngine.SECRET_KEY, algorithm=TokenEngine.ALGORITHM)

    @staticmethod
    def get_user_from_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, TokenEngine.SECRET_KEY, algorithms=[TokenEngine.ALGORITHM])
            if payload['exp'] < datetime.utcnow().timestamp():
                return None
            return payload['login']
        except JWTError:
            return None
