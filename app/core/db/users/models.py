from advanced_alchemy.base import BigIntAuditBase
from advanced_alchemy.types import PasswordHash
from advanced_alchemy.types.password_hash.pwdlib import PwdlibHasher

from pwdlib.hashers.argon2 import Argon2Hasher as PwdlibArgon2Hasher

from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column


class Users(BigIntAuditBase):
    """Модель таблицы users (Пользователи)"""
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(128), index=True)
    surname: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(
        PasswordHash(
            backend=PwdlibHasher(hasher=PwdlibArgon2Hasher())
        )
    )

    idx_users_name = Index("idx_users_name", name)
