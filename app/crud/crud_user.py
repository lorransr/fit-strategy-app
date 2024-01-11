from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.db.base_class import Base
from app.crud import base

ModelType = TypeVar("ModelType", bound=Base)


def get(db: Session, id: Any) -> Optional[User]:
    return base.get(db=db, model=User, id=id)


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return base.get_multi(db=db, skip=skip, limit=limit, model=User)


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, *, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        is_superuser=obj_in.is_superuser,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    return base.update(db, db_obj=db_obj, obj_in=update_data)


def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    return user.is_active


def is_superuser(user: User) -> bool:
    return user.is_superuser
