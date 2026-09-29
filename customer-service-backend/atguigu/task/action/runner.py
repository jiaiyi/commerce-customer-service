from dataclasses import dataclass, field
from typing import Dict, Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import ActionResult
from atguigu.task.action.registry import ActionRegistry


@dataclass
class ActionCall:
    action_name: str
    action_args: Dict[str,Any] = field(default_factory=dict)

class ActionRunner:

    def __init__(self,registry: ActionRegistry):
        self.registry = registry

    async def execute_action(self,action_call:ActionCall,state:DialogueState) -> ActionResult:
        # 1.从action_call中获取action_name
        action_name = action_call.action_name
        # 2.根据action_name获取对应的Action类的对象
        action = self.registry.get(action_name)
        # 3.使用Action类实例调用run方法
        action.run(state,action_call.action_args)