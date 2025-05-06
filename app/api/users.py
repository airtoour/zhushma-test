from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from core.db import UsersRepository, UsersCreate, UsersRead, UsersUpdate
from core.services.users import UsersService

from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from litestar.params import Parameter

from sqlalchemy.ext.asyncio import AsyncSession


class UsersController(Controller):
    path = "/users"

    dependencies = {
        "repository": Provide(lambda db_session: UsersRepository(db_session)),
        "service": Provide(lambda repository: UsersService(repository)),
    }

    @post("/add", summary="Создать пользователя")
    async def create_user(self, data: UsersCreate, service: UsersService) -> UsersRead:
        new_user = await service.add(data)
        return UsersRead(**new_user.__dict__)

    @get("/", summary="Список пользователей")
    async def list_users(self, service: UsersService) -> list[UsersRead]:
        return [UsersRead(**u.__dict__) for u in await service.list()]

    @get("/{user_id:int}", summary="Получить пользователя")
    async def get_user(self, user_id: int, service: UsersService) -> UsersRead:
        user = await service.get(user_id)
        return UsersRead(**user.__dict__)

    @patch("/{user_id:int}", summary="Обновить пользователя")
    async def update_user(self, user_id: int, data: UsersUpdate, service: UsersService) -> UsersRead:
        user = await service.update(user_id, data)
        return UsersRead(**user.__dict__)

    @delete("/{user_id:int}", summary="Удалить пользователя")
    async def delete_user(self, user_id: int, service: UsersService) -> None:
        await service.delete(user_id)
