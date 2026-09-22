from dataclasses import dataclass, field
from typing import Any, Dict




@dataclass(slots=True)
class TaskContext:
    flow_id: str
    step_id: str
    slots: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskContext":
        return cls(
            flow_id=data["flow_id"],
            step_id=data["step_id"],
            slots=dict(data.get("slots", {})),
        )

@dataclass(slots=True)
class SystemContext:
    """所以系统任务上下文的父类"""
    flow_id: str
    step_id: str

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "SystemContext":
        flow_id = raw_sys.get("flow_id")
        return SYSTEM_CONTEXT_DICT[flow_id].from_dict(raw_sys)

@dataclass(slots=True)
class StartedSystemContext(SystemContext):
    """system_task_started系统任务上下文"""
    started_flow_id: str
    started_flow_name: str

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "StartedSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            started_flow_id=raw_sys["started_flow_id"],
            started_flow_name=raw_sys["started_flow_name"]
        )

@dataclass(slots=True)
class ResumedSystemContext(SystemContext):
    """system_task_resumed系统任务上下文"""
    resumed_flow_id: str
    resumed_flow_name: str

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "ResumedSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            resumed_flow_id=raw_sys["resumed_flow_id"],
            resumed_flow_name=raw_sys["resumed_flow_name"]
        )

@dataclass(slots=True)
class CannotHandleSystemContext(SystemContext):
    """system_cannot_handle系统任务上下文"""
    reason: str
    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "CannotHandleSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            reason=raw_sys["reason"]
        )

@dataclass(slots=True)
class CollectSystemContext(SystemContext):
    """system_collect_information系统任务上下文"""
    slot_name: str
    response: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "CollectSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            slot_name=raw_sys["slot_name"],
            response=raw_sys.get("response", {})
        )

@dataclass(slots=True)
class InterruptedSystemContext(SystemContext):
    """system_task_interrupted系统任务上下文"""
    interrupted_flow_id: str
    interrupted_flow_name: str
    started_flow_id: str | None = None
    started_flow_name: str | None = None

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "InterruptedSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            interrupted_flow_id=raw_sys["interrupted_flow_id"],
            interrupted_flow_name=raw_sys["interrupted_flow_name"],
            started_flow_id=raw_sys.get("started_flow_id"),
            started_flow_name=raw_sys.get("started_flow_name")
        )

@dataclass(slots=True)
class CanceledSystemContext(SystemContext):
    """system_task_canceled系统任务上下文"""
    canceled_flow_id: str
    canceled_flow_name: str

    @classmethod
    def from_dict(cls, raw_sys:Dict) -> "CanceledSystemContext":
        return cls(
            flow_id=raw_sys["flow_id"],
            step_id=raw_sys["step_id"],
            canceled_flow_id=raw_sys["canceled_flow_id"],
            canceled_flow_name=raw_sys["canceled_flow_name"]
        )

SYSTEM_CONTEXT_DICT = {
    "system_task_started": StartedSystemContext,
    "system_task_resumed": ResumedSystemContext,
    "system_cannot_handle": CannotHandleSystemContext,
    "system_collect_information": CollectSystemContext,
    "system_task_interrupted": InterruptedSystemContext,
    "system_task_canceled": CanceledSystemContext,
}