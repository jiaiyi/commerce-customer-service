from typing import Dict, Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.task.action.custom.shared import fetch_order, _build_order_summary


class LookupOrderStatusAction(Action):

    name = "action_lookup_order_status"

    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        # 根据order_number查询订单状态信息：order_status，order_summary
        order_number = state.active_task.slots.get("order_number")
        payload = await fetch_order(order_number)
        if payload is None:
            return ActionResult(solt_updates={
                "order_status":"查询失败",
                "order_summary":"暂时无法查询到该订单信息，请稍后重试"
            })
        return ActionResult(solt_updates={
            "order_status": payload.get("order_status") or payload.get("status") or "未知",
            "order_summary":_build_order_summary(payload)
        })