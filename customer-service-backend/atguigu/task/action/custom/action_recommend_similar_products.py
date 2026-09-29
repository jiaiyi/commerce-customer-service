from typing import Dict, Any

from atguigu.domain.messages import BotMessage, MessageObject
from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.task.action.custom.shared import fetch_product


class RecommendSimilarProductsAction(Action):

    name = "action_recommend_similar_products"

    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        # 根据商品id查询类似商品
        product_id = state.active_task.slots.get("product_id")
        label = product_id or "这件商品"

        payload = await fetch_product(product_id)
        if payload:
            label = str(payload.get("title") or "").strip() or label

        return ActionResult(
            messages=[
                BotMessage(text="好的，为你推荐的商品如下："),
                BotMessage(object=MessageObject(
                    type="product",
                    id="SKU-50012",
                    title="索尼 WH-1000XM5",
                    attributes={
                        "price": "2499.00",
                        "type": "头戴式",
                        "anc": "行业领先"
                    }
                )),
                BotMessage(object=MessageObject(
                    type="product",
                    id="SKU-50013",
                    title="索尼 WH-1000XM4",
                    attributes={
                        "price": "1999.00",
                        "type": "头戴式",
                        "anc": "行业领先"
                    }
                )),
                BotMessage(object=MessageObject(
                    type="product",
                    id="SKU-50014",
                    title="索尼 WH-1000XM3",
                    attributes={
                        "price": "1499.00",
                        "type": "头戴式",
                        "anc": "行业领先"
                    }
                ))
            ]
        )