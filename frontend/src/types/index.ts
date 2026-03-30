/**
 * ====================================
 * 代码任务: TypeScript类型定义
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */

// 用户相关类型
export interface User {
  user_id: number
  username: string
  email: string
  phone?: string
  avatar_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// 店铺相关类型
export interface Shop {
  shop_id: number
  user_id: number
  shop_name: string
  shop_type: 'taobao' | 'jd' | 'pinduoduo' | 'other'
  shop_url?: string
  description?: string
  logo_url?: string
  status: 'active' | 'inactive' | 'suspended'
  created_at: string
  updated_at: string
}

// 商品相关类型
export interface Product {
  product_id: number
  shop_id: number
  sku: string
  name: string
  description?: string
  category?: string
  brand?: string
  cost_price: number
  current_price?: number
  original_price?: number
  stock_count: number
  sales_count: number
  main_image?: string
  images?: string[]
  attributes?: Record<string, any>
  is_active: boolean
  created_at: string
  updated_at: string
}

// 订单相关类型
export interface Order {
  order_id: number
  shop_id: number
  platform_order_id: string
  product_id?: number
  order_no: string
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled' | 'refunding'
  total_amount: number
  payment_amount?: number
  quantity: number
  buyer_name?: string
  buyer_phone?: string
  buyer_address?: string
  remark?: string
  paid_at?: string
  shipped_at?: string
  completed_at?: string
  created_at: string
  updated_at: string
}

// 物流相关类型
export interface Logistics {
  logistics_id: number
  order_id: number
  tracking_number: string
  carrier: string
  carrier_code?: string
  current_status?: string
  current_location?: string
  estimated_delivery?: string
  actual_delivery?: string
  tracking_details?: TrackingDetail[]
  anomaly_detected: boolean
  anomaly_type?: string
  last_sync_at?: string
}

export interface TrackingDetail {
  time: string
  status: string
  location?: string
}

// Agent对话相关类型
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  thought_process?: ThoughtStep[]
  agent_used?: string
}

export interface ThoughtStep {
  step: 'thought' | 'action' | 'observation'
  content: string
}

export interface ChatRequest {
  query: string
  shop_id?: string
  session_id?: string
}

export interface ChatResponse {
  response: string
  thought_process?: ThoughtStep[]
  agent_used?: string
  session_id?: string
}

// 数据看板相关类型
export interface DashboardMetrics {
  gmv: number
  order_count: number
  aov: number
  gmv_growth: number
  order_growth: number
  top_products: Product[]
  recent_orders: Order[]
  low_stock_count: number
  logistics_anomaly_count: number
}

// API响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
}

export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
