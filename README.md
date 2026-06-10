# 🏫 校园二手交易平台 (Campus Secondhand Market)

> 面向高校学生的校园二手交易平台，支持商品买卖、求购发布、在线聊天、订单管理等功能。

## 📋 项目概述

本项目是一个完整的校园二手交易平台，包含 **后端 API 服务** 和 **前端 UniApp 跨端应用**。后端基于 Python Flask 构建，前端基于 Vue.js + UniApp 开发，可编译为微信小程序、H5 等多端应用。

---

## 🛠️ 技术栈

### 后端 (Backend)

| 技术 | 说明 |
|------|------|
| **Python 3** | 编程语言 |
| **Flask** | Web 框架 |
| **SQLModel** | ORM（SQLAlchemy + Pydantic） |
| **SQLite** | 数据库（轻量级，无需额外安装） |
| **PyJWT** | JWT 身份认证 |
| **PBKDF2-HMAC-SHA256** | 密码加密 |
| **python-dotenv** | 环境变量管理 |
| **RESTful API** | 接口风格，统一 JSON 响应 |

### 前端 (Frontend)

| 技术 | 说明 |
|------|------|
| **Vue.js 2** | 前端框架 |
| **UniApp** | 跨端开发框架（一套代码编译到多端） |
| **SCSS** | CSS 预处理器 |
| **ES6+** | JavaScript 语法 |
| **uni-ui / uni_modules** | UniApp 生态组件 |


## 📁 项目结构

```
campus-secondhand-market/
├── back/                          # 后端服务
│   ├── src/
│   │   ├── main.py                # Flask 应用入口
│   │   ├── config.py              # 配置（环境变量、数据库等）
│   │   ├── db.py                  # SQLModel 引擎与初始化
│   │   ├── models.py              # 数据模型定义
│   │   ├── api/                   # API 路由层
│   │   │   ├── auth.py            # 用户注册/登录
│   │   │   ├── goods.py           # 商品 CRUD
│   │   │   ├── categories.py      # 分类
│   │   │   ├── favorites.py       # 收藏
│   │   │   ├── wanted.py          # 求购
│   │   │   ├── orders.py          # 订单
│   │   │   ├── reviews.py         # 评价
│   │   │   └── chat.py            # 聊天
│   │   ├── services/              # 业务逻辑层
│   │   │   ├── user_service.py
│   │   │   ├── goods_service.py
│   │   │   ├── category_service.py
│   │   │   ├── favorite_service.py
│   │   │   ├── wanted_service.py
│   │   │   ├── order_service.py
│   │   │   ├── review_service.py
│   │   │   └── chat_service.py
│   │   └── utils/                 # 工具类
│   │       ├── response.py        # 统一响应结构
│   │       ├── security.py        # 密码加密 & JWT
│   │       └── pagination.py      # 分页工具
│   ├── requirements.txt           # Python 依赖
│   ├── .env.example               # 环境变量示例
│   ├── start.sh                   # Linux/macOS 启动脚本
│   ├── start.bat                  # Windows 启动脚本
│   └── API.md                     # 接口文档
│
├── frontend/                      # 前端应用
│   ├── App.vue                    # 应用根组件
│   ├── main.js                    # 入口文件
│   ├── pages.json                 # 页面路由配置
│   ├── manifest.json              # UniApp 应用配置
│   ├── uni.scss                   # 全局样式变量
│   ├── index.html                 # H5 入口 HTML
│   ├── api/                       # API 请求封装
│   │   ├── request.js             # 请求拦截器（含 Token 注入）
│   │   └── index.js               # 所有 API 接口定义
│   ├── components/                # 公共组件
│   ├── pages/                     # 页面
│   │   ├── index/                 # 首页（商品列表）
│   │   ├── category/              # 分类浏览
│   │   ├── search/                # 商品搜索
│   │   ├── goods-detail/          # 商品详情
│   │   ├── publish/               # 发布商品
│   │   ├── edit-item/             # 编辑商品
│   │   ├── wanted-publish/        # 发布求购
│   │   ├── wanted-detail/         # 求购详情
│   │   ├── edit-wanted/           # 编辑求购
│   │   ├── login/                 # 登录
│   │   ├── register/              # 注册
│   │   ├── my/                    # 个人中心
│   │   ├── my-items/              # 我的商品
│   │   ├── my-favorites/          # 我的收藏
│   │   ├── my-wanted/             # 我的求购
│   │   ├── my-reviews/            # 我的评价
│   │   ├── user-profile/          # 用户主页
│   │   ├── user-items/            # 用户商品列表
│   │   ├── user-reviews/          # 用户评价列表
│   │   ├── edit-profile/          # 编辑资料
│   │   ├── order/                 # 订单列表
│   │   ├── order-detail/          # 订单详情
│   │   ├── chat-list/             # 会话列表
│   │   ├── chat/                  # 聊天室
│   │   ├── review/                # 评价页面
│   │   ├── wallet/                # 钱包
│   │   ├── settings/              # 设置
│   │   ├── about/                 # 关于
│   │   └── address*/              # 地址管理相关页面
│   └── static/                    # 静态资源
```

---

## ✨ 核心功能

### 👤 用户系统
- 注册 / 登录（JWT 认证）
- 个人资料编辑（昵称、头像、简介、校区、手机号）
- 用户主页浏览（查看他人发布的商品与评价）

### 📦 商品管理
- 发布商品（标题、描述、价格、分类、成色、校区、多图上传）
- 编辑 / 上下架商品
- 商品搜索（关键词、分类、校区、价格范围、成色等多维度筛选）
- 商品详情查看

### 🔍 求购系统
- 发布求购（标题、描述、预算范围、分类、校区、成色）
- 求购列表与详情
- 关闭 / 编辑求购

### ❤️ 收藏功能
- 收藏商品 / 求购
- 我的收藏列表

### 📋 订单管理
- 创建订单（买家发起）
- 订单状态流转：待确认 → 已完成 / 已取消
- 我的买入 / 我的卖出
- 订单操作日志

### ⭐ 评价系统
- 交易完成后互评（1-5 分 + 文字评价）
- 查看用户收到的评价

### 💬 即时聊天
- 创建会话（基于商品或求购）
- 发送文字消息 / 图片消息
- 会话列表（显示最后消息与未读数）
- 标记已读

### 💰 钱包
- 余额查看

### 📍 地址管理
- 收货地址的增删改查

---

## 🚀 快速开始

### 环境要求

- **Python 3.8+**
- **Node.js 14+**（前端开发时需要）
- **HBuilderX**（推荐，用于 UniApp 开发与小程序编译）

### 1️⃣ 启动后端服务

#### Windows

```bash
cd back
start.bat
```

#### Linux / macOS

```bash
cd back
bash start.sh
```

启动脚本会自动完成：
1. 检测 Python 3 环境
2. 创建虚拟环境 `.venv`
3. 安装依赖（`pip install -r requirements.txt`）
4. 生成 `.env` 配置文件（首次启动时从 `.env.example` 复制）
5. 启动 Flask 开发服务器（默认端口 **5000**）

#### 手动启动

```bash
cd back

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 为 .env 并修改）
cp .env.example .env

# 启动服务
python -m src.main
```

#### 环境变量说明（`.env`）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接地址 | `sqlite:///./data.db` |
| `SECRET_KEY` | JWT 签名密钥 | 需自行设置 |

### 2️⃣ 启动前端应用

#### 使用 HBuilderX（推荐）

1. 打开 HBuilderX
2. 导入 `frontend/` 目录
3. 选择运行目标：
   - **微信小程序**：点击「运行」→「运行到小程序模拟器」→「微信开发者工具」
   - **H5**：点击「运行」→「运行到浏览器」
4. 确保后端服务已启动，并在 `frontend/api/request.js` 中配置正确的后端地址

#### 使用 CLI 编译

```bash
cd frontend

# 安装依赖
npm install

# 编译到 H5
npm run dev:h5

# 编译到微信小程序
npm run dev:mp-weixin
```

---

## 🔗 API 接口概览

所有接口返回统一 JSON 格式：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

| 模块 | 主要接口 |
|------|----------|
| **用户认证** | `POST /api/user/register`、`POST /api/user/login`、`PUT /api/user/profile` |
| **商品** | `POST /api/items/publish`、`GET /api/items/search`、`GET /api/items/{id}` |
| **分类** | `GET /api/categories` |
| **收藏** | `POST /api/favorites/{itemId}`、`GET /api/favorites` |
| **求购** | `POST /api/wanted`、`GET /api/wanted/list` |
| **订单** | `POST /api/orders`、`GET /api/orders/my-buy`、`GET /api/orders/my-sell` |
| **评价** | `POST /api/reviews`、`GET /api/reviews/user/{userId}` |
| **聊天** | `POST /api/chat/sessions`、`POST /api/chat/messages`、`GET /api/chat/sessions/{id}/messages` |

> 完整接口文档请查看 [back/API.md](back/API.md)

---

## 🗄️ 数据模型

核心数据实体：**User（用户）**、**Goods（商品）**、**Category（分类）**、**Wanted（求购）**、**Favorite（收藏）**、**TradeOrder（订单）**、**Review（评价）**、**ChatSession（会话）**、**ChatMessage（消息）**

详细字段定义请查看 [back/src/models.py](back/src/models.py) 或 [back/README.md](back/README.md)。

---

## 📄 开源协议

本项目仅供学习交流使用。
