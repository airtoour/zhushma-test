from litestar import Litestar

from app.api.users import UsersController
from app.core.db.session import alchemy


app = Litestar(
    route_handlers=[UsersController],
    plugins=[alchemy]
)
