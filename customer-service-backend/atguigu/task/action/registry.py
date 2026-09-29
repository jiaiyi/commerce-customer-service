from typing import Dict

from atguigu.task.action.base import Action


class ActionRegistry:

    def __init__(self):
        self._actions:Dict[str, Action] = {}

    def register(self,action:Action):
        self._actions[action.name] = action

    def get(self,action_name:str) -> Action:
        if action_name not in self._actions:
            raise KeyError(f"Action {action_name} not found")
        return self._actions[action_name]

