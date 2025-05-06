from datetime import datetime
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from core.db import (
    Users,
    UsersRepository,
    UsersUpdate,
    UsersCreate
)
from core.logger import logger


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    async def list(self, *filters) -> List[Users]:
        """Метод получения всех пользователей из таблицы Users"""
        try:
            return self.repository.list(*filters)
        except (SQLAlchemyError, Exception) as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    async def get(self, user_id: int) -> Users:
        """Получение пользователя по ID"""
        try:
            return self.repository.get(user_id)
        except (SQLAlchemyError, Exception) as e:
            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")
            raise

    async def add(self, data: UsersCreate) -> Users:
        """Метод добавления пользователя в таблицу Users"""
        try:
            return self.repository.add(
                Users(
                    name=data.name,
                    surname=data.surname,
                    password=data.password,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
                auto_refresh=True
            )
        except (SQLAlchemyError, Exception) as e:
            await self.repository.session.rollback()

            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")

            raise

    async def update(self, user_id: int, data: UsersUpdate) -> Users:
        """Обновление пользователя в таблице Users"""
        try:
            user = await self.get(user_id)

            for field, value in data.__dict__.items():
                if value is not None:
                    setattr(user, field, value)

            user.updated_at = datetime.now()
            return await self.repository.update(user, auto_refresh=True)
        except (SQLAlchemyError, Exception) as e:
            await self.repository.session.rollback()

            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")

            raise

    async def delete(self, user_id: int) -> None:
        """Удаление пользователя из таблицы Users"""
        try:
            user = await self.get(user_id)
            await self.repository.delete(user)
        except (SQLAlchemyError, Exception) as e:
            await self.repository.session.rollback()

            error_message = "Database" if isinstance(e, SQLAlchemyError) else "Other"
            logger.error(error_message + f"Error:\n{e}")

            raise