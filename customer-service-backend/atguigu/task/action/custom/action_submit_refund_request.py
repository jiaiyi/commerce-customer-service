
from typing import Dict, Any
from urllib.parse import quote

from atguigu.conf.config import settings
from atguigu.domain.state import DialogueState
from atguigu.infrastructure.http_util import http_client
from atguigu.task.action.base import Action, ActionResult


class SubmitRefundRequestAction(Action):

    name = "action_submit_refund_request"

    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        # 1.从当前任务上下文的slots中获取订单编号与退款原因
        order_number = state.active_task.slots.get("order_number")
        refund_reason = state.active_task.slots.get("refund_reason")
        # 2.调用业务后端创建退款申请
        url = f"{settings.commerce_api_base_url.rstrip('/')}/orders/{quote(order_number)}/refund-applications"
        try:
            response = await http_client.post(url,json={"reason":refund_reason or "","submitted_by":"system"})
            result = response.json()
        except Exception:
            return ActionResult(solt_updates={
                "order_submit_status":"error"
            })
        # 3.根据返回结果设置退款状态
        if not isinstance(result, dict):
            return ActionResult(solt_updates={
                "order_submit_status":"error"
            })
        if result.get("code") == 0:
            return ActionResult(solt_updates={
                "order_submit_status":"success"
            })
        else:
            return ActionResult(solt_updates={
                "order_submit_status":"error"
            })