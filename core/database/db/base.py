__all__ = [
    'init_db',
]

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.setting import settings


def init_db(app: FastAPI):
    """
    初始化 tortoise-orm
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config=settings.get_orm_base_conf(),
        generate_schemas=True,
        add_exception_handlers=True,  # 生产环境改为False
    )

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.orm.scoping import scoped_session
#
# from core.setting import settings
#
# # 创建数据库连接引擎
# engine = create_engine(
#     settings.SQLALCHEMY_DATABASE_URI,
#     pool_pre_ping=True,
#     connect_args={"options": "-c timezone=Asia/Shanghai"},
#     pool_recycle=3600,
#     pool_size=100,
#     max_overflow=200
# )
# # 数据库连接会话
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # SessionLocal = scoped_session(session_factory)
#
# # 数据库模型基类
# Base = declarative_base()
#
#
# class SessionLocalContext(object):
#     __doc__ = "数据库Session上下文"
#
#     def __init__(self):
#         self.session = SessionLocal()
#
#     def __enter__(self):
#         return self.session
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.session.close()
