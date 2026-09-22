import uvicorn

from atguigu.conf.config import settings


def main():
    uvicorn.run(
        "atguigu.api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )

if __name__ == '__main__':
    main()