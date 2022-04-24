from enum import Enum, IntEnum


class Gender(str, Enum):
    Male = "男"
    Female = "女"


class StateEnum(IntEnum):
    """
    允许登录的权限,1:允许,2:禁用
    """
    allow = 1
    forbidden = 2
