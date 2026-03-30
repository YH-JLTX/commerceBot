/**
 * ====================================
 * 代码任务: Agent对话API接口
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */

import type { ChatRequest, ChatResponse, ChatMessage } from '@/types'

const API_BASE = '/api/v1'

// 模拟AI响应延迟
const MOCK_DELAY = 1000

// Mock对话历史
let mockMessages: ChatMessage[] = []

/**
 * 发送聊天消息
 */
export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, MOCK_DELAY))

  const userMessage: ChatMessage = {
    role: 'user',
    content: request.query,
    timestamp: new Date().toISOString()
  }
  mockMessages.push(userMessage)

  // 模拟Agent响应
  const response = mockAgentResponse(request.query)

  const assistantMessage: ChatMessage = {
    role: 'assistant',
    content: response.response,
    timestamp: new Date().toISOString(),
    thought_process: response.thought_process,
    agent_used: response.agent_used
  }
  mockMessages.push(assistantMessage)

  return response
}

/**
 * 获取对话历史
 */
export async function getChatHistory(sessionId?: string): Promise<ChatMessage[]> {
  await new Promise(resolve => setTimeout(resolve, 300))
  return mockMessages
}

/**
 * 清除对话历史
 */
export async function clearChatHistory(): Promise<void> {
  mockMessages = []
}

/**
 * 模拟Agent响应
 */
function mockAgentResponse(query: string): ChatResponse {
  const lowerQuery = query.toLowerCase()

  // 销售分析
  if (lowerQuery.includes('销售') || lowerQuery.includes('分析') || lowerQuery.includes('数据')) {
    return {
      response: `根据您店铺的数据分析，过去7天的销售情况如下：

**核心指标：**
- GMV：¥158,000（环比增长12.3%）
- 订单量：156单（环比增长8.5%）
- 客单价：¥1,012.82
- 利润率：28.5%

**趋势分析：**
- 销售额呈上升趋势，主要集中在周末
- 热销品类：数码产品（65%）、家居（25%）
- 需要注意：库存周转天数偏高，建议优化库存结构`,
      thought_process: [
        { step: 'thought', content: '用户想了解销售情况，需要获取订单数据' },
        { step: 'action', content: 'fetch_orders: {"date_range": "last_7_days"}' },
        { step: 'observation', content: '获取到156条订单记录' },
        { step: 'thought', content: '计算GMV和增长率' },
        { step: 'action', content: 'calculate_gmv: {"orders": [...]}' },
        { step: 'observation', content: 'GMV = 158,000元，环比增长12.3%' }
      ],
      agent_used: 'Data Agent'
    }
  }

  // 定价相关
  if (lowerQuery.includes('价格') || lowerQuery.includes('定价') || lowerQuery.includes('优化')) {
    return {
      response: `我为您分析了"无线蓝牙耳机"的定价策略：

**当前定价：** ¥299
**成本价：** ¥200
**竞品均价：** ¥285

**定价建议：**
- 建议售价：¥285
- 预期利润率：30%
- 竞争优势：价格适中，性价比突出

**分析依据：**
- 竞品价格区间：¥279 - ¥329
- 建议略低于竞品均价以获取更多流量
- 当前定价偏高，可能影响转化率

是否需要我帮您更新价格？`,
      thought_process: [
        { step: 'thought', content: '用户询问定价优化，需要获取商品信息和竞品价格' },
        { step: 'action', content: 'get_product_info: {"sku": "SKU-123"}' },
        { step: 'observation', content: '商品：无线蓝牙耳机，成本200元，当前售价299元' },
        { step: 'action', content: 'get_competitor_prices: {"category": "数码"}' },
        { step: 'observation', content: '竞品价格：[279, 285, 299, 315, 329]，均价285元' },
        { step: 'thought', content: '基于成本和竞品分析，计算最优价格' }
      ],
      agent_used: 'Pricing Agent'
    }
  }

  // 库存相关
  if (lowerQuery.includes('库存') || lowerQuery.includes('补货')) {
    return {
      response: `检测到以下商品库存预警：

🔴 **紧急补货（库存<安全库存的30%）：**
- 手机壳（SKU-001）：当前5件，安全库存50件
- 数据线（SKU-002）：当前8件，安全库存40件

🟡 **建议补货（库存<安全库存的60%）：**
- 充电头（SKU-003）：当前25件，安全库存50件

**自动操作：**
- 已为紧急商品生成补货单，建议补货量：手机壳100件、数据线80件
- 补货单已发送至您的待处理列表

是否需要我查看更多库存详情？`,
      thought_process: [
        { step: 'thought', content: '用户询问库存，需要检查当前库存状态' },
        { step: 'action', content: 'check_inventory: {"shop_id": "1"}' },
        { step: 'observation', content: '发现2个商品库存严重低于安全库存' },
        { step: 'thought', content: '需要预测未来销量以确定补货量' },
        { step: 'action', content: 'forecast_demand: {"product_id": "1"}' },
        { step: 'observation', content: '未来7天预测销量80件' },
        { step: 'action', content: 'create_restock_order: {"product_id": "1", "quantity": 100}' }
      ],
      agent_used: 'Inventory Agent'
    }
  }

  // 物流相关
  if (lowerQuery.includes('物流') || lowerQuery.includes('快递')) {
    return {
      response: `物流异常提醒：

⚠️ **需要关注的异常订单：**
1. 订单号 ON-20240325001
   - 物流单号：SF1234567890
   - 异常类型：派送失败
   - 原因：收件人电话无法接通
   - 建议：联系收件人确认

2. 订单号 ON-20240324005
   - 物流单号：ZTO9876543210
   - 异常类型：物流停滞
   - 停滞时间：48小时
   - 建议：联系快递公司查询

**整体物流状况：**
- 在途订单：23单
- 异常订单：2单（异常率8.7%）
- 已签收：156单

是否需要我帮您处理这些异常？`,
      thought_process: [
        { step: 'thought', content: '用户询问物流，需要检查异常订单' },
        { step: 'action', content: 'get_anomaly_orders: {"shop_id": "1"}' },
        { step: 'observation', content: '发现2个异常订单' }
      ],
      agent_used: 'Logistics Agent'
    }
  }

  // 默认响应
  return {
    response: `您好！我是您的电商智能运营助手。我可以帮您：

📊 **数据分析**
- 销售分析、利润分析、趋势分析

💰 **智能定价**
- 价格优化建议、竞品对比分析

📦 **库存管理**
- 库存预警、销量预测、补货建议

🚚 **物流跟踪**
- 物流查询、异常识别、状态更新

📋 **报表生成**
- 日报、周报、月报自动生成

💬 **智能客服**
- 知识库问答、常见咨询

请告诉我您需要什么帮助？`,
    agent_used: 'Master Agent'
  }
}

/**
 * WebSocket连接类
 */
export class AgentWebSocket {
  private ws: WebSocket | null = null
  private reconnectTimer: number | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5

  constructor(private userId: string) {}

  connect() {
    const wsUrl = `ws://localhost:8765/ws?user_id=${this.userId}`
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket连接已建立')
      this.reconnectAttempts = 0
      this.onConnected?.()
    }

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.handleMessage(data)
    }

    this.ws.onclose = () => {
      console.log('WebSocket连接已关闭')
      this.onDisconnected?.()
      this.scheduleReconnect()
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket错误:', error)
      this.onError?.(error)
    }
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
      this.reconnectTimer = window.setTimeout(() => {
        console.log(`尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
        this.connect()
      }, delay)
    }
  }

  private handleMessage(data: any) {
    switch (data.type) {
      case 'agent:thinking':
        this.onThinking?.(data.content)
        break
      case 'agent:message':
        this.onMessage?.(data.content)
        break
      case 'alert:inventory':
        this.onAlert?.(data)
        break
      case 'alert:logistics':
        this.onAlert?.(data)
        break
    }
  }

  // 事件回调
  onConnected?: () => void
  onDisconnected?: () => void
  onError?: (error: Event) => void
  onThinking?: (content: string) => void
  onMessage?: (content: string) => void
  onAlert?: (alert: any) => void
}
