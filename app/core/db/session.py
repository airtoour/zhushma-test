from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin, SQLAlchemyAsyncConfig
from litestar.contrib.sqlalchemy.plugins import SQL
from core.config import settings

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.url
)

db_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
