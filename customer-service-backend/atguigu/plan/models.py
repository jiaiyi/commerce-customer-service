from dataclasses import dataclass, field

from atguigu.task.commands.models import Command


@dataclass(slots=True)
class TaskTurnPlan:
    command : list[Command] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dict_data: dict) -> 'TaskTurnPlan':
        return cls(
            commands=[Command.from_dict(command_dict) for command_dict in dict_data.get("commands",[])]
        )


@dataclass(slots=True)
class KnowledgeTurnPlan:
    intents : list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dict_data: dict) -> 'KnowledgeTurnPlan':
        return cls(
            intents=dict_data.get("intents",[])
        )


@dataclass(slots=True)
class ChitchatTurnPlan:
    pass

@dataclass(slots=True)
class TurnPlan:
    task : TaskTurnPlan | None = None
    knowledge : KnowledgeTurnPlan | None = None
    chitchat : ChitchatTurnPlan | None = None

    @classmethod
    def from_dict(cls, dict_data: dict) -> 'TurnPlan':
        return cls(
            task = None,
            knowledge = None,
            chitchat = None,
        )

    @classmethod
    def from_dict(cls,dict_data: dict) -> 'TurnPlan':
        return cls(
            task = TaskTurnPlan.from_dict(dict_data.get('task')) if dict_data.get('task') else None,
            knowledge = KnowledgeTurnPlan.from_dict(dict_data.get('knowledge')) if dict_data.get('knowledge') else None,
            chitchat = ChitchatTurnPlan() if dict_data.get('chitchat') else None,
        )