# 校园二手交易平台后端

> 基于 Flask + SQLModel + SQLite 的校园二手交易平台后端服务。

## 技术选型

- Web 框架：Flask
- 数据库：SQLite
- ORM：SQLModel
- 认证：JWT（PyJWT）
- 密码加密：PBKDF2-HMAC-SHA256

## 目标与范围

- 提供核心业务接口：用户登录、二手商品列表、商品详情等
- 数据持久化：使用 SQLite，并通过 SQLModel 进行数据访问
- 接口风格：RESTful
- 返回格式：统一 JSON 结构

## 项目结构

```
back/
  src/
    main.py               # Flask 应用入口
    config.py              # 配置（环境变量、数据库等）
    db.py                  # SQLModel 引擎与初始化
    models.py              # 数据模型
    api/
      __init__.py          # API 包
      auth.py              # 用户与认证
      goods.py             # 商品路由
      categories.py        # 分类路由
      favorites.py         # 收藏路由
      wanted.py            # 求购路由
      orders.py            # 订单路由
      reviews.py           # 评价路由
      chat.py              # 聊天路由
    services/
      __init__.py          # 服务层包
      user_service.py      # 用户业务逻辑
      goods_service.py     # 商品业务逻辑
      category_service.py  # 分类业务逻辑
      favorite_service.py  # 收藏业务逻辑
      wanted_service.py    # 求购业务逻辑
      order_service.py     # 订单业务逻辑
      review_service.py    # 评价业务逻辑
      chat_service.py      # 聊天业务逻辑
    utils/
      __init__.py          # 工具包
      response.py          # 通用响应结构
      security.py          # 密码加密与 JWT
      pagination.py        # 分页工具
  start.sh                 # Linux/macOS 启动脚本
  start.bat                # Windows 启动脚本
  requirements.txt         # Python 依赖
  .env.example             # 环境变量示例
```

## 数据模型

### User

- id: int
- username: str（唯一）
- password_hash: str
- nickname: str
- bio: str
- campus: str
- phone: str
- avatar: str
- balance: Decimal
- created_at: datetime

### Category

- id: int
- name: str
- is_active: bool

### Goods

- id: int
- title: str
- description: str
- price: Decimal
- cover_url: str
- seller_id: int（关联 User）
- category_id: int（关联 Category）
- campus: str
- condition_level: str
- status: str（on_sale / offline / sold）
- created_at: datetime
- updated_at: datetime

### GoodsImage

- id: int
- goods_id: int（关联 Goods）
- image_url: str

### Wanted

- id: int
- user_id: int（关联 User）
- title: str
- description: str
- budget_min: Decimal
- budget_max: Decimal
- campus: str
- condition_level: str
- category_id: int
- status: str（active / closed）
- created_at: datetime
- updated_at: datetime

### WantedImage

- id: int
- wanted_id: int
- image_url: str

### Favorite

- id: int
- user_id: int
- item_id: int（可选）
- wanted_id: int（可选）
- created_at: datetime

### TradeOrder

- id: int
- item_id: int
- buyer_id: int
- seller_id: int
- trade_location: str
- remark: str
- status: str（pending / cancelled / completed）
- cancel_reason: str
- created_at: datetime
- updated_at: datetime

### TradeOrderLog

- id: int
- order_id: int
- action: str
- operator_id: int
- created_at: datetime

### Review

- id: int
- order_id: int
- reviewer_id: int
- reviewee_id: int
- rating: int（1-5）
- content: str
- created_at: datetime

### ChatSession

- id: int
- item_id: int（可选）
- wanted_id: int（可选）
- user1_id: int
- user2_id: int
- last_message: str
- last_message_at: datetime
- unread_count: int
- created_at: datetime

### ChatMessage

- id: int
- session_id: int
- sender_id: int
- message_type: str
- content: str
- is_read: bool
- created_at: datetime

## 接口列表

> 统一响应结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 用户与认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/user/register | 用户注册 |
| POST | /api/user/login | 用户登录 |
| GET | /api/user/{id} | 获取用户信息 |
| GET | /api/user/list | 用户列表 |
| DELETE | /api/user/{id} | 删除用户 |
| PUT | /api/user/profile | 更新用户资料 |
| POST | /api/user/avatar/upload | 上传头像 |
| GET | /api/user/wallet | 获取钱包信息 |

### 分类

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/categories | 获取分类列表 |

### 商品

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/items/publish | 发布商品 |
| GET | /api/items/{id} | 商品详情 |
| GET | /api/items/search | 商品搜索 |
| GET | /api/items/user/{userId} | 用户商品列表 |
| POST | /api/items/images/upload | 上传商品图片 |
| PUT | /api/items/{id} | 编辑商品 |
| PUT | /api/items/{id}/offline | 下架商品 |
| PUT | /api/items/{id}/online | 上架商品 |

### 收藏

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/favorites/{itemId} | 收藏商品 |
| DELETE | /api/favorites/{itemId} | 取消收藏 |
| POST | /api/favorites/wanted/{wantedId} | 收藏求购 |
| DELETE | /api/favorites/wanted/{wantedId} | 取消收藏求购 |
| GET | /api/favorites | 我的收藏 |

### 求购

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/wanted | 发布求购 |
| GET | /api/wanted/list | 求购列表 |
| GET | /api/wanted/{id} | 求购详情 |
| PUT | /api/wanted/{id} | 更新求购 |
| DELETE | /api/wanted/{id} | 删除求购 |
| DELETE | /api/wanted/user/{userId} | 删除用户求购 |
| GET | /api/wanted/my | 我的求购 |
| PUT | /api/wanted/{id}/close | 关闭求购 |

### 订单

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/orders | 创建订单 |
| GET | /api/orders/my-buy | 我的买入 |
| GET | /api/orders/my-sell | 我的卖出 |
| PUT | /api/orders/{id}/cancel | 取消订单 |
| PUT | /api/orders/{id}/complete | 完成订单 |

### 评价

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/reviews | 创建评价 |
| PUT | /api/reviews/{id} | 更新评价 |
| DELETE | /api/reviews/{id} | 删除评价 |
| GET | /api/reviews/user/{userId} | 用户评价 |
| GET | /api/reviews/my | 我的评价 |
| GET | /api/reviews/check | 检查是否已评价 |

### 聊天

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/chat/sessions | 创建会话 |
| GET | /api/chat/sessions | 会话列表 |
| POST | /api/chat/messages | 发送消息 |
| GET | /api/chat/sessions/{id}/messages | 消息列表 |
| PUT | /api/chat/sessions/{id}/read | 标记已读 |
| POST | /api/chat/images/upload | 上传聊天图片 |

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

- 创建虚拟环境并安装依赖（Flask、SQLModel、python-dotenv、PyJWT）
- 设置环境变量：
  - DATABASE_URL=sqlite:///./data.db
  - SECRET_KEY=your-secret
- 启动服务：
  - python -m src.main

## 约定

- 所有接口返回 JSON
- 统一错误码与错误信息
- 业务逻辑与路由分离

## TODO

请查看 [TODO.md](TODO.md)。
