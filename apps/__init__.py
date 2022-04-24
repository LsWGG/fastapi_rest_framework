from fastapi import FastAPI

from apps.api.v1.router import api_router
from core.database import init_db
from core.exception import register_exception
from core.middleware import register_cross, register_middleware, register_startup_and_shutdown
from core.setting import settings


def create_app():
    app = FastAPI(
        title="Demo_API",
        version="0.1.1",
        docs_url="/api/docs",  # 自定义文档地址
        openapi_url="/api/openapi.json",
    )

    # 导入路由, 前缀设置
    app.include_router(
        api_router,
        prefix=settings.API_V1_STR,
    )
    # 初始化
    init_db(app)
    register_cross(app)
    register_middleware(app)
    register_startup_and_shutdown(app)
    register_exception(app)

    return app
