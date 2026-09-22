import uuid

from fastapi import APIRouter, Depends
from langchain.agents.middleware.todo import Todo
from langchain_core.messages import ChatMessage

from atguigu.api.deps import get_dialogue_service
from atguigu.api.schemas import ChatHistoryResponse, ChatResponse, ChatRequest, BotMessageResponse, \
    ChatHistoryMessageResponse, ChatObjectPayload
from atguigu.domain.message import UserMessage, ProcessResult, MessageType, MessageObject
from atguigu.service.dialogue_service import DialogueService

router = APIRouter()

# 将接口请求对象转换为Message对象
def _build_message(chat_request : ChatRequest) -> UserMessage:
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id or str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text=chat_request.text,
        object=MessageObject(
            type=chat_request.object.type,
            id=chat_request.object.id,
            title=chat_request.object.title,
            attributes=chat_request.object.attributes
        ) if chat_request.object else None
    )

# 将消息处理后的ProcessResult(Message对象)转换为ChatResponse对象
def _build_response(process_result):
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        messages=[BotMessageResponse(
            text=bot_msg.text,
            object=ChatObjectPayload(
                type=bot_msg.object.type,
                id=bot_msg.object.id,
                title=bot_msg.object.title,
                attributes=bot_msg.object.attributes
            ) if bot_msg.object else None
        ) for bot_msg in process_result.messages]
    )

# 对话
@router.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest,dialogue_service: DialogueService = Depends(get_dialogue_service)):
    # 1.将交互模型chat_request 转换成 领域模型 UserMessage
    user_message:UserMessage = _build_message(chat_request)

    # 2.调用DialogueService类中的process_message方法进行对话处理
    process_result:ProcessResult = dialogue_service.process_message(user_message)

    # 3.将领域模型 process_result 转换成交互模型 ChatResponse
    chat_response = _build_response(process_result)
    return chat_response


# 历史对话
@router.get("/api/chat/history",response_model=ChatHistoryResponse)
async  def chat_history(sender_id:str):
    print("sender_id",sender_id)
    # TODO 调用service查询当前用户的历史记录
    return ChatHistoryResponse(
                sender_id=sender_id,
                messages=[
                    ChatHistoryMessageResponse(
                        role="user",
                        text="你好"
                    ),
                    ChatHistoryMessageResponse(
                        role="bot",
                        text="你好呀~O(∩_∩)O~"
                    )
                ]
            )