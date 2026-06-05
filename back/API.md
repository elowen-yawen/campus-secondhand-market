# 后端 API 定义（参考 YatIdle）

> 本文档根据 YatIdle 后端控制器接口整理，作为当前项目后端 API 定义参考。

## 通用说明

- 基础路径：/api
- 返回格式：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

- 认证方式：部分接口通过 `userId` 作为请求参数（未体现统一鉴权中间件）
- 文件上传：`multipart/form-data`，字段名为 `file`

## 用户与认证

- POST /api/user/register
  - 说明：注册并返回登录信息
  - Body：`RegisterDTO`（username, password, nickname, bio, campus）

- POST /api/user/login
  - 说明：登录并返回登录信息
  - Body：`LoginDTO`（username, password）

- GET /api/user/{id}
  - 说明：按 ID 获取用户信息

- GET /api/user/list
  - 说明：获取用户列表

- DELETE /api/user/{id}
  - 说明：删除用户

- PUT /api/user/profile
  - 说明：更新用户资料
  - Body：`UpdateProfileDTO`（userId, password, phone, avatar, nickname, bio, campus）

- POST /api/user/avatar/upload
  - 说明：上传头像
  - 表单：file
  - 返回：url

- GET /api/user/wallet
  - 说明：获取钱包信息
  - Query：userId

## 分类

- GET /api/categories
  - 说明：获取分类列表

## 商品

- POST /api/items/publish
  - 说明：发布商品
  - Body：`ItemPublishDTO`（userId, title, campus, conditionLevel, description, price, categoryId, imageUrls）

- GET /api/items/{id}
  - 说明：商品详情

- GET /api/items/search
  - 说明：商品搜索
  - Query：keyword, categoryId, campus, conditionLevel, minPrice, maxPrice, priceSort, page, size

- GET /api/items/user/{userId}
  - 说明：获取用户发布商品
  - Query：status, page, size

- POST /api/items/images/upload
  - 说明：上传商品图片
  - 表单：file
  - 返回：url

- PUT /api/items/{id}
  - 说明：编辑商品
  - Body：`ItemPublishDTO`

- PUT /api/items/{id}/offline
  - 说明：下架商品
  - Query：userId

- PUT /api/items/{id}/online
  - 说明：上架商品
  - Query：userId

## 收藏

- POST /api/favorites/{itemId}
  - 说明：收藏商品
  - Query：userId

- DELETE /api/favorites/{itemId}
  - 说明：取消收藏商品
  - Query：userId

- POST /api/favorites/wanted/{wantedId}
  - 说明：收藏求购
  - Query：userId

- DELETE /api/favorites/wanted/{wantedId}
  - 说明：取消收藏求购
  - Query：userId

- GET /api/favorites
  - 说明：我的收藏列表
  - Query：userId

## 求购

- POST /api/wanted
  - 说明：发布求购
  - Body：`CreateWantedDTO`（userId, title, budgetMin, budgetMax, campus, conditionLevel, description, categoryId, imageUrls）

- GET /api/wanted/list
  - 说明：求购列表
  - Query：campus, categoryId, status

- GET /api/wanted/{id}
  - 说明：求购详情

- PUT /api/wanted/{id}
  - 说明：更新求购
  - Body：`CreateWantedDTO`

- DELETE /api/wanted/{id}
  - 说明：删除求购

- DELETE /api/wanted/user/{userId}
  - 说明：删除用户全部求购

- GET /api/wanted/my
  - 说明：我的求购
  - Query：userId

- PUT /api/wanted/{id}/close
  - 说明：关闭求购
  - Query：userId

## 订单

- POST /api/orders
  - 说明：创建订单
  - Query：userId
  - Body：`CreateOrderDTO`（itemId, tradeLocation, remark）

- GET /api/orders/my-buy
  - 说明：我的买入订单
  - Query：userId

- GET /api/orders/my-sell
  - 说明：我的卖出订单
  - Query：userId

- PUT /api/orders/{id}/cancel
  - 说明：取消订单
  - Query：userId
  - Body：`CancelOrderDTO`（cancelReason，可选）

- PUT /api/orders/{id}/complete
  - 说明：完成订单
  - Query：userId

## 评价

- POST /api/reviews
  - 说明：创建评价
  - Query：userId
  - Body：`CreateReviewDTO`（orderId, revieweeId, rating, content）

- PUT /api/reviews/{id}
  - 说明：更新评价
  - Query：userId
  - Body：`CreateReviewDTO`

- DELETE /api/reviews/{id}
  - 说明：删除评价
  - Query：userId

- GET /api/reviews/user/{userId}
  - 说明：获取用户的评价与统计

- GET /api/reviews/my
  - 说明：我的评价列表
  - Query：userId

- GET /api/reviews/check
  - 说明：检查是否已评价
  - Query：orderId, userId

## 聊天

- POST /api/chat/sessions
  - 说明：创建聊天会话
  - Query：userId
  - Body：`CreateChatSessionDTO`（itemId, wantedId）

- GET /api/chat/sessions
  - 说明：我的会话列表
  - Query：userId

- POST /api/chat/messages
  - 说明：发送消息
  - Query：userId
  - Body：`SendMessageDTO`（sessionId, messageType, content）

- GET /api/chat/sessions/{sessionId}/messages
  - 说明：会话消息列表
  - Query：userId

- PUT /api/chat/sessions/{sessionId}/read
  - 说明：标记会话已读
  - Query：userId

- POST /api/chat/images/upload
  - 说明：上传聊天图片
  - 表单：file
  - 返回：url
