"""
====================================
代码任务: AI聊天API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from backend.database import get_async_session
from backend.models.user import User
from backend.models.shop import Shop
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.api.v1.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["AI聊天"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """AI对话接口"""
    # 验证店铺权限
    if request.shop_id:
        shop_stmt = select(Shop).where(
            Shop.shop_id == request.shop_id,
            Shop.user_id == current_user.user_id
        )
        shop_result = await session.execute(shop_stmt)
        if shop_result.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="店铺不存在或无权访问")

    # 生成会话ID
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # TODO: 接入真实的Agent系统
    # 目前返回模拟响应
    response = _generate_mock_response(request.message)

    return ChatResponse(
        response=response,
        conversation_id=conversation_id,
        intermediate_steps=[]
    )


def _generate_mock_response(message: str) -> str:
    """生成模拟响应（后续会被真实Agent替换）"""
    message_lower = message.lower()

    if "销售" in message or "gmv" in message_lower:
        return """根据您的店铺数据分析：

📊 **销售概览**（近30天）
- GMV：¥128,500
- 订单量：485单
- 客单价：¥265
- 环比增长：+12.5%

📈 **趋势分析**
- 本周销售表现良好，尤其是数码类商品
- 建议关注库存紧张的热销商品

需要更详细的销售分析吗？"""

    elif "库存" in message:
        return """📦 **库存预警**

当前有3个商品库存不足：
1. 小米手环7 (SKU: SKU-MI-001) - 库存: 5件
2. 华为耳机 (SKU: SKU-HW-002) - 库存: 8件
3. 苹果数据线 (SKU: SKU-AP-003) - 库存: 3件

💡 **补货建议**
建议优先补充小米手环7，该商品周销量约20件

需要我帮您生成采购单吗？"""

    elif "物流" in message:
        return """🚚 **物流异常提醒**

当前有2个订单存在物流异常：
1. 订单 ON-12345678 - 运输超时
2. 订单 ON-87654321 - 签收异常

📍 **处理建议**
- 建议联系快递公司核实情况
- 主动联系买家说明情况

需要我帮您批量处理吗？"""

    elif "定价" in message or "价格" in message:
        return """💰 **智能定价建议**

分析竞品数据后，以下商品建议调价：

1. **小米充电宝** (当前: ¥99)
   - 竞品均价: ¥89-95
   - 建议调整: ¥92（提升竞争力）

2. **华为手机壳** (当前: ¥49)
   - 竞品均价: ¥55-60
   - 建议调整: ¥58（提升利润率）

是否执行价格调整？"""

    else:
        return """您好！我是您的电商运营助手，可以帮您：

📊 **数据分析**
- 销售分析、GMV统计
- 订单趋势、客单价分析

📦 **库存管理**
- 库存预警、补货建议
- 销量预测

🚚 **物流跟踪**
- 物流异常提醒
- 批量查询物流

💰 **智能定价**
- 竞品价格分析
- 定价建议

请告诉我您需要什么帮助？"""
