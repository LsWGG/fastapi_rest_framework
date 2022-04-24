import os
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    __doc__ = "开发环境配置"

    API_V1_STR: str = "/api/v1"
    # ---------------- apps 配置 ----------------
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "http://127.0.0.1:8001")
    # SECRET_KEY 记得保密生产环境 不要直接写在代码里面
    SECRET_KEY: str = "(-ASp+_)-Ulhw0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE"
    # token过期时间 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # ---------------- 数据库配置 ----------------
    DB_HOST: str = os.getenv("DB_HOST", '127.0.0.1')
    DB_PORT: int = os.getenv("DB_PORT", 5432)
    DB_USER: str = os.getenv("DB_USER", 'postgres')
    DB_PWD: str = os.getenv("DB_PWD", 'admin')
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "public")
    DB_DATABASE: str = os.getenv("DB_DATABASE", 'dev')
    DB_MAX_SIZE: int = os.getenv("DB_MAX_SIZE", 100)
    DB_ENGINE: str = os.getenv("DB_ENGINE", "tortoise.backends.asyncpg")

    def get_orm_base_conf(self) -> dict:
        return {
            'connections': {
                'default': {
                    'engine': self.DB_ENGINE,
                    'credentials': {
                        'host': self.DB_HOST,
                        'port': self.DB_PORT,
                        'user': self.DB_USER,
                        'password': self.DB_PWD,
                        'database': self.DB_DATABASE,
                        'minsize': 1,
                        'maxsize': self.DB_MAX_SIZE,
                        'schema': self.DB_SCHEMA,
                    }
                },
            },
            'apps': {
                'models': {
                    'models': [
                        'apps.models.__init__'
                    ],
                    'default_connection': 'default',
                },
            },
            'use_tz': False,
            'timezone': 'Asia/Shanghai'
        }

    # ---------------- Redis配置 ----------------
    REDIS_HOST: str = os.environ.get('REDIS_HOST', '127.0.0.1')
    REDIS_PORT: int = os.environ.get('REDIS_PORT', '6379')
    REDIS_PWD: str = os.environ.get('REDIS_PASSWORD')
    REDIS_DEFAULT_DB = int(os.environ.get('REDIS_DEFAULT_DB', 3))

    # ----------------- Elasticsearch配置 ----------------
    ES_HOST: str = os.getenv("ES_HOST", 'http://127.0.0.1:9200')
    ES_USERNAME: str = os.getenv("ES_USERNAME")
    ES_PASSWORD: str = os.getenv("ES_PASSWORD")


# 实例化配置对象
settings = Settings()
