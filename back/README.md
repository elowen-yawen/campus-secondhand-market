# 校园二手交易平台后端（规划版）

> 本文档仅用于后端项目规划，尚未包含实现代码。

## 技术选型

- Web 框架：Flask
- 数据库：SQLite
- ORM：SQLModel
- 数据迁移：Alembic（规划）
- 认证：基于 JWT 的登录态（规划）

## 目标与范围

- 提供核心业务接口：用户登录、二手商品列表、商品详情等
- 数据持久化：使用 SQLite，并通过 SQLModel 进行数据访问
- 接口风格：RESTful
- 返回格式：统一 JSON 结构

## 项目结构（规划）

```
back/
  src/
    app.py                # Flask 应用入口
    config.py             # 配置（环境变量、数据库等）
    db/
      engine.py           # SQLModel 引擎与 Session
      models.py           # 数据模型
      seed.py             # 初始化数据（可选）
    api/
      __init__.py         # Blueprint 注册
      auth.py             # 登录/注册
      goods.py            # 商品列表与详情
      users.py            # 用户信息
      health.py           # 健康检查
    schemas/
      common.py           # 通用响应结构
      auth.py             # 登录相关请求/响应
      goods.py            # 商品相关请求/响应
    services/
      auth_service.py     # 登录逻辑
      goods_service.py    # 商品业务逻辑
    utils/
      security.py         # 密码加密与 JWT
      pagination.py       # 分页工具
```

## 数据模型（规划）

### User

- id: int
- username: str（唯一）
- password_hash: str
- nickname: str
- created_at: datetime

### Goods

- id: int
- title: str
- description: str
- price: float
- cover_url: str
- seller_id: int（关联 User）
- status: str（如："on_sale"、"sold"）
- created_at: datetime

### GoodsImage（可选）

- id: int
- goods_id: int
- image_url: str

## 接口规划

> 统一响应结构示例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

### 认证

- POST /api/auth/login
  - 入参：username, password
  - 出参：token, user

- POST /api/auth/register（可选）
  - 入参：username, password, nickname
  - 出参：user

### 商品

- GET /api/goods
  - 说明：商品列表，支持分页与筛选
  - 参数：page, size, keyword, status

- GET /api/goods/{id}
  - 说明：商品详情

- POST /api/goods（可选）
  - 说明：发布商品

- PUT /api/goods/{id}（可选）
  - 说明：编辑商品

### 用户

- GET /api/users/me
  - 说明：获取当前用户信息（需要登录）

### 健康检查

- GET /api/health
  - 说明：服务健康状态

## 运行方式

- Linux / macOS：`bash start.sh`
- Windows：双击 `start.bat` 或在命令行中执行 `start.bat`

启动脚本会自动完成以下步骤：

1. 检测 Python 3 环境
2. 创建虚拟环境（`.venv`）
3. 安装依赖（`requirements.txt`）
4. 生成 `.env`（从 `.env.example` 复制，首次启动时）
5. 启动服务（`python -m src.main`）

手动启动（如需跳过脚本）：

- 创建虚拟环境并安装依赖（Flask、SQLModel、python-dotenv 等）
- 设置环境变量：
  - DATABASE_URL=sqlite:///./data.db
  - SECRET_KEY=your-secret
- 启动服务：
  - python -m src.app

## 约定

- 所有接口返回 JSON
- 统一错误码与错误信息
- 业务逻辑与路由分离

## TODO

请查看 [TODO.md](TODO.md)。
