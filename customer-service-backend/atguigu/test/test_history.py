from atguigu.domain.messages import UserMessage, MessageType, BotMessage, MessageObject
from atguigu.domain.state import Turn
from atguigu.prompts.history_builder import build_history

if __name__ == '__main__':
    turns: list[Turn] = [
        Turn(
            turn_id="turn_001",
            input_message=UserMessage(
                message_id="msg_001",
                sender_id="user_100",
                type=MessageType.TEXT,
                text="你好，我想查一下我的订单"
            ),
            assistant_messages=[
                BotMessage(text="好的，请提供您的订单号，我帮您查询。")
            ]
        ),
        Turn(
            turn_id="turn_002",
            input_message=UserMessage(
                message_id="msg_002",
                sender_id="user_100",
                type=MessageType.OBJECT,
                object=MessageObject(
                    type="order",
                    id="ORD-20260620-88431",
                    title="订单信息",
                    attributes={"status": "已发货", "amount": "299.00", "created_at": "2026-06-20"}
                )
            ),
            assistant_messages=[
                BotMessage(text="已为您查到该订单的详细信息："),
                BotMessage(
                    object=MessageObject(
                        type="order",
                        id="ORD-20260620-88431",
                        title="蓝牙耳机",
                        attributes={"status": "已发货", "amount": "299.00", "logistics": "顺丰快递"}
                    )
                )
            ]
        ),
        Turn(
            turn_id="turn_003",
            input_message=UserMessage(
                message_id="msg_003",
                sender_id="user_100",
                type=MessageType.TEXT,
                text="这个耳机有降噪功能吗？"
            ),
            assistant_messages=[
                BotMessage(text="这款耳机支持主动降噪（ANC），降噪深度可达35dB，非常适合通勤和办公使用。")
            ]
        ),
        Turn(
            turn_id="turn_004",
            input_message=UserMessage(
                message_id="msg_004",
                sender_id="user_100",
                type=MessageType.TEXT,
                text="我想看看有没有其他类似的耳机"
            ),
            assistant_messages=[
                BotMessage(text="为您推荐以下几款热销降噪耳机："),
                BotMessage(
                    object=MessageObject(
                        type="product",
                        id="SKU-50012",
                        title="索尼 WH-1000XM5",
                        attributes={"price": "2499.00", "type": "头戴式", "anc": "行业领先"}
                    )
                ),
                BotMessage(
                    object=MessageObject(
                        type="product",
                        id="SKU-50037",
                        title="苹果 AirPods Pro 2",
                        attributes={"price": "1799.00", "type": "入耳式", "anc": "自适应降噪"}
                    )
                )
            ]
        ),
        Turn(
            turn_id="turn_005",
            input_message=UserMessage(
                message_id="msg_005",
                sender_id="user_100",
                type=MessageType.TEXT,
                text="索尼那款包邮吗？"
            ),
            assistant_messages=[
                BotMessage(text="索尼 WH-1000XM5 目前全场包邮，预计2个工作日内发货，支持7天无理由退换。")
            ]
        ),
    ]

    result = build_history(turns)
    print(result)