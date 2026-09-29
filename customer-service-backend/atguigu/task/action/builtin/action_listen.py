
from typing import Any, Dict, List


from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class ActionListen(Action):
    name = "action_listen"
    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        pass