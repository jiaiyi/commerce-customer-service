import asyncio

from atguigu.infrastructure import http_util
# 测试get请求
async def test_get_request():
    http_util.init_http_client()
    response = await http_util.http_client.get("http://localhost:18081/users/u1001/orders")
    print(response.json())
    await http_util.close_http_client()

if __name__ == '__main__':
    asyncio.run(test_get_request())