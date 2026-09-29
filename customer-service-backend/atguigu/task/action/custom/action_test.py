from typing import Dict, Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class TestAction(Action):
    name = "test_action"
    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        pass