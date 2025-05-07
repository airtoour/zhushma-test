from advanced_alchemy.exceptions import (
    NotFoundError,
    SerializationError,
    RepositoryError
)
from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies
)
from advanced_alchemy.service import OffsetPagination

from app.core.db import UsersCreate, UsersUpdate, UsersRead
from app.core.services.users import UsersService

from litestar import Controller, get, post, patch, delete
from litestar.exceptions.http_exceptions import NotFoundException, ClientException
from litestar.params import Parameter


class UsersController(Controller):
    """CRUD-эндпоинты для модели Users"""

    path = "/users"
    tags = ["Users"]

    dependencies = create_service_dependencies(
        UsersService,
        key="service"
    )

    @post("/add", summary="Создать пользователя")
    async def create_user(self, service: UsersService, data: UsersCreate) -> UsersRead:
        try:
            # Пытаемся создать пользователя
            obj = await service.create(data)
        except (SerializationError, RepositoryError):
            raise ClientException

        # Возвращаем схему нового пользователя
        return service.to_schema(obj, schema_type=UsersRead)

    @get("/", summary="Список пользователей")
    async def list_users(self, service: UsersService) -> OffsetPagination[UsersRead]:
        try:
            # Получаем всех пользователей в виде пагинации
            results, total = await service.list_and_count()
        except NotFoundError:
            raise NotFoundException(detail="Rows Not Found")

        # Возвращаем схему пагинации пользователей
        return service.to_schema(results, total, schema_type=UsersRead)

    @get("/{user_id:int}", summary="Получить пользователя", cache=True)
    async def get_user(
        self,
        service: UsersService,
        user_id: int = Parameter(description="ID Пользователя")
    ) -> UsersRead:
        try:
            # Получаем пользователя по user_id
            user = await service.get(user_id)
        except NotFoundError:
            raise NotFoundException(detail="User Not Found")

        # Возвращаем схему найденного пользователя
        return service.to_schema(user, schema_type=UsersRead)

    @patch("/{user_id:int}", summary="Обновить пользователя")
    async def update_user(
        self,
        service: UsersService,
        data: UsersUpdate,
        user_id: int = Parameter(description="ID Пользователя")
    ) -> UsersRead:
        try:
            # Обновляем пользователя по user_id
            user = await service.update(data.serialize(), user_id)
        except NotFoundError:
            raise NotFoundException(detail="User Not Found")

        # Возвращаем схему обновлённого пользователя
        return service.to_schema(user, schema_type=UsersRead)

    @delete("/{user_id:int}", summary="Удалить пользователя")
    async def delete_user(
        self,
        service: UsersService,
        user_id: int = Parameter(description="ID Пользователя")
    ) -> None:
        try:
            # Удаляем пользователя по user_id
            await service.delete(user_id)
        except NotFoundError:
            raise NotFoundException(detail="User Not Found")
