# CommerceBot - 智营电商智能体

> 基于多Agent架构和ReAct范式的电商智能运营系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.4+-brightgreen.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目概述

CommerceBot 是一个面向电商卖家的AI智能运营系统，通过多Agent协作实现运营自动化。系统采用**ReAct（推理-行动）范式**，像经验丰富的运营专家一样主动发现问题、分析问题并执行解决方案。

### 核心特性

- **多Agent架构**：Master Agent统筹 + 6个专业Agent协作
- **自然语言交互**：对话式完成销售分析、定价、库存、物流等操作
- **数据驱动决策**：基于真实数据的智能分析和建议
- **实时预警推送**：库存不足、物流异常等情况主动通知
- **多店铺管理**：支持一个用户管理多个店铺

### 技术栈

| 层级 | 技术选型 |
|------|----------|
| Agent框架 | LangGraph + LangChain |
| LLM引擎 | OpenRouter (step-3.5-flash:free) |
| 后端框架 | FastAPI + SQLAlchemy 2.0 |
| 数据库 | SQLite (开发) / MySQL 8.0 (生产) |
| 前端框架 | Vue 3 + TypeScript + TailwindCSS |
| 图表库 | ECharts |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- SQLite / MySQL 8.0

### 一键启动

```bash
# 克隆项目
git clone https://github.com/your-repo/commerce-bot.git
cd commerce-bot

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库并生成测试数据
python start_backend.py

# 启动后端服务
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8765 --reload

# 安装前端依赖并启动
cd frontend
npm install
npm run dev
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端界面 | http://localhost:3445 |
| 后端API | http://localhost:8765 |
| API文档 | http://localhost:8765/docs |

### 测试账号

| 用户名 | 密码 | 说明 |
|--------|------|------|
| demo_user | demo123 | 演示账号（3个店铺） |
| test_user1 | password123 | 测试账号 |
| premium_user | premium123 | 高级用户 |

## 项目结构

```
commerce-bot/
├── backend/                    # 后端代码
│   ├── api/v1/                # API路由
│   │   ├── auth.py           # 认证接口
│   │   ├── shops.py          # 店铺管理
│   │   ├── products.py       # 商品管理
│   │   ├── orders.py         # 订单管理
│   │   ├── dashboard.py      # 数据看板
│   │   └── chat.py           # AI对话接口
│   ├── core/                  # 核心模块
│   │   ├── seed_data.py      # 测试数据生成
│   │   └── agent/            # Agent系统（待实现）
│   ├── models/                # ORM模型
│   │   ├── user.py           # 用户模型
│   │   ├── shop.py           # 店铺模型
│   │   ├── product.py        # 商品模型
│   │   ├── order.py          # 订单模型
│   │   ├── logistics.py      # 物流模型
│   │   ├── review.py         # 评价模型
│   │   ├── customer.py       # 客户模型
│   │   ├── promotion.py      # 促销模型
│   │   └── analytics.py      # 统计模型
│   ├── schemas/               # Pydantic模型
│   ├── database.py            # 数据库配置
│   └── main.py                # FastAPI应用入口
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── api/              # API接口层
│   │   ├── components/       # 公共组件
│   │   ├── views/            # 页面视图
│   │   │   ├── LoginView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── ChatView.vue
│   │   │   ├── ShopsView.vue
│   │   │   ├── ProductsView.vue
│   │   │   ├── OrdersView.vue
│   │   │   ├── InventoryView.vue
│   │   │   └── LogisticsView.vue
│   │   ├── stores/           # Pinia状态管理
│   │   ├── router/           # 路由配置
│   │   └── types/            # TypeScript类型
│   └── package.json
├── docs/                       # 项目文档
├── CLAUDE.md                   # 项目开发规范
├── requirements.txt            # Python依赖
├── .env.example                # 环境变量模板
└── README.md                   # 本文件
```

## 多Agent架构

### 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                      Master Agent                           │
│              (意图识别 + 任务编排 + 路由)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────┬───────┬──┴────┬───────┬───────────┐
    │           │       │        │       │           │
    ▼           ▼       ▼        ▼       ▼           ▼
Data      Pricing  Inventory  Logistics  Report  Knowledge
Agent      Agent    Agent      Agent     Agent    Agent
```

### Agent职责

| Agent | 职责 | 关键能力 |
|-------|------|----------|
| **Master Agent** | 意图识别、任务分解、子Agent调度 | 路由决策、上下文管理 |
| **Data Agent** | 数据获取、分析、指标计算 | 销售分析、趋势预测 |
| **Pricing Agent** | 价格分析、竞品对比、定价建议 | 智能定价、利润优化 |
| **Inventory Agent** | 库存查询、销量预测、补货建议 | 库存预警、需求预测 |
| **Logistics Agent** | 物流查询、异常识别、状态更新 | 物流跟踪、异常处理 |
| **Report Agent** | 数据汇总、图表生成、报告输出 | 自动报表、可视化 |
| **Knowledge Agent** | 知识检索、FAQ匹配、客服回复 | 智能客服、知识库 |

### ReAct循环示例

```
User: "帮我分析一下上周的销售情况"

Thought: 用户想了解销售情况，需要获取上周的订单数据
Action: fetch_orders({"date_range": "last_7_days"})
Observation: 获取到156条订单记录

Thought: 有了订单数据，现在计算GMV
Action: calculate_gmv({"orders": [...]})
Observation: GMV = 158,000元

Thought: 还需要计算客单价和环比增长
Action: calculate_aov({"orders": [...]})
Observation: AOV = 1012.82元

Final Answer: 上周销售情况：GMV 15.8万元，订单156单，客单价1012.82元...
```

## 数据库设计

### 核心业务表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| users | 用户表 | user_id, username, email, password_hash |
| shops | 店铺表 | shop_id, user_id, shop_name, shop_type, status |
| products | 商品表 | product_id, shop_id, sku, name, category, cost_price, current_price |
| orders | 订单表 | order_id, shop_id, product_id, order_no, status, total_amount |
| logistics | 物流表 | logistics_id, order_id, tracking_number, carrier, current_status |
| product_reviews | 商品评价 | review_id, product_id, rating, content, seller_reply |
| customers | 客户表 | customer_id, shop_id, name, level, total_orders, total_amount |
| promotions | 促销活动 | promotion_id, shop_id, name, type, status, discount_value |
| shop_analytics | 店铺统计 | analytics_id, shop_id, stat_date, gmv, order_count, page_views |

### 测试数据规模

| 模型 | 数量 |
|------|------|
| 用户 | 8 |
| 店铺 | 18 |
| 商品 | ~1,000 |
| 订单 | ~6,800 |
| 物流记录 | ~4,750 |
| 客户 | ~2,100 |
| 商品评价 | ~3,260 |
| 促销活动 | 100 |
| 统计数据 | ~1,080 |

## API接口

### 认证接口

```
POST /api/v1/auth/register  # 用户注册
POST /api/v1/auth/login     # 用户登录
GET  /api/v1/auth/me        # 获取当前用户信息
```

### 店铺管理

```
GET    /api/v1/shops         # 获取店铺列表
POST   /api/v1/shops         # 创建店铺
GET    /api/v1/shops/{id}    # 获取店铺详情
PUT    /api/v1/shops/{id}    # 更新店铺信息
DELETE /api/v1/shops/{id}    # 删除店铺
```

### 商品管理

```
GET    /api/v1/products      # 获取商品列表
POST   /api/v1/products      # 创建商品
GET    /api/v1/products/{id} # 获取商品详情
PUT    /api/v1/products/{id} # 更新商品信息
DELETE /api/v1/products/{id} # 删除商品
```

### 订单管理

```
GET /api/v1/orders           # 获取订单列表
GET /api/v1/orders/{id}      # 获取订单详情
PUT /api/v1/orders/{id}      # 更新订单状态
```

### 仪表盘

```
GET /api/v1/dashboard/metrics?shop_id={id}  # 获取看板指标
```

### AI对话

```
POST /api/v1/chat            # 发送消息给AI助手
```

## 功能模块

### 1. 数据看板
- 核心指标卡片（GMV、订单量、客单价、预警数）
- 销售趋势图表
- 品类分布图表
- 热销商品列表
- 最近订单列表
- 快速操作入口

### 2. 店铺管理
- 店铺列表展示
- 创建/编辑/删除店铺
- 多店铺切换

### 3. 商品管理
- 商品列表（搜索、筛选、分页）
- 添加/编辑商品
- SKU管理
- 智能定价建议

### 4. 订单管理
- 订单列表（状态筛选）
- 订单详情查看
- 订单状态更新

### 5. 库存管理
- 库存状态统计
- 低库存预警
- 补货建议

### 6. 物流管理
- 物流列表
- 物流单号查询
- 物流轨迹详情
- 异常订单处理

### 7. AI助手
- 自然语言交互
- 销售分析
- 智能定价
- 库存查询
- 物流跟踪

## 开发指南

### 后端开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/

# 代码格式化
black backend/
isort backend/
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 开发运行
npm run dev

# 构建生产版本
npm run build
```

### 代码规范

- 遵循 `CLAUDE.md` 中定义的规范
- Python代码使用类型注解
- Vue组件使用 `<script setup>` 语法
- 所有文件头包含任务描述和修改时间

## 配置说明

### 环境变量

创建 `.env` 文件：

```bash
# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///commerce_bot.db
# 生产环境使用MySQL
# DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/commerce_bot

# JWT配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# LLM配置
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODEL=stepfun/step-3.5-flash:free

# 服务器配置
HOST=0.0.0.0
PORT=8765

# CORS配置
CORS_ORIGINS=http://localhost:3445,http://localhost:3446
```

## 常见问题

### Q: 如何切换到MySQL数据库？

修改 `.env` 文件中的 `DATABASE_URL`：

```bash
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/commerce_bot
```

### Q: 端口被占用怎么办？

修改后端端口：
```bash
python -m uvicorn backend.main:app --port 8766
```

修改前端端口：编辑 `frontend/package.json` 中的 `--port` 参数。

### Q: 如何重新生成测试数据？

```bash
# 删除旧数据库
rm commerce_bot.db

# 重新生成
python start_backend.py
```

## 路线图

- [ ] 完整的Agent系统实现（LangGraph + ReAct）
- [ ] WebSocket实时通信
- [ ] 定时任务（库存预警、报表生成）
- [ ] 竞品价格爬取
- [ ] 更多图表类型
- [ ] 数据导出功能
- [ ] 单元测试和E2E测试

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目地址: [GitHub](https://github.com/your-repo/commerce-bot)
- 问题反馈: [Issues](https://github.com/your-repo/commerce-bot/issues)

---

**版本**: v1.0.0 | **最后更新**: 2026-03-30
