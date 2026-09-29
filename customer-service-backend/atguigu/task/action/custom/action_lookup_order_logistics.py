from typing import Dict, Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.task.action.custom.shared import fetch_logistics


class LookupOrderLogistics(Action):

    name = "action_lookup_logistics"

    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        # 根据订单编号查询订单物流信息：logistics_company,tracking_number,logistics_status
        order_number = state.active_task.slots.get("order_number")
        payload = await fetch_logistics(order_number)

        if payload is None:
            return ActionResult(solt_updates={
                "tracking_number":"未知",
                "logistics_company":"未知",
                "logistics_status":"暂时无法查到物流信息，请稍后重试"
            })
        return ActionResult(solt_updates={
            "tracking_number":payload.get("tracking_number") or "未知",
            "logistics_company":payload.get("logistics_company") or "未知",
            "logistics_status":payload.get("status_desc") or payload.get("status") or "未知"
        })

