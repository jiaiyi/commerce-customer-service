import asyncio

from sqlalchemy import text

from atguigu.infrastructure import database


# 测试数据库连接
async def test():
    database.init_db_engine()
    async with database.session_factory() as session:
        result = await session.execute(text("select 1"))
        print(result.fetchone())
    await database.close_db_engine()

if __name__ == '__main__':

    asyncio.run(test())