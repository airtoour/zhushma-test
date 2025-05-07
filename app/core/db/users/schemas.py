from typing import Optional
from datetime import datetime
from msgspec import Struct


class UsersCreate(Struct):
    """Схема создания пользователя"""
    name: str
    surname: str
    password: str


class UsersUpdate(Struct):
    """Схема обновления пользователя"""
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

    def serialize(self):
        """Метод сериализации полученных данных на обновление"""
        data = {
            "name": self.name,
            "surname": self.surname,
            "password": self.password,
        }
        return {k: v for k, v in data.items() if v is not None}


class UsersRead(Struct):
    """Схема чтения пользователя"""
    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime
