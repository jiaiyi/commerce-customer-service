import time
from dataclasses import dataclass, field
from typing import Any, Dict

from atguigu.domain.contexts import TaskContext, SystemContext
from atguigu.domain.message import UserMessage, BotMessage


@dataclass(slots=True)
class FocusedObject:
    type:str
    id:str
    title:str
    attributes:dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls,raw_fo:Dict[str,Any]) -> "FocusedObject":
        return cls(**raw_fo)

@dataclass(slots=True)
class Turn:
    """对话轮次"""
    turn_id:str
    input_message: UserMessage
    assistant_messages: list[BotMessage] = field(default_factory=list)

    @classmethod
    def from_dict(cls,data:Dict[str,Any]) -> "Turn":
        return cls(
            turn_id=data["turn_id"],
            input_message=UserMessage.from_dict(data["input_message"]),
            assistant_messages=[BotMessage.from_dict(m) for m in data.get("assistant_messages", [])],
        )

@dataclass(slots=True)
class Session:
    """用户会话：当两条消息时间间隔超过【1个小时】时，会话结束"""
    session_id: str
    stared_at: float
    last_activity_at: float
    closed_at: float
    turns: list[Turn] = field(default_factory=list)

    @classmethod
    def from_dict(cls,data:dict) -> "Session":
        return cls(
            session_id=data["session_id"],
            stared_at=data.get("stared_at",time.time()),
            last_activity_at=data.get("last_activity_at",time.time()),
            closed_at=data.get("closed_at"),
            turns=[Turn.from_dict(t) for t in data.get("turns", [])],
        )

@dataclass(slots=True)
class DialogueState:
    sender_id: str
    active_task: TaskContext | None = None
    paused_tasks: list[TaskContext] = field(default_factory=list)
    active_system_task: SystemContext | None = None
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(default_factory=list)
    current_session_id: str |None = None
    pending_turn: Turn | None = None

    @classmethod
    def from_dict(cls,data:dict[str,Any]) -> "DialogueState":
        """从字典还原 DialogueState"""
        state = cls(sender_id=data["sender_id"])
        # 当前用户任务
        raw_task = data.get("active_task")
        state.active_task = TaskContext.from_dict(raw_task) if raw_task is not None else None
        # 挂起的任务
        paused_tasks = [TaskContext.from_dict(t) for t in data.get("paused_tasks", [])]
        # 系统任务
        raw_sys = data.get("active_system_task")
        state.active_system_task = SystemContext.from_dict(raw_sys) if raw_sys is not None else None

        raw_fo = data.get("focused_object")
        state.focused_object = FocusedObject.from_dict(raw_fo) if raw_fo is not None else None
        state.sessions = [Session.from_dict(s) for s in data.get("sessions", [])]
        state.current_session_id = data.get("current_session_id")
        return state