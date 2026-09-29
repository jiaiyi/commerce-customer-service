from typing import Any

from atguigu.conf.config import settings
from atguigu.infrastructure.http_util import http_client
from urllib.parse import quote


def _base_url() -> str:
    return settings.commerce_api_base_url.rstrip("/")


def _extract_data(resullt:dict | None) -> dict | None:
    data = resullt.get("data") if isinstance(resullt,dict) else None
    return data if isinstance(data,dict) else None



async def fetch_logistics(order_id:str) -> dict | None:
    try:
        r = await http_client.get(f"{_base_url()}/orders/{quote(order_id)}/logistics")
        return _extract_data(r.json())
    except Exception as e:
        return None

async def fetch_order(order_id:str) -> dict | None:
    try:
        r = await http_client.get(f"{_base_url()}/orders/{quote(order_id)}")
        return _extract_data(r.json())
    except Exception as e:
        return None

async def fetch_product(product_id:str) -> dict | None:
    try:
        r = await http_client.get(f"{_base_url()}/products/{quote(product_id)}")
        return _extract_data(r.json())
    except Exception as e:
        return None

async def _build_order_summary(payload:dict[str,Any]) -> str:
    parts = []
    if payload.get("amount"):
        parts.append(f"订单金额 ￥{payload['amount']}")
    items = payload.get("items") or []
    if items:
        titles = [str(item.get("title_snapshot") or "").strip() for item in items[:2] if item.get("title_snapshot")]
        if titles:
            parts.append("商品：" + "、".join(titles))
    return "。".join(parts) + "。" if parts else ""
