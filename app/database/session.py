from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core import config

engine = create_async_engine(config.database.create_url())

async_session = async_sessionmaker(engine)
