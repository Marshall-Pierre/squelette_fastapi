from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy import update, func
import random
import string

from ..Db.Model import UserModel
from ..Schema import UserSchema
from core.config import settings


################################### Read Function #####################################################################
async def get_by_user_code(db: Session, user_code: str):
    user = db.query(UserModel.User).filter(UserModel.User.user_code == user_code).first()
    if user is not None:
        return UserSchema.Read(**vars(user))


async def get_all(db: Session):
    return db.query(UserModel.User).all()


################################### Add Function #####################################################################
async def add(db: Session, user: UserSchema.Create):
    user_code = generate_user_code(lastname=user.lastname, firstname=user.firstname)
    verif_user = await get_by_user_code(db=db, user_code=user_code)
    if verif_user:
        raise HTTPException(status_code=400, detail="Code déjà existant")

    clear_password = generate_password()
    db_user = UserModel.User(
        user_code=user_code,
        firstname=user.firstname,
        lastname=user.lastname,
        phone_number=user.phone_number,
        email=user.email,
        role=user.role,
        password=hash_password(clear_password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


################################### Update Function #####################################################################
async def update_password(db: Session, password: str, current_user: UserSchema.Read):
    query = update(UserModel.User).where(UserModel.User.user_code == current_user.user_code).values(
        password=hash_password(password),
        password_is_change=True,
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()
    return {"msg": "Mot de passe changé avec succès"}


################################### Function #####################################################################
def generate_user_code(lastname: str, firstname: str):
    lastname_group = lastname.split()
    first_lastname = lastname_group[0].upper()
    code_user = f"{first_lastname}.{firstname[0].capitalize()}"
    return code_user


def hash_password(password):
    return settings.pwd_context.hash(password)


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    clear_password = ''.join(random.choice(characters) for _ in range(7))
    return clear_password
