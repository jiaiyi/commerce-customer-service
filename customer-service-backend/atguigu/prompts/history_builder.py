from typing import List

from sqlalchemy.orm import attributes

from atguigu.domain.messages import UserMessage, MessageType, MessageObject, BotMessage
from atguigu.domain.state import Turn


def render_object(object):
    # [订单信息 id=ORD-20260620-88431,title=蓝牙耳机,status=已发货,amount=299.00,logistics=顺丰快递]
    # [商品信息 id=SKU-50012,title=索尼 WH-1000XM5,price=2499.00,type=头戴式,anc=行业领先]
    label = "订单信息" if object.type == "order" else "商品信息"
    attributes_str = ",".join([f"{key}={value}" for key, value in object.attributes.items()])
    return f"{label} id={object.id},title={object.title},{attributes_str}"

def render_user_message(user_message:UserMessage) -> str:
    if user_message.type == MessageType.TEXT:
        return f"USER:{user_message.text}"
    else:
        object:MessageObject = user_message.object
        object_text = render_object(object)
        return f"USER:{object_text}"


def render_bot_message(bot_message:BotMessage) -> str:
    if bot_message.text:
        return f"BOT:{bot_message.text}"
    else:
        object:MessageObject = bot_message.object
        object_text = render_object(object)
        return f"BOT:{object_text}"

def build_history(turns:List[Turn]) -> str:
    """
        构建历史对话内容，构建后的对话历史结构如下：
    """
    chat_list = []
    for turn in turns:
        # 一轮对话中的用户消息
        user_message:UserMessage = turn.input_message
        user_message_text = render_user_message(user_message)
        chat_list.append(user_message_text)
        # 一轮对话中的机器人消息
        bot_messages = turn.assistant_messages
        for bot_message in bot_messages:
            bot_message_text = render_bot_message(bot_message)
            chat_list.append(bot_message_text)
    return f"\n".join(chat_list)