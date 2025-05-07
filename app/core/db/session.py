from advanced_alchemy.config import (
    AsyncSessionConfig,
    AlembicAsyncConfig
)
from advanced_alchemy.extensions.litestar import (
    SQLAlchemyPlugin,
    SQLAlchemyAsyncConfig
)
from app.core.config import settings


session_config = AsyncSessionConfig(expire_on_commit=False)

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=str(settings.db.url),
    before_send_handler="autocommit",
    session_config=session_config,
    alembic_config=AlembicAsyncConfig(script_location="./migrations")
)

alchemy = SQLAlchemyPlugin(config=sqlalchemy_config)
