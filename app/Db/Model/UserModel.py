from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..Connection import Base


# TODO: Création de la table user
class User(Base):
    __tablename__ = "users"

    user_code = Column(String, primary_key=True, unique=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(String)
    email = Column(String)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    password_is_change = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
