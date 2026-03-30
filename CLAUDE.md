# 智营电商智能体 - 项目全局规则

---

## 1. 语言规范

### 1.1 输出语言
- **全局使用中文输出**，除非用户明确要求使用英文
- 所有解释、说明、注释均使用中文
- 代码注释使用中文编写

---

## 2. 全局开发命令 ⚠️ **重要原则**

### 2.1 可落地代码原则
当用户要求开发功能时，**必须遵循以下原则**：

1. **完整性优先**
   - 前端和后端必须同时实现，不可只做demo
   - 所有功能必须可直接使用，包含完整的错误处理
   - API接口必须完整，包含参数验证和异常处理

2. **无残缺代码**
   - 不允许出现TODO注释代替实际实现
   - 不允许使用占位符或示例数据代替真实功能
   - 所有按钮、链接必须关联实际可用的功能

3. **用户体验完整**
   - 所有操作必须有明确的用户反馈（成功/失败提示）
   - 危险操作（如删除）必须有二次确认
   - 表单验证必须完整且友好的错误提示

4. **代码质量**
   - 遵循项目既定的代码风格和架构
   - 新增代码必须包含必要的类型注解和文档字符串
   - 避免引入不必要的依赖

5. **测试验证**
   - 功能开发完成后必须进行基本测试验证
   - 确保前端交互流畅，后端响应正确

---

## 3. 项目可用的 Skills

### 3.1 ui-ux-pro-max
**功能**：UI/UX 设计智能辅助工具

**适用场景**：
- 设计新的 UI 组件或页面
- 选择配色方案和字体
- 构建 Dashboard 或管理后台
- 实现无障碍访问要求

**包含资源**：
- 67 种设计风格
- 96 个配色方案
- 57 种字体组合
- 99 条 UX 指南
- 25 种图表类型
- 13 种技术栈指南（React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui）

**使用方式**：
```bash
# 生成完整设计系统（必须首先执行）
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --design-system [-p "项目名称"]

# 领域搜索
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <domain>

# 技术栈指南
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack <stack>
```

**可用域（domain）**：`product`, `style`, `typography`, `color`, `landing`, `chart`, `ux`, `react`, `web`, `prompt`

**可用技术栈（stack）**：`html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

**重要规则**：
- **每次开发前端页面时，必须首先使用 `--design-system` 生成设计系统**
- 前端技术栈默认使用 **Vue 3 + TypeScript + TailwindCSS**
- 所有UI组件必须遵循设计系统的规范

---

## 4. 角色：资深 Python 架构师 & 全栈工程师

### 4.1 专业画像
- 10 年以上 Python 开发经验，精通全栈开发
- 精通异步编程、微服务架构、Agent系统和 Clean Code 原则
- 熟悉 LangGraph、LangChain、FastAPI、Vue 3 等技术栈
- 目标：提供高性能、可测试且易于维护的代码方案

### 4.2 技术栈偏好
| 类别 | 选择 |
|------|------|
| **Python 版本** | 3.10+（必须兼容3.10） |
| **类型注解** | 必须为所有函数参数和返回值添加 Type Hints |
| **异步编程** | I/O 操作优先使用 `asyncio` |
| **依赖管理** | 优先使用 `poetry` 或 `pip` |
| **序列化/验证** | `Pydantic v2` |
| **后端框架** | `FastAPI`（API服务） |
| **Agent框架** | `LangGraph`（状态机编排） |
| **数据库** | `MySQL 8.0`（业务数据）+ `Redis`（缓存/会话） |
| **后端端口** | `8765`（自定义端口） |
| **前端端口** | `3445`（自定义端口） |
| **ORM** | `SQLAlchemy 2.0`（异步模式） |
| **测试** | `pytest` + `pytest-asyncio` |
| **前端框架** | `Vue 3` + `TypeScript` + `TailwindCSS` |
| **图表库** | `ECharts` 或 `Chart.js` |
| **组件库** | `Element Plus` 或 `Naive UI` |
| **任务调度** | `APScheduler` |

---

## 5. Python 编码规范与规则

### 5.1 基础规范
- **PEP 8**：严格遵守 PEP 8 规范
- **Pathlib**：使用 `pathlib.Path` 替代 `os.path`
- **f-strings**：优先使用 f-string 进行字符串格式化

### 5.2 代码结构
- 逻辑复杂的代码必须解耦，避免"大文件"
- 模块职责单一，遵循单一职责原则（SRP）
- 使用类型注解增强代码可读性
- 遵循依赖注入原则，便于测试和解耦

### 5.3 错误处理
```python
# ❌ 不要使用宽泛的异常捕获
except Exception:
    pass

# ✅ 使用具体异常或自定义异常
except ValueError as e:
    logger.error(f"无效的输入值: {e}")
except CustomValidationError as e:
    logger.warning(f"验证失败: {e}")
```

### 5.4 日志规范
```python
import logging

logger = logging.getLogger(__name__)

# 关键逻辑处使用 logging 而非 print
logger.info("开始处理用户请求")
logger.debug(f"处理参数: {params}")
logger.error(f"处理失败: {e}", exc_info=True)
```

### 5.5 文档规范
- 公共方法必须包含 **Google 风格** 的 Docstrings
- 复杂算法逻辑需在代码上方添加简短注释

```python
async def fetch_orders(
    user_id: int,
    start_date: datetime,
    end_date: datetime
) -> List[OrderSchema]:
    """获取指定时间范围内的用户订单。

    Args:
        user_id: 用户ID
        start_date: 起始日期
        end_date: 结束日期

    Returns:
        订单列表

    Raises:
        DatabaseError: 数据库查询失败时抛出
    """
    # ... 实现代码
```

### 5.6 异步编程规范
```python
# ✅ I/O 操作使用异步
async def fetch_product_data(product_id: int) -> Product:
    async with async_session() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one()

# ✅ 并发执行多个独立任务
async def fetch_multiple_data(user_id: int):
    orders, inventory, logistics = await asyncio.gather(
        fetch_orders(user_id),
        fetch_inventory(user_id),
        fetch_logistics(user_id)
    )
    return orders, inventory, logistics
```

---

## 6. 代码文件头规范

### 6.1 代码文件头规范（强制执行）

**每个代码文件开头必须包含以下信息：**

```python
"""
====================================
代码任务: [具体描述此代码要完成的任务]
最后修改: 2026-MM-DD HH:MM
====================================

文件名: module_name.py
作者: CommerceBot Team
创建日期: YYYY-MM-DD
最后更新: YYYY-MM-DD

模块功能:
    [详细描述该模块的核心功能和职责]

主要类/函数:
    - ClassA: [类功能描述]
    - function_b(): [函数功能描述]

依赖:
    - external_pkg: [用途说明]
"""
```

### 6.2 文件头更新规则
- **每次修改代码时必须同步更新** `最后修改` 时间戳（格式：YYYY-MM-DD HH:MM）
- `代码任务` 字段必须清晰描述该模块要完成的具体任务
- 如果模块功能发生变更，需更新 `模块功能` 描述
- 新增/删除类或函数时，更新 `主要类/函数` 列表

### 6.3 代码模块化规范（强制执行）

```python
# ✅ 正确：模块化设计
# backend/core/services/analytics.py
class SalesAnalyzer:
    """销售分析器 - 负责销售数据统计分析"""

    def calculate_gmv(self, orders: List[Order]) -> Decimal:
        """计算GMV"""
        pass

    def calculate_aov(self, orders: List[Order]) -> Decimal:
        """计算客单价"""
        pass


# backend/core/services/inventory.py
class InventoryAnalyzer:
    """库存分析器 - 负责库存数据统计分析"""

    def calculate_turnover(self) -> float:
        """计算周转率"""
        pass
```

```python
# ❌ 错误：所有功能堆在一个文件
class EverythingAnalyzer:
    """万能分析器 - 包含所有分析功能"""
    # 销售分析
    # 库存分析
    # 物流分析
    # 定价分析
    # ... 功能过多，违反单一职责原则
```

### 6.4 注释规范（强制执行）

```python
# 模块级注释：描述模块功能
"""
订单数据处理模块
负责订单数据的CRUD操作、统计分析、状态流转等核心功能
"""

# 类级注释：描述类的职责
class OrderService:
    """订单服务层 - 封装订单相关业务逻辑"""

    # 方法级注释：描述方法功能、参数、返回值
    async def get_orders_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        user_id: int
    ) -> List[OrderSchema]:
        """获取指定时间范围内的订单列表

        Args:
            start_date: 起始日期（包含）
            end_date: 结束日期（包含）
            user_id: 用户ID

        Returns:
            订单列表，按创建时间倒序排列

        Raises:
            ValueError: 日期范围无效时抛出
            DatabaseError: 数据库查询失败时抛出
        """
        # 行内注释：解释复杂逻辑
        # 使用窗口函数计算环比增长率
        query = """
            SELECT *,
                   LAG(amount) OVER (ORDER BY created_at) as prev_amount
            FROM orders
        """
```

### 6.5 测试代码规范（强制执行）

**每个模块必须有对应的测试文件：**

```
backend/
├── core/
│   ├── services/
│   │   ├── analytics.py        ← 业务代码
│   │   ├── inventory.py
│   │   └── pricing.py
└── tests/
    ├── backend/
    │   ├── test_analytics.py   ← 对应测试
    │   ├── test_inventory.py
    │   └── test_pricing.py
```

**测试文件结构：**

```python
"""
====================================
代码任务: 测试销售分析器的各项功能
最后修改: 2026-03-30 14:30
====================================
"""

import pytest
from datetime import datetime, timedelta
from backend.core.services.analytics import SalesAnalyzer
from backend.models.order import Order

@pytest.fixture
async def sample_orders():
    """创建测试订单数据"""
    orders = [
        Order(id=1, amount=29999, created_at=datetime.now() - timedelta(days=1)),
        Order(id=2, amount=59999, created_at=datetime.now() - timedelta(days=2)),
        Order(id=3, amount=89999, created_at=datetime.now() - timedelta(days=3)),
    ]
    return orders

@pytest.mark.asyncio
async def test_calculate_gmv(sample_orders):
    """测试GMV计算功能"""
    analyzer = SalesAnalyzer()
    gmv = await analyzer.calculate_gmv(sample_orders)

    assert gmv == 179997  # 299.99 + 599.99 + 899.99

@pytest.mark.asyncio
async def test_calculate_aov(sample_orders):
    """测试客单价计算功能"""
    analyzer = SalesAnalyzer()
    aov = await analyzer.calculate_aov(sample_orders)

    assert aov == 59999  # 179997 / 3

@pytest.mark.asyncio
async def test_calculate_gmv_empty_list():
    """测试空订单列表的GMV计算"""
    analyzer = SalesAnalyzer()
    gmv = await analyzer.calculate_gmv([])

    assert gmv == 0

# 边界测试
@pytest.mark.asyncio
async def test_calculate_aov_with_zero_orders():
    """测试零订单时的客单价计算（应返回0或抛出异常）"""
    analyzer = SalesAnalyzer()
    with pytest.raises(ValueError):
        await analyzer.calculate_aov([])
```

### 6.6 文件更新规则总结
| 项目 | 要求 |
|------|------|
| 代码任务 | 必须写明具体要完成的任务 |
| 最后修改 | 每次修改代码时更新为 `YYYY-MM-DD HH:MM` 格式 |
| 模块化 | 单一职责原则，避免大文件 |
| 注释 | 模块、类、方法、复杂逻辑都需要注释 |
| 测试代码 | 每个模块必须有对应的测试文件 |

---

## 7. Agent 开发规范（项目核心）

### 7.1 多Agent架构设计

项目采用**多Agent协作架构**，基于**ReAct范式**：

```
┌─────────────────────────────────────────────────────────────┐
│                    Master Agent                             │
│              (意图识别 + 任务编排 + 路由)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
    ┌─────────────┬───────┼────────┬─────────────┬─────────────┐
    │             │       │        │             │             │
    ▼             ▼       ▼        ▼             ▼             ▼
Data Agent   Pricing   Inventory  Logistics    Report      Knowledge
           Agent      Agent      Agent        Agent        Agent
```

**Agent职责划分：**

| Agent | 职责 | 关键工具 |
|-------|------|----------|
| Master Agent | 意图识别、任务分解、子Agent调度 | route_task, decompose_query |
| Data Agent | 数据获取、分析、指标计算 | fetch_orders, analyze_sales, calculate_metrics |
| Pricing Agent | 价格分析、竞品对比、定价建议 | fetch_competitor, calculate_price, update_price |
| Inventory Agent | 库存查询、销量预测、补货建议 | check_inventory, forecast_demand |
| Logistics Agent | 物流查询、异常识别、状态更新 | track_shipment, detect_anomaly |
| Report Agent | 数据汇总、图表生成、报告输出 | generate_chart, create_report |
| Knowledge Agent | 知识检索、FAQ匹配、客服回复 | search_knowledge, match_faq |

### 7.2 ReAct范式实现

每个Agent遵循 **Thought → Action → Observation** 循环：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ReAct Prompt模板
REACT_PROMPT = ChatPromptTemplate.from_template("""
你是一个{role}。请遵循以下步骤完成任务：

**任务**: {task}

**可用工具**:
{tools}

**请按以下格式输出**:
Thought: [你的思考过程]
Action: [要执行的工具名称]
Action Input: [工具的输入参数]
Observation: [工具执行后的结果]
... (可重复多次Thought-Action-Observation)
Thought: [基于所有观察，给出最终答案]
Final Answer: [最终答案]

开始!
{history}
""")
```

**ReAct Agent基类：**

```python
"""
====================================
代码任务: 实现ReAct范式Agent基类
最后修改: 2026-03-30 16:00
====================================
"""

from typing import List, Dict, Any, Optional
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

class ReActAgent:
    """ReAct范式Agent基类

    实现Thought-Action-Observation循环，支持多步推理和工具调用
    """

    def __init__(
        self,
        name: str,
        role: str,
        tools: List[BaseTool],
        llm: Optional[ChatOpenAI] = None,
        max_iterations: int = 10
    ):
        """初始化Agent

        Args:
            name: Agent名称
            role: Agent角色描述
            tools: 可用工具列表
            llm: 语言模型实例
            max_iterations: 最大迭代次数
        """
        self.name = name
        self.role = role
        self.tools = {tool.name: tool for tool in tools}
        self.llm = llm or self._get_default_llm()
        self.max_iterations = max_iterations

    async def run(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行Agent的ReAct循环

        Args:
            task: 用户任务描述
            context: 上下文信息（user_id, shop_id等）

        Returns:
            包含最终答案和执行历史的字典
        """
        history = []
        state = {"task": task, "context": context}

        for iteration in range(self.max_iterations):
            # Thought: 推理下一步行动
            thought = await self._think(state, history)
            history.append({"step": "thought", "content": thought})

            # 检查是否完成
            if "Final Answer:" in thought:
                return {
                    "final_answer": thought.split("Final Answer:")[-1].strip(),
                    "history": history,
                    "iterations": iteration + 1
                }

            # Action: 解析行动
            action, action_input = self._parse_action(thought)
            history.append({"step": "action", "content": f"{action}({action_input})"})

            # Observation: 执行工具
            observation = await self._execute_action(action, action_input, context)
            history.append({"step": "observation", "content": str(observation)})

            # 更新状态
            state["last_observation"] = observation

        return {"error": "超过最大迭代次数", "history": history}

    async def _think(
        self,
        state: Dict[str, Any],
        history: List[Dict]
    ) -> str:
        """推理下一步行动"""
        # 构建prompt并调用LLM
        pass

    def _parse_action(self, thought: str) -> tuple[str, str]:
        """从thought中解析action和action_input"""
        # 解析逻辑
        pass

    async def _execute_action(
        self,
        action: str,
        action_input: str,
        context: Dict[str, Any]
    ) -> Any:
        """执行action并返回observation"""
        if action not in self.tools:
            return f"错误: 未知工具 '{action}'"
        tool = self.tools[action]
        return await tool.ainvoke(input=action_input, **context)

    @staticmethod
    def _get_default_llm() -> ChatOpenAI:
        """获取默认LLM配置"""
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
            model="stepfun/step-3.5-flash:free",
            temperature=0.7
        )
```

### 7.3 LangGraph状态机设计（Master Agent）

```python
"""
====================================
代码任务: Master Agent - 意图识别与任务路由
最后修改: 2026-03-30 16:00
====================================
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import operator

class MasterAgentState(TypedDict):
    """Master Agent状态定义"""
    user_id: str
    shop_id: Optional[str]
    query: str
    intent: str
    delegated_agent: Optional[str]
    intermediate_steps: Annotated[list, operator.add]
    final_response: Optional[str]
    error: Optional[str]

class MasterAgent:
    """主控Agent - 负责意图识别和任务路由"""

    def __init__(self, sub_agents: Dict[str, ReActAgent]):
        """初始化

        Args:
            sub_agents: 子Agent字典，键为agent名称
        """
        self.sub_agents = sub_agents
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """构建状态机工作流"""
        workflow = StateGraph(MasterAgentState)

        # 添加节点
        workflow.add_node("classify_intent", self._classify_intent_node)
        workflow.add_node("delegate_to_agent", self._delegate_node)
        workflow.add_node("format_response", self._format_response_node)

        # 设置入口
        workflow.set_entry_point("classify_intent")

        # 添加边
        workflow.add_conditional_edges(
            "classify_intent",
            self._should_delegate,
            {
                "delegate": "delegate_to_agent",
                "respond": "format_response"
            }
        )
        workflow.add_edge("delegate_to_agent", "format_response")
        workflow.add_edge("format_response", END)

        return workflow.compile(checkpointer=MemorySaver())

    async def _classify_intent_node(self, state: MasterAgentState) -> MasterAgentState:
        """意图识别节点"""
        query = state["query"]
        # 使用LLM进行意图分类
        intent = await self._classify_with_llm(query)
        state["intent"] = intent
        return state

    async def _classify_with_llm(self, query: str) -> str:
        """使用LLM分类意图"""
        prompt = f"""
请将以下用户查询分类到合适的意图类别：

查询: {query}

意图类别:
- analyze_business: 销售分析、利润分析、趋势分析
- optimize_pricing: 定价、价格优化、竞品价格
- check_inventory: 库存、补货、安全库存
- track_logistics: 物流、快递、运输
- generate_report: 日报、周报、月报
- customer_service: 客服、咨询、退货
- manage_shop: 店铺、商品、订单管理
- general_chat: 闲聊

仅返回意图类别名称，不要其他内容。
"""
        # 调用LLM
        response = await ReActAgent._get_default_llm().ainvoke(prompt)
        return response.content.strip()

    def _should_delegate(self, state: MasterAgentState) -> str:
        """判断是否需要委托给子Agent"""
        if state["intent"] in ["general_chat", "manage_shop"]:
            return "respond"
        return "delegate"

    async def _delegate_node(self, state: MasterAgentState) -> MasterAgentState:
        """委托给子Agent执行"""
        intent = state["intent"]
        agent_name = self._intent_to_agent(intent)

        if agent_name not in self.sub_agents:
            state["error"] = f"未找到对应的Agent: {agent_name}"
            return state

        agent = self.sub_agents[agent_name]
        result = await agent.run(
            task=state["query"],
            context={
                "user_id": state["user_id"],
                "shop_id": state.get("shop_id")
            }
        )

        state["final_response"] = result.get("final_answer", "执行失败")
        state["intermediate_steps"].append(result.get("history", []))
        return state

    def _intent_to_agent(self, intent: str) -> str:
        """意图映射到Agent"""
        mapping = {
            "analyze_business": "data_agent",
            "optimize_pricing": "pricing_agent",
            "check_inventory": "inventory_agent",
            "track_logistics": "logistics_agent",
            "generate_report": "report_agent",
            "customer_service": "knowledge_agent"
        }
        return mapping.get(intent, "data_agent")

    async def _format_response_node(self, state: MasterAgentState) -> MasterAgentState:
        """格式化最终响应"""
        if not state["final_response"]:
            state["final_response"] = "抱歉，我无法理解您的请求。"
        return state

    async def run(self, query: str, user_id: str, shop_id: Optional[str] = None) -> str:
        """运行Master Agent

        Args:
            query: 用户查询
            user_id: 用户ID
            shop_id: 店铺ID（可选）

        Returns:
            Agent响应
        """
        config = {"configurable": {"thread_id": f"{user_id}_master"}}
        result = await self.graph.ainvoke(
            {
                "user_id": user_id,
                "shop_id": shop_id,
                "query": query,
                "intent": "",
                "delegated_agent": None,
                "intermediate_steps": [],
                "final_response": None,
                "error": None
            },
            config=config
        )
        return result.get("final_response", "")
```

### 7.4 工具（Tool）开发规范

```python
"""
====================================
代码任务: LangChain工具定义示例
最后修改: 2026-03-30 16:00
====================================
"""

from langchain_core.tools import tool
from backend.models.product import Product
from backend.database import async_session

@tool
async def fetch_product_info(sku: str, shop_id: str) -> dict:
    """获取商品信息

    Args:
        sku: 商品SKU编码
        shop_id: 店铺ID

    Returns:
        包含商品信息的字典，包括商品名称、成本价、当前售价、库存等
    """
    async with async_session() as session:
        stmt = select(Product).where(
            Product.sku == sku,
            Product.shop_id == shop_id
        )
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": f"未找到SKU为 {sku} 的商品"}

        return {
            "product_id": product.id,
            "sku": product.sku,
            "name": product.name,
            "cost_price": float(product.cost_price),
            "current_price": float(product.current_price) if product.current_price else None,
            "stock_count": product.stock_count,
            "sales_count": product.sales_count
        }

@tool
async def calculate_optimal_price(
    sku: str,
    shop_id: str,
    min_margin: float = 0.15
) -> dict:
    """计算商品最优定价

    Args:
        sku: 商品SKU编码
        shop_id: 店铺ID
        min_margin: 最低利润率，默认15%

    Returns:
        包含建议价格和定价依据的字典
    """
    # 获取商品信息
    product_info = await fetch_product_info.ainvoke({"sku": sku, "shop_id": shop_id})

    if "error" in product_info:
        return product_info

    cost_price = product_info["cost_price"]

    # 获取竞品价格（模拟）
    competitor_prices = await _fetch_competitor_prices(sku)
    avg_competitor_price = sum(competitor_prices) / len(competitor_prices) if competitor_prices else cost_price * 1.5

    # 计算最优价格
    min_price = cost_price * (1 + min_margin)
    suggested_price = max(min_price, avg_competitor_price * 0.95)
    suggested_price = min(suggested_price, avg_competitor_price * 1.05)

    return {
        "sku": sku,
        "cost_price": cost_price,
        "competitor_avg": avg_competitor_price,
        "suggested_price": round(suggested_price, 2),
        "min_price": round(min_price, 2),
        "reason": f"基于成本价{cost_price}元、竞品均价{avg_competitor_price:.2f}元计算"
    }

async def _fetch_competitor_prices(sku: str) -> list[float]:
    """获取竞品价格（模拟数据）"""
    # 实际实现中可爬取真实数据
    import random
    base_price = random.uniform(100, 500)
    return [base_price * random.uniform(0.8, 1.2) for _ in range(3)]
```

### 7.5 LLM配置规范

```python
"""
====================================
代码任务: LLM配置管理
最后修改: 2026-03-30 16:00
====================================
"""

from langchain_openai import ChatOpenAI
from typing import Literal

# LLM配置
LLM_CONFIG = {
    "openrouter": {
        "provider": "openrouter",
        "model": "stepfun/step-3.5-flash:free",
        "api_key": "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",
        "base_url": "https://openrouter.ai/api/v1",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}

def get_llm(
    provider: Literal["openrouter"] = "openrouter",
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> ChatOpenAI:
    """获取LLM实例

    Args:
        provider: LLM提供商
        temperature: 温度参数
        max_tokens: 最大token数

    Returns:
        ChatOpenAI实例
    """
    config = LLM_CONFIG[provider]
    return ChatOpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        model=config["model"],
        temperature=temperature,
        max_tokens=max_tokens
    )
```

### 7.6 LangGraph 快速参考

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    """Agent状态定义"""
    user_id: str
    intent: str
    input_data: dict
    intermediate_results: Annotated[list, operator.add]
    final_response: str
    error: str | None

# 工作流定义
workflow = StateGraph(AgentState)
workflow.add_node("node_name", node_function)
workflow.add_edge("node_a", "node_b")
workflow.set_entry_point("start_node")
app = workflow.compile()
```

---

## 8. 数据库开发规范

### 8.1 SQLAlchemy 异步模型
```python
from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, Boolean, ForeignKey, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
import enum

class Base(AsyncAttrs, DeclarativeBase):
    """异步ORM基类"""
    pass

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    avatar_url = Column(String(255))
    notification_settings = Column(JSON)  # WebSocket通知偏好
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    shops = relationship("Shop", back_populates="user", cascade="all, delete-orphan")

class ShopType(str, enum.Enum):
    """店铺类型枚举"""
    TAOBAO = "taobao"
    JD = "jd"
    PINDUODUO = "pinduoduo"
    OTHER = "other"

class ShopStatus(str, enum.Enum):
    """店铺状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class Shop(Base):
    """店铺模型"""
    __tablename__ = "shops"

    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    shop_name = Column(String(100), nullable=False)
    shop_type = Column(Enum(ShopType), default=ShopType.TAOBAO)
    shop_url = Column(String(255))
    description = Column(Text)
    logo_url = Column(String(255))
    platform_shop_id = Column(String(100))
    status = Column(Enum(ShopStatus), default=ShopStatus.ACTIVE)
    settings = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="shops")
    products = relationship("Product", back_populates="shop", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="shop", cascade="all, delete-orphan")

class Product(Base):
    """商品模型"""
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False)
    sku = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    brand = Column(String(50))
    cost_price = Column(DECIMAL(10, 2), nullable=False)
    current_price = Column(DECIMAL(10, 2))
    original_price = Column(DECIMAL(10, 2))
    stock_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)
    main_image = Column(String(255))
    images = Column(JSON)
    attributes = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    shop = relationship("Shop", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDING = "refunding"

class Order(Base):
    """订单模型"""
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False)
    platform_order_id = Column(String(100), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    order_no = Column(String(100), nullable=False, unique=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_amount = Column(DECIMAL(10, 2))
    quantity = Column(Integer, default=1)
    buyer_name = Column(String(50))
    buyer_phone = Column(String(20))
    buyer_address = Column(Text)
    remark = Column(Text)
    paid_at = Column(DateTime)
    shipped_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    shop = relationship("Shop", back_populates="orders")
    product = relationship("Product")
    logistics = relationship("Logistics", back_populates="order", uselist=False)

class Logistics(Base):
    """物流模型"""
    __tablename__ = "logistics"

    logistics_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    tracking_number = Column(String(100), nullable=False)
    carrier = Column(String(50), nullable=False)
    carrier_code = Column(String(20))
    current_status = Column(String(50))
    current_location = Column(String(255))
    estimated_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    tracking_details = Column(JSON)
    anomaly_detected = Column(Boolean, default=False)
    anomaly_type = Column(String(50))
    last_sync_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    order = relationship("Order", back_populates="logistics")
```

### 8.2 数据库操作规范
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_product_by_sku(session: AsyncSession, sku: str) -> Product | None:
    """根据SKU获取商品"""
    stmt = select(Product).where(Product.sku == sku)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

# ✅ 使用上下文管理器
async with async_session() as session:
    product = await get_product_by_sku(session, "SKU123")
```

### 8.3 虚拟数据生成（多用户、多店铺）

```python
"""
====================================
代码任务: 生成多用户、多店铺的测试数据
最后修改: 2026-03-30 16:30
====================================
"""

from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict
from backend.models import User, Shop, Product, Order, Logistics
from backend.database import async_session
from sqlalchemy import select
import asyncio

fake = Faker('zh_CN')

# 测试数据配置
TEST_DATA_CONFIG = {
    "users": [
        {"username": "test_user1", "email": "user1@test.com", "password": "password123"},
        {"username": "test_user2", "email": "user2@test.com", "password": "password123"},
        {"username": "test_user3", "email": "user3@test.com", "password": "password123"},
        {"username": "test_admin", "email": "admin@test.com", "password": "admin123"},
        {"username": "demo_user", "email": "demo@test.com", "password": "demo123"},
    ],
    "shops_per_user": [2, 1, 3, 1, 2],  # 每个用户的店铺数量
    "products_per_shop": (20, 50),  # 每个店铺商品数量范围
    "orders_per_shop": (100, 500),  # 每个店铺订单数量范围
}

SHOP_NAME_TEMPLATES = [
    "{category}专营店", "{brand}旗舰店", "优选{category}馆",
    "{category}直销店", "{brand}官方店", "精品{category}"
]

PRODUCT_CATEGORIES = [
    "数码", "家电", "服装", "鞋包", "美妆",
    "家居", "食品", "母婴", "运动", "图书"
]

PRODUCT_BRANDS = [
    "小米", "华为", "苹果", "耐克", "阿迪达斯",
    "海尔", "格力", "美的", "三只松鼠", "良品铺子"
]

CARRIERS = [
    {"name": "顺丰速运", "code": "SF"},
    {"name": "中通快递", "code": "ZTO"},
    {"name": "圆通速递", "code": "YTO"},
    {"name": "韵达速递", "code": "YD"},
    {"name": "申通快递", "code": "STO"},
]

async def generate_all_test_data() -> Dict[str, int]:
    """生成所有测试数据

    Returns:
        生成的数据统计
    """
    stats = {"users": 0, "shops": 0, "products": 0, "orders": 0, "logistics": 0}

    async with async_session() as session:
        # 1. 创建用户
        users = []
        for user_config in TEST_DATA_CONFIG["users"]:
            user = User(
                username=user_config["username"],
                email=user_config["email"],
                password_hash=hash_password(user_config["password"]),
                is_active=True
            )
            session.add(user)
            users.append(user)
        await session.commit()
        stats["users"] = len(users)

        # 2. 为每个用户创建店铺
        all_shops = []
        for i, user in enumerate(users):
            shop_count = TEST_DATA_CONFIG["shops_per_user"][i]
            for j in range(shop_count):
                category = random.choice(PRODUCT_CATEGORIES)
                brand = random.choice(PRODUCT_BRANDS)
                shop_name = fake.random_element(SHOP_NAME_TEMPLATES).format(
                    category=category, brand=brand
                )
                shop = Shop(
                    user_id=user.user_id,
                    shop_name=f"{user.username}_{shop_name}",
                    shop_type=random.choice(list(ShopType)),
                    description=fake.text(max_nb_chars=200),
                    status=ShopStatus.ACTIVE
                )
                session.add(shop)
                all_shops.append(shop)
        await session.commit()
        stats["shops"] = len(all_shops)

        # 3. 为每个店铺创建商品
        all_products = []
        for shop in all_shops:
            product_count = random.randint(*TEST_DATA_CONFIG["products_per_shop"])
            for _ in range(product_count):
                category = random.choice(PRODUCT_CATEGORIES)
                cost_price = random.randint(50, 5000)
                product = Product(
                    shop_id=shop.shop_id,
                    sku=fake.unique.bothify(text='SKU-???-########'),
                    name=f"{category}_{fake.word()}_{fake.random_int(min=100, max=999)}",
                    description=fake.text(max_nb_chars=500),
                    category=category,
                    brand=random.choice(PRODUCT_BRANDS),
                    cost_price=cost_price,
                    current_price=round(cost_price * random.uniform(1.2, 2.0), 2),
                    original_price=round(cost_price * random.uniform(1.5, 2.5), 2),
                    stock_count=random.randint(0, 1000),
                    sales_count=random.randint(0, 500),
                    is_active=True
                )
                session.add(product)
                all_products.append(product)
        await session.commit()
        stats["products"] = len(all_products)

        # 4. 为每个店铺生成订单（过去30天）
        all_orders = []
        for shop in all_shops:
            order_count = random.randint(*TEST_DATA_CONFIG["orders_per_shop"])
            shop_products = [p for p in all_products if p.shop_id == shop.shop_id]

            for _ in range(order_count):
                product = random.choice(shop_products)
                days_ago = random.randint(0, 30)
                created_at = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

                # 根据订单创建时间决定状态
                if days_ago > 7:
                    status = random.choice([OrderStatus.COMPLETED, OrderStatus.CANCELLED])
                elif days_ago > 2:
                    status = OrderStatus.SHIPPED if random.random() > 0.2 else OrderStatus.PAID
                else:
                    status = random.choice([OrderStatus.PAID, OrderStatus.PENDING, OrderStatus.SHIPPED])

                order = Order(
                    shop_id=shop.shop_id,
                    platform_order_id=fake.bothify(text='ORD-##########'),
                    product_id=product.product_id,
                    order_no=fake.unique.bothify(text='ON-############'),
                    status=status,
                    total_amount=product.current_price * random.randint(1, 5),
                    payment_amount=product.current_price * random.randint(1, 5),
                    quantity=random.randint(1, 5),
                    buyer_name=fake.name(),
                    buyer_phone=fake.phone_number(),
                    buyer_address=fake.address(),
                    remark=fake.sentence() if random.random() > 0.7 else None,
                    created_at=created_at,
                    paid_at=created_at + timedelta(hours=random.randint(1, 24)) if status != OrderStatus.PENDING else None,
                    shipped_at=created_at + timedelta(days=random.randint(1, 3)) if status in [OrderStatus.SHIPPED, OrderStatus.COMPLETED] else None,
                    completed_at=created_at + timedelta(days=random.randint(5, 15)) if status == OrderStatus.COMPLETED else None
                )
                session.add(order)
                all_orders.append(order)
        await session.commit()
        stats["orders"] = len(all_orders)

        # 5. 为已发货订单生成物流信息
        for order in all_orders:
            if order.status in [OrderStatus.SHIPPED, OrderStatus.COMPLETED]:
                carrier = random.choice(CARRIERS)
                logistics = Logistics(
                    order_id=order.order_id,
                    tracking_number=f"{carrier['code']}{fake.numerify(text='##########')}",
                    carrier=carrier['name'],
                    carrier_code=carrier['code'],
                    current_status="已签收" if order.status == OrderStatus.COMPLETED else "运输中",
                    tracking_details=generate_tracking_details(
                        carrier['name'],
                        order.shipped_at,
                        order.completed_at
                    ),
                    anomaly_detected=random.random() < 0.05,  # 5%异常率
                    last_sync_at=datetime.now()
                )
                session.add(logistics)
                stats["logistics"] += 1

        await session.commit()

    return stats

def generate_tracking_details(
    carrier: str,
    shipped_at: datetime,
    completed_at: datetime | None
) -> List[Dict]:
    """生成物流轨迹"""
    details = [
        {"time": shipped_at.strftime("%Y-%m-%d %H:%M"), "status": "已揽收"},
        {"time": (shipped_at + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M"), "status": "运输中"},
    ]
    if completed_at:
        details.append({
            "time": completed_at.strftime("%Y-%m-%d %H:%M"),
            "status": "已签收"
        })
    return details

def hash_password(password: str) -> str:
    """简单的密码哈希（生产环境应使用bcrypt）"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

# 执行数据生成
if __name__ == "__main__":
    stats = asyncio.run(generate_all_test_data())
    print(f"测试数据生成完成: {stats}")
```

---

## 9. API 开发规范

---

## 9. API 开发规范

### 9.1 FastAPI 路由设计
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """获取商品列表"""
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit不能超过100"
        )
    # 实现逻辑
    pass

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    """创建新商品"""
    # 实现逻辑
    pass
```

### 9.2 Pydantic 模型定义
```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ProductBase(BaseModel):
    """商品基础模型"""
    sku: str = Field(..., min_length=1, max_length=50, description="商品SKU")
    name: str = Field(..., min_length=1, max_length=200, description="商品名称")
    cost_price: int = Field(..., gt=0, description="成本价（分）")

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """验证SKU格式"""
        if not v.replace('-', '').isalnum():
            raise ValueError('SKU只能包含字母、数字和连字符')
        return v.upper()

class ProductCreate(ProductBase):
    """创建商品请求模型"""
    pass

class ProductResponse(ProductBase):
    """商品响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## 10. 前端开发规范

### 10.1 Vue 3 组件开发
```typescript
<!-- src/components/ProductCard.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Product } from '@/types/product'

interface Props {
  product: Product
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'optimize-price', sku: string): void
}>()

const isLoading = ref(false)
const formattedPrice = computed(() => {
  return (props.product.cost_price / 100).toFixed(2)
})

async function handleOptimizePrice() {
  isLoading.value = true
  try {
    await api.optimizePrice(props.product.sku)
    emit('optimize-price', props.product.sku)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="product-card">
    <!-- 模板内容 -->
  </div>
</template>

<style scoped>
.product-card {
  /* 样式 */
}
</style>
```

### 10.2 TailwindCSS 使用规范
```html
<!-- ✅ 使用设计系统定义的颜色变量 -->
<div class="bg-primary text-primary-foreground">
  <h1 class="text-2xl font-bold">标题</h1>
</div>

<!-- ✅ 响应式设计 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 内容 -->
</div>

<!-- ✅ 交互状态 -->
<button class="px-4 py-2 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 transition-colors">
  点击
</button>
```

---

## 11. 响应指南

### 11.1 沂通风格
- **无废话**：直接进入主题，不要说"好的"、"没问题"等客套话
- 专注技术问题，避免无关的寒暄

### 11.2 增量修改
- 修改大文件时，使用 `# ... existing code ...` 标注，仅显示修改部分
- 清晰标识变更位置和内容

### 11.3 性能预警
如果用户需求可能导致性能问题，**主动指出**：
- N+1 查询问题
- 数据库连接池耗尽
- 内存泄漏风险
- 不必要的重复计算
- WebSocket连接数过多

---

## 12. 工作流程

### 12.1 开发新功能的标准流程
1. **需求分析**：理解用户需求，确认技术方案
2. **设计先行**：设计数据模型、API接口、状态机流程
3. **设计系统**：使用 ui-ux-pro-max 生成前端设计系统
4. **后端开发**：实现数据库模型、API接口、Agent节点
5. **前端开发**：实现页面组件，对接API
6. **数据生成**：创建虚拟测试数据
7. **测试验证**：功能测试，确保可正常运行
8. **文档更新**：更新相关文档

### 12.2 前端开发必遵循流程
1. **生成设计系统**：`python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --design-system -p "CommerceBot"`
2. **补充设计细节**：根据需要查询具体domain（如 `--domain ux "form"`）
3. **获取技术栈指南**：`python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack vue`
4. **实现UI代码**：严格遵循设计系统规范

---

## 13. 项目特定规范（CommerceBot）

### 13.1 目录结构
```
commerceBot/
├── backend/
│   ├── api/                # FastAPI 路由和端点
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── analytics.py
│   │   │   ├── products.py
│   │   │   ├── inventory.py
│   │   │   └── logistics.py
│   ├── core/               # 核心业务逻辑
│   │   ├── agent/          # Agent相关（LangGraph状态机）
│   │   │   ├── graph.py
│   │   │   ├── nodes/      # 各节点实现
│   │   │   └── tools/      # LangChain工具
│   │   ├── services/       # 业务服务层
│   │   └── config.py
│   ├── models/             # SQLAlchemy ORM模型
│   ├── schemas/            # Pydantic请求/响应模型
│   ├── database.py         # 数据库连接配置
│   └── main.py             # FastAPI应用入口
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia状态管理
│   │   ├── api/            # API调用封装
│   │   ├── types/          # TypeScript类型定义
│   │   └── assets/         # 静态资源
│   ├── public/
│   └── package.json
├── data/                   # 测试数据
│   └── seed/
├── tests/                  # 测试用例
│   ├── backend/
│   └── frontend/
├── docs/                   # 项目文档
├── .claude/                # Claude Code技能配置
├── PRD.md                  # 产品需求文档
├── CLAUDE.md               # 本文件
├── pyproject.toml          # Python项目配置
└── README.md
```

### 13.2 核心模块规范
- **Agent系统**：基于LangGraph的状态机编排
- **意图识别**：LLM驱动的意图分类
- **原子能力**：各节点独立实现，便于测试和复用
- **工具层**：LangChain Tool封装，供Agent调用

### 13.3 数据库与端口配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 后端端口 | 8765 | FastAPI服务端口 |
| 前端端口 | 3445 | Vue DevServer端口 |
| MySQL | localhost:3306 | 业务数据存储 |
| Redis | localhost:6379 | 缓存和会话存储 |

### 13.4 数据来源说明
本项目所有数据均由AI生成虚拟测试数据，使用Faker库创建：
- 中文姓名、地址、手机号
- 电商场景数据（商品、订单、物流）
- 覆盖正常和边界情况

### 13.4 测试数据生成
使用 `Faker` 库生成逼真的测试数据：
- 中文姓名、地址、手机号
- 真实的电商场景数据
- 覆盖各种边界情况

---

## 14. Git 提交规范

### 14.1 Commit Message 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 14.2 Type 类型
| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug修复 |
| docs | 文档更新 |
| style | 代码格式（不影响逻辑） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具相关 |

### 14.3 示例
```
feat(agent): 添加库存预警工作流

- 实现inventory_planner节点
- 添加销量预测算法
- 配置定时任务

Closes #123
```

---

**文档版本:** v2.0
**最后更新:** 2026-03-30
**维护者:** CommerceBot Team
