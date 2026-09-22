from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from atguigu.conf.config import settings

engine : AsyncEngine | None = None
session_factory : async_sessionmaker[AsyncSession] | None = None

# 初始化数据库和会话工厂
def init_db_engine_and_session_factory() -> None:
    global engine, session_factory
    engine = create_async_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True,
    )
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

#关闭数据库引擎
async def close_db_engine():
    if engine is not None:
        await engine.dispose()
