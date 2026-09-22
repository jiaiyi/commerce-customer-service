from atguigu.domain.message import UserMessage, ProcessResult, BotMessage, MessageObject


class DialogueService:

    def process_message(self,user_message:UserMessage) -> ProcessResult:
        # 1.调用Repository层：根据message.sender_id查询当前用户的对话状态
        # 2.调用Enginge层：处理消息
        # 3.调用Repository层：更新对话状态
        # 4.返回处理结果
        return ProcessResult(
            sender_id=user_message.sender_id,
            message_id=user_message.message_id,
            messages=[
                BotMessage(
                    text="你好，我是小谷，请问有什么我可以帮忙的吗？",
                    object=None
                ),
                BotMessage(
                    text=None,
                    object=MessageObject(
                        type="product",
                        id="123456789",
                        title="联想U盘-128GB",
                        attributes={
                            "size": "128GB",
                            "color": "white",
                            "price": "100"
                        }
                    )
                )
            ]
        )