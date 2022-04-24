__all__ = [
    'register_cross', 'register_middleware', 'register_startup_and_shutdown'
]

import datetime
import time
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from core.database import redis_cache, es
from core.setting import settings


def register_cross(app: FastAPI):
    """
    跨越配置
    :param app:
    :return:
    """
    origins = settings.BACKEND_CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def rewrite_other_exception_response(request: Request, call_next):
        """
        中间件
        :param request:
        :param call_next:
        :return:
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        # 无nginx
        # ip = request.client.host
        # 有Nginx  二选一 得看NGINX 的配置
        ip = request.headers.get('X-Real-IP')
        # 因为有可能走多层代理 取最后一个
        if ip:
            ip = ip.split(',')[-1]
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        path = request.url
        response.headers["X-Process-Time"] = str(process_time)
        print(f"{time_str} | {ip} | {path}：处理时间：{process_time}s")
        return response


def register_startup_and_shutdown(app: FastAPI) -> None:
    """
    把redis挂载到app对象上面
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        启动
        :return:
        """
        await redis_cache.init_cache()

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        关闭
        :return:
        """
        await redis_cache.close()
        await es.close()
