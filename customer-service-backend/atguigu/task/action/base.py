from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState

@dataclass(slots=True)
class ActionResult:
    messages:List[BotMessage] = field(default_factory=list)
    solt_updates:Dict[str,Any] = field(default_factory=dict)


class Action(ABC):
    name:str

    @abstractmethod
    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        pass