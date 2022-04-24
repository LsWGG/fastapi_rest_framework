# Fastapi_rest_framework
    基于fast API编写的ViewSet, 目前仅集成简单表逻辑的增删改查操作；后续会不断完善。

## 安装
1. 创建虚拟环境
2. 安装依赖
    ```bash
    pip install -r r.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

## 使用
    详见apps中，书籍管理demo

## 目前集成功能
1. 自动注册视图集提供路由，需继承 ModelViewSet 类
2. 根据Model类生成Schemas
