# 校园闲置宝 - UniApp 前端项目

## 一、项目概述

本项目是一个基于 **UniApp** 框架开发的校园二手交易平台前端应用，支持微信小程序、H5等多端运行。项目采用模块化设计，接口层与页面层分离，具备完善的Mock数据支持，便于前后端并行开发。

## 二、技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 框架 | UniApp | 最新 |
| 语言 | JavaScript | ES6+ |
| 样式 | SCSS | - |
| 构建工具 | HBuilderX | - |

## 三、目录结构

```
frontend/
├── api/                    # API接口层（核心）
│   ├── index.js           # 请求封装与Mock数据
│   ├── user.js            # 用户模块API
│   ├── item.js            # 商品模块API
│   ├── order.js           # 订单模块API
│   ├── chat.js            # 聊天模块API
│   ├── favorite.js        # 收藏模块API
│   ├── review.js          # 评价模块API
│   ├── wallet.js          # 钱包模块API
│   ├── wanted.js          # 求购模块API
│   └── report.js          # 举报模块API
├── pages/                 # 页面层（24个页面）
│   ├── index/             # 首页
│   ├── wanted/            # 求购
│   ├── publish/           # 发布
│   ├── messages/          # 消息
│   ├── my/                # 我的
│   └── ...                # 其他页面
├── components/            # 组件层
│   └── tab-bar.vue        # 自定义底部导航
├── static/               # 静态资源
│   ├── tabbar/           # TabBar图标
│   └── iconfont/         # 字体图标
├── main.js               # 入口文件
├── pages.json            # 页面路由配置
├── manifest.json         # 应用配置
├── uni.scss              # 全局样式变量
└── README.md             # 项目说明文档
```

## 四、API层设计

### 4.1 统一请求封装

**文件位置**：`api/index.js`

**核心功能**：
- **Base URL统一管理**：后端服务地址 `http://127.0.0.1:5000`
- **Mock模式支持**：通过 `MOCK` 开关切换假数据与真实接口
- **请求方法封装**：`get`, `post`, `put`, `del` 四个基础方法
- **Token认证**：自动在请求头添加 `Authorization: Bearer {token}`
- **响应统一处理**：约定 `code=0` 为成功，其他为失败

**响应格式约定**：
```json
{
    "code": 0,              // 0成功，非0失败
    "message": "success",   // 提示信息
    "data": {}              // 业务数据
}
```

### 4.2 业务模块API划分

| 模块 | API文件 | 主要接口 | 后端端点 |
|------|---------|----------|----------|
| **用户** | `user.js` | 注册、登录、获取信息、更新资料、头像上传 | `/api/user/*` |
| **商品** | `item.js` | 发布、搜索、详情、上下架、图片上传 | `/api/items/*` |
| **订单** | `order.js` | 创建、查询（买入/卖出）、取消、完成 | `/api/orders/*` |
| **聊天** | `chat.js` | 创建会话、发送消息、获取消息列表、标记已读 | `/api/chat/*` |
| **收藏** | `favorite.js` | 添加收藏、取消收藏、获取收藏列表 | `/api/favorites/*` |
| **评价** | `review.js` | 获取评价列表 | `/api/reviews/*` |
| **钱包** | `wallet.js` | 获取余额、交易记录 | `/api/wallet/*` |
| **求购** | `wanted.js` | 发布求购、搜索求购信息 | `/api/wanted/*` |
| **举报** | `report.js` | 提交举报 | `/api/report/*` |

### 4.3 Mock数据机制

**Mock开关**：在 `api/index.js` 中设置
```javascript
export const MOCK = false  // true=使用假数据，false=调用真实接口
```

**Mock数据结构**：包含用户、商品、订单、收藏、聊天等完整数据

**Mock模式优势**：
- 前后端分离开发，前端无需等待后端接口
- 快速验证功能，不依赖网络环境
- 稳定的测试数据支持

## 五、前端与后端数据流转

### 5.1 数据流转流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   前端页面      │     │    API层        │     │    后端服务      │
│  (Vue组件)      │────▶│  (统一封装)      │────▶│  (Flask/Django) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                        │                        │
       │ 调用业务API            │ 添加Token            │ 验证Token
       │ 如 searchItems()       │ 拼接URL             │ 查询数据库
       │                        │ 处理响应            │ 返回数据
       │◀──── 业务数据 ────────│◀─── code=0,data ────│
```

### 5.2 认证机制

**登录流程**：
1. 用户输入账号密码 → 调用 `login()`
2. 后端验证成功 → 返回 `token` 和 `userInfo`
3. 前端存储：`uni.setStorageSync('token', token)`
4. 后续请求自动携带Token

**Token过期处理**：后端返回 `code=401` → 前端清除Token → 跳转登录页

### 5.3 图片上传处理

```javascript
export function uploadImage(filePath) {
    const token = uni.getStorageSync('token')
    return new Promise((resolve, reject) => {
        uni.uploadFile({
            url: BASE_URL + '/api/items/images/upload',
            filePath: filePath,
            name: 'file',
            header: { 'Authorization': 'Bearer ' + token },
            success(res) {
                const data = JSON.parse(res.data)
                if (data.code === 0) {
                    resolve(data.data.url)
                }
            }
        })
    })
}
```

## 六、页面结构

### 6.1 TabBar页面（5个）

| 页面 | 路径 | 功能描述 |
|------|------|----------|
| 首页 | `pages/index/index` | 商品列表、分类筛选、搜索 |
| 求购 | `pages/wanted/wanted` | 求购信息列表 |
| 发布 | `pages/publish/publish` | 发布商品入口 |
| 消息 | `pages/messages/messages` | 聊天会话列表 |
| 我的 | `pages/my/my` | 用户中心 |

### 6.2 二级页面（19个）

| 页面 | 路径 | 功能描述 |
|------|------|----------|
| 商品详情 | `pages/goods-detail/goods-detail` | 查看商品详情 |
| 确认购买 | `pages/buy/buy` | 创建订单 |
| 订单详情 | `pages/order-detail/order-detail` | 订单详情 |
| 我的订单 | `pages/my-orders/my-orders` | 订单列表 |
| 我的发布 | `pages/my-listings/my-listings` | 已发布商品 |
| 心愿单 | `pages/my-wishlist/my-wishlist` | 收藏列表 |
| 我的钱包 | `pages/my-wallet/my-wallet` | 钱包余额、交易记录 |
| 我的信用 | `pages/my-credit/my-credit` | 信用评分 |
| 评价 | `pages/my-review/my-review` | 评价列表 |
| 通知 | `pages/notifications/notifications` | 通知消息 |
| 设置 | `pages/settings/settings` | 系统设置 |
| 登录 | `pages/login/login` | 登录/注册 |
| 编辑资料 | `pages/my-edit/my-edit` | 修改个人信息 |
| 编辑商品 | `pages/goods-edit/goods-edit` | 修改商品信息 |
| 发布表单 | `pages/publish-form/publish-form` | 填写发布信息 |
| 用户主页 | `pages/profile/profile` | 查看他人主页 |
| 聊天 | `pages/chat/chat` | 聊天对话 |
| 求购详情 | `pages/wanted-detail/wanted-detail` | 求购信息详情 |
| 举报 | `pages/report/report` | 举报功能 |

## 七、核心设计亮点

### 7.1 统一响应处理
- 所有接口统一错误提示（`uni.showToast`）
- 统一的成功/失败判断逻辑

### 7.2 灵活的Mock机制
- 一键切换真实/假数据
- Mock数据支持完整的增删改查模拟

### 7.3 模块化API设计
- 按业务模块划分API文件
- 清晰的接口命名规范

### 7.4 全局状态管理
- 使用 `uni.setStorageSync` 存储用户信息和Token
- 跨页面状态共享

## 八、与后端对接规范

### 8.1 后端技术栈建议
- **框架**：Flask / Django / Spring Boot
- **数据库**：MySQL / PostgreSQL
- **认证**：JWT Token
- **文件存储**：本地存储 / 云存储（阿里云OSS等）

### 8.2 接口文档示例

**登录接口**：
```
接口地址：POST /api/user/login
请求体：
{
    "username": "string (必填，用户名)",
    "password": "string (必填，密码)"
}
成功响应：
{
    "code": 0,
    "message": "success",
    "data": {
        "id": 1,
        "username": "testuser",
        "avatar": "",
        "token": "xxx.yyy.zzz"
    }
}
失败响应：
{
    "code": 1001,
    "message": "用户名或密码错误"
}
```

### 8.3 跨域处理

后端需配置CORS：
```python
# Flask示例
from flask_cors import CORS
CORS(app, supports_credentials=True)
```

## 九、运行方式

### 9.1 开发环境
1. 打开HBuilderX
2. 导入项目
3. 选择运行方式（微信小程序/H5/APP）

### 9.2 构建生产版本
1. 在HBuilderX中选择"发行"
2. 选择目标平台
3. 构建产物输出到 `unpackage/build` 目录

## 十、接口列表速查

### 10.1 用户模块
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/user/register` | 用户注册 |
| POST | `/api/user/login` | 用户登录 |
| GET | `/api/user/{id}` | 获取用户信息 |
| PUT | `/api/user/profile` | 更新用户资料 |
| POST | `/api/user/avatar/upload` | 上传头像 |

### 10.2 商品模块
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/categories` | 获取分类列表 |
| POST | `/api/items/publish` | 发布商品 |
| GET | `/api/items/{id}` | 获取商品详情 |
| GET | `/api/items/search` | 搜索商品 |
| GET | `/api/items/user/{userId}` | 获取用户商品列表 |
| PUT | `/api/items/{id}` | 更新商品 |
| PUT | `/api/items/{id}/offline` | 商品下架 |
| PUT | `/api/items/{id}/online` | 商品上架 |
| POST | `/api/items/images/upload` | 上传商品图片 |

### 10.3 订单模块
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/orders` | 创建订单 |
| GET | `/api/orders/my-buy` | 获取购买订单 |
| GET | `/api/orders/my-sell` | 获取卖出订单 |
| PUT | `/api/orders/{id}/cancel` | 取消订单 |
| PUT | `/api/orders/{id}/complete` | 完成订单 |

### 10.4 聊天模块
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/chat/sessions` | 创建会话 |
| GET | `/api/chat/sessions` | 获取会话列表 |
| POST | `/api/chat/messages` | 发送消息 |
| GET | `/api/chat/sessions/{id}/messages` | 获取消息列表 |
| PUT | `/api/chat/sessions/{id}/read` | 标记已读 |

### 10.5 收藏模块
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/favorites` | 获取收藏列表 |
| POST | `/api/favorites/{itemId}` | 添加收藏 |
| DELETE | `/api/favorites/{itemId}` | 取消收藏 |

### 10.6 钱包模块
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/wallet` | 获取钱包信息 |
| GET | `/api/wallet/transactions` | 获取交易记录 |

### 10.7 评价模块
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/reviews` | 获取评价列表 |
| GET | `/api/user-credit` | 获取信用信息 |

### 10.8 求购模块
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/wanted` | 发布求购 |
| GET | `/api/wanted` | 获取求购列表 |
| GET | `/api/wanted/{id}` | 获取求购详情 |

### 10.9 举报模块
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/report` | 提交举报 |

## 十一、注意事项

1. **Mock模式**：开发阶段建议开启Mock模式，便于快速验证功能
2. **Token管理**：确保Token过期后正确处理跳转登录页
3. **图片路径**：使用 `resolveImageUrl()` 函数处理图片URL
4. **网络请求**：所有网络请求必须使用API层封装的方法，禁止直接使用 `uni.request`
5. **错误处理**：所有API调用建议使用 try-catch 包裹，统一处理异常

## 十二、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-05 | 项目初始化，完成核心功能 |
