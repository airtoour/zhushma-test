from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.core.db import Users


class UsersService(SQLAlchemyAsyncRepositoryService[Users]):  # type: ignore
    """Сервис Users"""

    class UsersRepository(SQLAlchemyAsyncRepository[Users]):
        """Репозиторий Users"""
        model_type = Users

    repository_type = UsersRepository
