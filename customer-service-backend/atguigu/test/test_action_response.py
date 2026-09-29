import asyncio

from typer.cli import state

from atguigu.domain.contexts import TaskContext
from atguigu.domain.messages import UserMessage, MessageType
from atguigu.domain.state import DialogueState, Turn
from atguigu.task.action.base import ActionResult
from atguigu.task.action.builtin.action_response import ActionResponse

async def test():
    action = ActionResponse()

    state = DialogueState(sender_id="u1001")
    state.active_task = TaskContext(
        flow_id="ghjkl",
        step_id="start",
        slots={
            "order_number": "123456",
            "order_status": "已发货"
        }
    )
    state.pending_turn = Turn(
        turn_id="turn_001",
        input_message=UserMessage(
            sender_id="u1001",
            message_id="msg_001",
            type=MessageType.TEXT,
            text="我想查询一下我的订单状态。"
        )
    )

    args = {
        "mode": "generate",
        # "text": "订单{{ slots.order_number }}当前状态是{{ slots.order_status }}我会继续帮你跟进。"
    }

    result: ActionResult = await action.run(state, args)
    print(result)


if __name__ == '__main__':
    asyncio.run(test())