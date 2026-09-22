from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List


# 用户消息类型枚举
class MessageType(str, Enum):
    TEXT = 'text'
    OBJECT = 'object'

# 对象消息模型
@dataclass(slots=True)
class MessageObject:
    type: str
    id: str
    title: str
    attributes: dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    @classmethod
    def from_dict(cls, dict_data: Dict[str, Any]) -> "MessageObject":
        return cls(**dict_data)

# 用户消息模型
@dataclass(slots=True)
class UserMessage:
    message_id: str
    sender_id: str
    type: MessageType
    text: str | None = None
    object: MessageObject | None = None

    def to_dict(self) -> Dict[str, Any]:
        return{
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "type": self.type.value,
            "text": self.text,
            "object": self.object.to_dict() if self.object else None
        }
    @classmethod
    def from_dict(cls, dict_data: Dict[str, Any]) -> "UserMessage":
        return cls(
            message_id=dict_data['message_id'],
            sender_id=dict_data['sender_id'],
            type=MessageType.TEXT if dict_data['type'] == "text" else MessageType.OBJECT,
            text=dict_data.get('text'),
            object=MessageObject.from_dict(dict_data["object"]) if dict_data.get("object") else None
        )

# 机器消息模型
@dataclass(slots=True)
class BotMessage:
    text: str | None = None
    object: MessageObject | None = None

    def to_dict(self) -> dict:
        return{
            "text": self.text,
            "object": self.object.to_dict() if self.object else None
        }
    @classmethod
    def from_dict(cls, dict_data: dict) -> "BotMessage":
        return cls(
            text=dict_data.get('text'),
            object=MessageObject.from_dict(dict_data["object"]) if dict_data.get("object") else None
        )

# service处理结果模型
@dataclass(slots=True)
class ProcessResult:
    message_id: str
    sender_id: str
    messages: List[BotMessage] = field(default_factory=list)
