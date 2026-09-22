from functools import lru_cache

from atguigu.service.dialogue_service import DialogueService


@lru_cache
def get_dialogue_service() -> DialogueService:
    return DialogueService()