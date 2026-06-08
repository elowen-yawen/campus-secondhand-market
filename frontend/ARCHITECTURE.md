# 校园闲置宝 - 前端架构图

## 前端架构设计

```mermaid
graphTD
    %% ========== 页面层 ==========
    subgraph Pages["页面层（27个页面）"]
        P1["首页（index）"]
        P2["求购（wanted）"]
        P3["发布（publish）"]
        P4["消息（messages）"]
        P5["我的（my）"]
        P6["商品详情（goods-detail）"]
        P7["购买页面（buy）"]
        P8["订单详情（order-detail）"]
        P9["聊天（chat）"]
        P10["登录（login）"]
        P11["其他页面（16个）"]
    end

    %% ========== API服务层 ==========
    subgraph API["API服务层（模块化）"]
        A1["user.js<br/>用户模块"]
        A2["item.js<br/>商品模块"]
        A3["order.js<br/>订单模块"]
        A4["chat.js<br/>聊天模块"]
        A5["favorite.js<br/>收藏模块"]
        A6["review.js<br/>评价模块"]
        A7["wallet.js<br/>钱包模块"]
        A8["wanted.js<br/>求购模块"]
        A9["report.js<br/>举报模块"]
    end

    %% ========== 请求拦截层 ==========
    subgraph RequestInterceptor["请求拦截层"]
        R1["Token自动注入<br/>Authorization: Bearer {token}"]
        R2["Mock开关控制<br/>MOCK = true/false"]
        R3["请求方法封装<br/>get/post/put/del"]
    end

    %% ========== 响应拦截层 ==========
    subgraph ResponseInterceptor["响应拦截层"]
        S1["统一状态处理<br/>code=0 成功"]
        S2["401未授权处理<br/>清除Token + 跳转登录"]
        S3["错误提示<br/>uni.showToast"]
    end

    %% ========== 本地存储 ==========
    subgraph Storage["本地存储"]
        ST1["token<br/>用户认证令牌"]
        ST2["user<br/>用户信息"]
        ST3["currentOrder<br/>当前订单"]
        ST4["needRefreshHomeGoods<br/>首页刷新标记"]
    end

    %% ========== Mock数据 ==========
    subgraph MockData["Mock数据"]
        M1["用户数据"]
        M2["商品数据"]
        M3["订单数据"]
        M4["聊天数据"]
        M5["收藏数据"]
        M6["评价数据"]
        M7["钱包数据"]
    end

    %% ========== 后端（简化） ==========
    subgraph Backend["后端服务"]
        B1["Flask服务<br/>http://127.0.0.1:5000"]
        B2["API路由分发"]
        B3["安全鉴权"]
        B4["业务逻辑"]
        B5["数据库"]
    end

    %% ========== 页面到API的连接 ==========
    P1 --> A2
    P1 --> A1
    P2 --> A8
    P3 --> A2
    P3 --> A8
    P4 --> A4
    P5 --> A1
    P5 --> A7
    P5 --> A6
    P6 --> A2
    P6 --> A5
    P7 --> A3
    P8 --> A3
    P9 --> A4
    P10 --> A1
    P11 --> A1

    %% ========== API到拦截层的连接 ==========
    A1 --> RequestInterceptor
    A2 --> RequestInterceptor
    A3 --> RequestInterceptor
    A4 --> RequestInterceptor
    A5 --> RequestInterceptor
    A6 --> RequestInterceptor
    A7 --> RequestInterceptor
    A8 --> RequestInterceptor
    A9 --> RequestInterceptor

    %% ========== 请求拦截到响应拦截 ==========
    RequestInterceptor --> ResponseInterceptor

    %% ========== 响应拦截到后端 ==========
    ResponseInterceptor --> B1

    %% ========== 后端内部流程 ==========
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5

    %% ========== 本地存储与页面的连接 ==========
    ST1 --> P10
    ST2 --> P5
    ST3 --> P8
    ST4 --> P1

    %% ========== Mock数据与API的连接 ==========
    M1 --> A1
    M2 --> A2
    M3 --> A3
    M4 --> A4
    M5 --> A5
    M6 --> A6
    M7 --> A7

    %% ========== 样式设置 ==========
    classDef pageStyle fill:#e1f5ff,stroke:#0288d1,stroke-width:2px;
    classDef apiStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef interceptorStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef storageStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef mockStyle fill:#fff8e1,stroke:#ffa000,stroke-width:2px;
    classDef backendStyle fill:#ffebee,stroke:#d32f2f,stroke-width:2px;

    class P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11 pageStyle;
    class A1,A2,A3,A4,A5,A6,A7,A8,A9 apiStyle;
    class R1,R2,R3,S1,S2,S3 interceptorStyle;
    class ST1,ST2,ST3,ST4 storageStyle;
    class M1,M2,M3,M4,M5,M6,M7 mockStyle;
    class B1,B2,B3,B4,B5 backendStyle;
```

## 架构说明

### 1. 页面层（表现层）
- **27个Vue页面**：负责用户交互和界面展示
- **核心页面**：首页、求购、发布、消息、我的
- **功能页面**：商品详情、购买、订单、聊天、登录等

### 2. API服务层（业务层）
- **9个业务模块**：按功能划分，职责清晰
- **模块化设计**：每个模块独立管理相关接口
- **统一调用**：所有页面通过API层与后端交互

### 3. 请求拦截层
- **Token自动注入**：自动在请求头添加认证信息
- **Mock开关**：支持开发阶段使用假数据
- **方法封装**：提供get/post/put/del统一接口

### 4. 响应拦截层
- **统一状态处理**：code=0表示成功
- **401处理**：Token过期自动清除并跳转登录
- **错误提示**：统一的错误信息展示

### 5. 本地存储
- **token**：用户认证令牌
- **user**：用户基本信息
- **currentOrder**：当前订单信息
- **needRefreshHomeGoods**：首页刷新标记

### 6. Mock数据
- **完整数据模拟**：支持用户、商品、订单、聊天等模块
- **开发便利**：无需后端即可验证前端功能

### 7. 后端服务（简化）
- **Flask服务**：运行在 http://127.0.0.1:5000
- **API路由**：接收前端请求
- **安全鉴权**：验证Token有效性
- **业务逻辑**：处理具体业务
- **数据库**：数据持久化

## 数据流走向

```
页面组件 → API模块 → 请求拦截 → 后端服务 → 响应拦截 → 页面组件
                                    ↓
                              本地存储/Mock数据
```

## 技术栈

| 层次 | 技术 |
|------|------|
| 页面层 | UniApp + Vue |
| API层 | JavaScript (ES6+) |
| 拦截层 | uni.request |
| 存储层 | uni.setStorageSync |
| 后端层 | Flask + SQLite |