from functools import lru_cache

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.engine.builder import build_dialogue_engine
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.infrastructure import database
from atguigu.repository.dialogue_state_repository import DialogueStateRepository
from atguigu.service.dialogue_service import DialogueService


async def get_session() -> AsyncSession:
    async with database.session_factory() as session:
        yield session

@lru_cache()
def get_dialogue_state_repository(
        session: AsyncSession = Depends(get_session),
) -> DialogueStateRepository:
    return DialogueStateRepository(session)

@lru_cache()
def get_dialogue_engine() -> DialogueEngine:
    return build_dialogue_engine()

@lru_cache
def get_dialogue_service(
        repository: DialogueStateRepository = Depends(get_dialogue_state_repository),
        engine: DialogueEngine = Depends(get_dialogue_engine)
) -> DialogueService:
    return DialogueService(repository,engine)