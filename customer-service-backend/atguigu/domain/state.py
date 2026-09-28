import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List

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

    def get_current_session(self) ->Session|None:
        if self.current_session_id is None:
            return None
        for session in self.sessions:
            if session.session_id == self.current_session_id:
                return session

    def start_session(self):
        now_time = time.time()
        new_session = Session(
            session_id=str(uuid.uuid4()),
            stared_at=now_time,
            last_activity_at=now_time,
        )
        self.sessions.append(new_session)
        self.current_session_id = new_session.session_id

    def close_current_session(self):
        self.get_current_session().closed_at = time.time()
        self.current_session_id = None

    def reset_runtime_state_for_new_session(self):
        self.active_task = None
        self.active_system_task = None
        self.focused_object = None
        self.paused_tasks = []

    def update_session_last_activity(self):
        self.get_current_session().last_activity_at = time.time()

    def begin_turn(self, user_message:UserMessage):
        self.pending_turn = Turn(
            turn_id=str(uuid.uuid4()),
            input_message=user_message,
        )

    def fill_pending_turn(self, messages:List[BotMessage]):
        self.pending_turn.assistant_messages = messages

    def commit_pending_turn(self):
        self.get_current_session().turns.append(self.pending_turn)
        self.pending_turn = None

    def interrupt_active_task(self):
        self.paused_tasks.append(self.active_task)
        self.active_task = None
        self.active_system_task = None

    def start_task(self, task_context:TaskContext):
        self.active_task = task_context
        self.active_system_task = None

    def start_system_task(self, system_context:SystemContext):
        self.active_system_task = system_context

    def set_slots(self, slots:dict):
        self.active_task.slots.update(slots)

    def cancel_active_task(self):
        self.active_task = None
        self.active_system_task = None

    def resume_task(self, flow_id:str):
        for task in self.paused_tasks:
            if task.flow_id == flow_id:
                self.active_task = task
                self.paused_tasks.remove(task)
                break