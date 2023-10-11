from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from ..Controller import UserController
from ..Middleware.DatabaseSession import get_db
from ..Schema import TokenSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Vous n'êtes pas autorisé à effectuer cette action",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_code: str = payload.get("user_code")
        if user_code is None:
            raise credentials_exception
        token_data = TokenSchema.TokenData(username=user_code)
    except JWTError:
        raise credentials_exception
    user = await UserController.get_by_user_code(db=db, user_code=token_data.username)
    if user is None:
        raise credentials_exception
    return user
