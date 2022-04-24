from tortoise.models import Model
from tortoise import fields

class BaseModel(Model):
    __doc__ = "基础模型"
    id = fields.BigIntField(pk=True, description="ID")
    create_time = fields.DatetimeField(auto_now=True, null=False, description="创建时间")
    update_time = fields.DatetimeField(auto_now_add=True, description="更新时间")

    class Meta:
        abstract = True  # 表示抽象类 不会映射数据库表


class AutoModel(BaseModel):
    __doc__ = "含用户信息基础模型"
    creator = fields.CharField(max_length=32, null=True, description="创建者")
    mender = fields.CharField(max_length=32, null=True, description="修改者")

    class Meta:
        abstract = True  # 表示抽象类 不会映射数据库表
