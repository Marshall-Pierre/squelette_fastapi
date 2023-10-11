from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import UserController
from ..Schema import UserSchema

router = APIRouter()


@router.get("/all", tags=["Utilisateurs"], response_model=list[UserSchema.Read])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.get_all(db)


@router.post("/add", tags=["Utilisateurs"], response_model=UserSchema.Read, status_code=status.HTTP_201_CREATED)
async def add(
        user: UserSchema.Create,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.add(db=db, user=user)


@router.put("/update_password", tags=["Utilisateurs"])
async def update_password(
        password,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.update_password(db=db, current_user=current_user, password=password)
