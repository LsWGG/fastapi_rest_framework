import os
from . import prod_config
from . import dev_config

# 获取环境变量
env = os.getenv("ENV", False)
if env:
    # 如果有虚拟环境 则是 生产环境
    print("----------生产环境启动------------")
    settings = prod_config.settings
else:
    # 没有则是开发环境
    print("----------开发环境启动------------")
    settings = dev_config.settings
