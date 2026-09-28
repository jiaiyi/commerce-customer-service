from dataclasses import dataclass, field
from enum import Enum
from typing import Any


#=============step的next属性  link=======================

@dataclass(slots=True)
class FlowStepLink:
    target:str

@dataclass(slots=True)
class ConditionalLink(FlowStepLink):
    condition:str

@dataclass(slots=True)
class FallbackLink(FlowStepLink):
    pass

@dataclass(slots=True)
class StaticLink(FlowStepLink):
    pass


#===================steps属性=========================

class FlowStepType(str,Enum):
    START = "start"
    ACTION = "action"
    COLLECT = "collect"
    END = "end"

@dataclass(slots=True)
class FlowStep:
    id:str
    type:FlowStepType
    next:list[FlowStepLink]

    @classmethod
    def from_dict(cls, dict_data:dict) -> "FlowStep":
        step_type = dict_data.get("type")
        return FLOWSTEO_DICT[step_type].from_dict(dict_data)


@dataclass(slots=True)
class StartFlowStep(FlowStep):
    @classmethod
    def from_dict(cls, dict_data:dict) -> "StartFlowStep":
        return cls(
            id=dict_data.get("id"),
            type=FlowStepType.START,
            next=_build_next_links(dict_data.get("next",[])),
        )

def _build_next_links(next_data:str | list) -> list[FlowStepLink]:
    next_link = []
    if isinstance(next_data, str):
        next_link.append(StaticLink(target=next_data))
    else:
        for link_data in next_data:
            if link_data.get("if"):
                next_link.append(ConditionalLink(
                    condition=link_data.get("if"),
                    target=link_data.get("then")
                ))
            else:
                next_link.append(FallbackLink(
                    target=link_data.get("else"),
                ))
    return next_link

@dataclass(slots=True)
class EndFlowStep(FlowStep):
    @classmethod
    def from_dict(cls, dict_data:dict) -> "EndFlowStep":
        return cls(
            id=dict_data.get("id"),
            type=FlowStepType.END,
            next=[]
        )

@dataclass(slots=True)
class ActionFlowStep(FlowStep):
    action:str
    args:dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, dict_data:dict) -> "ActionFlowStep":
        return cls(
            id=dict_data.get("id"),
            type=FlowStepType.ACTION,
            next=_build_next_links(dict_data.get("next",[])),
            action=dict_data.get("action"),
            args=dict_data.get("args",{}),
        )

@dataclass(slots=True)
class ResponseDefinition:
    mode:str = "static"
    text:str | None = None
    prompt:str | None = None

@dataclass(slots=True)
class SlotValidation:
    condition:str
    failure_response:ResponseDefinition | None = None

@dataclass(slots=True)
class CollectFlowStep(FlowStep):
    slot_name:str
    response:ResponseDefinition
    validation:SlotValidation | None = None

    @classmethod
    def from_dict(cls, dict_data:dict) -> "CollectFlowStep":
        return cls(
            id=dict_data.get("id"),
            type=FlowStepType.COLLECT,
            next=_build_next_links(dict_data.get("next",[])),
            slot_name=dict_data.get("slot_name"),
            response=ResponseDefinition(**dict_data.get("response",{})),
            validation=SlotValidation(
                condition=dict_data.get("validation").get("condition",""),
                failure_response=ResponseDefinition(**dict_data.get("validation").get("failure_response",{})),
            ) if dict_data.get("validation") else None,
        )

FLOWSTEO_DICT = {
    "start": StartFlowStep,
    "end": EndFlowStep,
    "action": ActionFlowStep,
    "collect": CollectFlowStep
}

#================flow=====================

@dataclass(slots=True)
class FlowSlot:
    name:str
    type:str
    label:str
    description:str

@dataclass(slots=True)
class Flow:
    id:str
    name:str
    description:str
    steps:list[FlowStep] = field(default_factory=list)
    slots:list[FlowSlot] = field(default_factory=list)

    def get_start_step(self) ->FlowStep:
        for step in self.steps:
            if step.type == FlowStepType.START:
                return step
        raise Exception("No start step")


@dataclass(slots=True)
class FlowsList:
    slots:dict[str,FlowSlot] = field(default_factory=dict)
    flows:list[Flow] = field(default_factory=list)

    def get_flow_by_id(self, flow_id:str) -> Flow|None:
        for flow in self.flows:
            if flow.id == flow_id:
                return flow
        return None




