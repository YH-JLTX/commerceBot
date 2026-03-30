/**
 * ====================================
 * 代码任务: API接口层（Mock数据）
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */

import type { Shop, Product, Order, Logistics, DashboardMetrics, PaginatedResponse } from '@/types'

const API_BASE = '/api/v1'

// 模拟延迟
const mockDelay = (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms))

// ==================== Mock数据 ====================

const mockShops: Shop[] = [
  {
    shop_id: 1,
    user_id: 1,
    shop_name: '数码专营店',
    shop_type: 'taobao',
    description: '专注数码电子产品，品质保证',
    logo_url: '/shops/digital.png',
    status: 'active',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  },
  {
    shop_id: 2,
    user_id: 1,
    shop_name: '家居生活馆',
    shop_type: 'jd',
    description: '打造温馨家居生活',
    logo_url: '/shops/home.png',
    status: 'active',
    created_at: '2024-02-01T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  }
]

const mockProducts: Product[] = [
  {
    product_id: 1,
    shop_id: 1,
    sku: 'SKU-001',
    name: '无线蓝牙耳机 5.0',
    description: '高保真音质，长续航，降噪功能',
    category: '数码',
    brand: '小米',
    cost_price: 200,
    current_price: 299,
    original_price: 399,
    stock_count: 150,
    sales_count: 256,
    main_image: '/products/earphone.jpg',
    is_active: true,
    created_at: '2024-01-20T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  },
  {
    product_id: 2,
    shop_id: 1,
    sku: 'SKU-002',
    name: '快充数据线 Type-C',
    description: '支持快充，耐用加粗',
    category: '数码',
    brand: '华为',
    cost_price: 15,
    current_price: 39,
    original_price: 59,
    stock_count: 5,
    sales_count: 89,
    main_image: '/products/cable.jpg',
    is_active: true,
    created_at: '2024-01-20T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  },
  {
    product_id: 3,
    shop_id: 1,
    sku: 'SKU-003',
    name: '手机壳 硅胶防摔',
    description: '多款颜色可选，防摔保护',
    category: '数码',
    brand: '品胜',
    cost_price: 8,
    current_price: 19,
    original_price: 29,
    stock_count: 3,
    sales_count: 45,
    main_image: '/products/case.jpg',
    is_active: true,
    created_at: '2024-01-20T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  },
  {
    product_id: 4,
    shop_id: 2,
    sku: 'SKU-004',
    name: '棉麻舒适沙发套',
    description: '透气舒适，易清洗',
    category: '家居',
    brand: '宜家',
    cost_price: 120,
    current_price: 259,
    original_price: 399,
    stock_count: 45,
    sales_count: 23,
    main_image: '/products/sofa.jpg',
    is_active: true,
    created_at: '2024-02-05T10:00:00Z',
    updated_at: '2024-03-30T10:00:00Z'
  }
]

const mockOrders: Order[] = Array.from({ length: 50 }, (_, i) => {
  const statuses: Order['status'][] = ['pending', 'paid', 'shipped', 'completed', 'cancelled']
  const status = statuses[Math.floor(Math.random() * statuses.length)]
  const daysAgo = Math.floor(Math.random() * 30)

  return {
    order_id: i + 1,
    shop_id: 1,
    platform_order_id: `TB${Date.now()}${i}`,
    product_id: mockProducts[Math.floor(Math.random() * mockProducts.length)].product_id,
    order_no: `ON-202403${String(i + 1).padStart(4, '0')}`,
    status,
    total_amount: Math.floor(Math.random() * 2000) + 50,
    payment_amount: status !== 'pending' ? Math.floor(Math.random() * 2000) + 50 : undefined,
    quantity: Math.floor(Math.random() * 3) + 1,
    buyer_name: `张三${i + 1}`,
    buyer_phone: '138****8888',
    buyer_address: `北京市朝阳区某某街道${i + 1}号`,
    remark: Math.random() > 0.7 ? '请尽快发货' : undefined,
    paid_at: status !== 'pending' ? new Date(Date.now() - daysAgo * 86400000).toISOString() : undefined,
    shipped_at: ['shipped', 'completed'].includes(status) ? new Date(Date.now() - (daysAgo - 2) * 86400000).toISOString() : undefined,
    completed_at: status === 'completed' ? new Date(Date.now() - (daysAgo - 7) * 86400000).toISOString() : undefined,
    created_at: new Date(Date.now() - daysAgo * 86400000).toISOString(),
    updated_at: new Date().toISOString()
  }
})

// ==================== 店铺API ====================

/**
 * 获取店铺列表
 */
export async function getShops(): Promise<Shop[]> {
  await mockDelay()
  return mockShops
}

/**
 * 获取店铺详情
 */
export async function getShopDetail(shopId: number): Promise<Shop | null> {
  await mockDelay()
  return mockShops.find(s => s.shop_id === shopId) || null
}

/**
 * 创建店铺
 */
export async function createShop(data: Partial<Shop>): Promise<Shop> {
  await mockDelay()
  const newShop: Shop = {
    shop_id: mockShops.length + 1,
    user_id: 1,
    shop_name: data.shop_name || '新店铺',
    shop_type: data.shop_type || 'taobao',
    description: data.description,
    logo_url: data.logo_url,
    status: 'active',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
  mockShops.push(newShop)
  return newShop
}

// ==================== 商品API ====================

/**
 * 获取商品列表
 */
export async function getProducts(params: {
  shop_id?: number
  page?: number
  page_size?: number
  category?: string
  keyword?: string
}): Promise<PaginatedResponse<Product>> {
  await mockDelay()

  let filtered = [...mockProducts]
  if (params.shop_id) {
    filtered = filtered.filter(p => p.shop_id === params.shop_id)
  }
  if (params.category) {
    filtered = filtered.filter(p => p.category === params.category)
  }
  if (params.keyword) {
    filtered = filtered.filter(p => p.name.includes(params.keyword!))
  }

  const page = params.page || 1
  const pageSize = params.page_size || 10
  const start = (page - 1) * pageSize
  const items = filtered.slice(start, start + pageSize)

  return {
    items,
    total: filtered.length,
    page,
    page_size: pageSize,
    total_pages: Math.ceil(filtered.length / pageSize)
  }
}

/**
 * 获取商品详情
 */
export async function getProductDetail(productId: number): Promise<Product | null> {
  await mockDelay()
  return mockProducts.find(p => p.product_id === productId) || null
}

/**
 * 创建商品
 */
export async function createProduct(data: Partial<Product>): Promise<Product> {
  await mockDelay()
  const newProduct: Product = {
    product_id: mockProducts.length + 1,
    shop_id: data.shop_id || 1,
    sku: `SKU-${String(mockProducts.length + 1).padStart(3, '0')}`,
    name: data.name || '新商品',
    description: data.description,
    category: data.category,
    brand: data.brand,
    cost_price: data.cost_price || 0,
    current_price: data.current_price,
    original_price: data.original_price,
    stock_count: data.stock_count || 0,
    sales_count: 0,
    main_image: data.main_image,
    is_active: data.is_active !== false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
  mockProducts.push(newProduct)
  return newProduct
}

// ==================== 订单API ====================

/**
 * 获取订单列表
 */
export async function getOrders(params: {
  shop_id?: number
  page?: number
  page_size?: number
  status?: Order['status']
}): Promise<PaginatedResponse<Order>> {
  await mockDelay()

  let filtered = [...mockOrders]
  if (params.shop_id) {
    filtered = filtered.filter(o => o.shop_id === params.shop_id)
  }
  if (params.status) {
    filtered = filtered.filter(o => o.status === params.status)
  }

  const page = params.page || 1
  const pageSize = params.page_size || 20
  const start = (page - 1) * pageSize
  const items = filtered.slice(start, start + pageSize).sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  )

  return {
    items,
    total: filtered.length,
    page,
    page_size: pageSize,
    total_pages: Math.ceil(filtered.length / pageSize)
  }
}

/**
 * 获取订单详情
 */
export async function getOrderDetail(orderId: number): Promise<Order | null> {
  await mockDelay()
  return mockOrders.find(o => o.order_id === orderId) || null
}

/**
 * 更新订单状态
 */
export async function updateOrderStatus(orderId: number, status: Order['status']): Promise<boolean> {
  await mockDelay()
  const order = mockOrders.find(o => o.order_id === orderId)
  if (order) {
    order.status = status
    order.updated_at = new Date().toISOString()
    return true
  }
  return false
}

// ==================== 数据看板API ====================

/**
 * 获取仪表盘数据
 */
export async function getDashboardMetrics(shopId: number): Promise<DashboardMetrics> {
  await mockDelay()

  const shopOrders = mockOrders.filter(o => o.shop_id === shopId)
  const shopProducts = mockProducts.filter(p => p.shop_id === shopId)

  const completedOrders = shopOrders.filter(o => o.status === 'completed')
  const gmv = completedOrders.reduce((sum, o) => sum + (o.payment_amount || 0), 0)

  return {
    gmv,
    order_count: completedOrders.length,
    aov: completedOrders.length > 0 ? gmv / completedOrders.length : 0,
    gmv_growth: 12.3,
    order_growth: 8.5,
    top_products: shopProducts.sort((a, b) => b.sales_count - a.sales_count).slice(0, 5),
    recent_orders: shopOrders.slice(0, 10),
    low_stock_count: shopProducts.filter(p => p.stock_count < 10).length,
    logistics_anomaly_count: 2
  }
}

// ==================== 物流API ====================

/**
 * 获取物流信息
 */
export async function getLogistics(orderId: number): Promise<Logistics | null> {
  await mockDelay()
  return {
    logistics_id: 1,
    order_id: orderId,
    tracking_number: 'SF1234567890',
    carrier: '顺丰速运',
    carrier_code: 'SF',
    current_status: '派送中',
    current_location: '北京市朝阳区营业点',
    estimated_delivery: new Date(Date.now() + 86400000).toISOString(),
    tracking_details: [
      { time: '2024-03-30 09:00', status: '已揽收', location: '深圳市南山营业点' },
      { time: '2024-03-30 15:00', status: '运输中', location: '深圳转运中心' },
      { time: '2024-03-31 08:00', status: '派送中', location: '北京市朝阳区营业点' }
    ],
    anomaly_detected: false,
    last_sync_at: new Date().toISOString()
  }
}

// ==================== 用户认证API ====================

/**
 * 用户登录
 */
export async function login(username: string, password: string): Promise<{ token: string; user: any }> {
  await mockDelay()
  return {
    token: 'mock-jwt-token',
    user: {
      user_id: 1,
      username: 'test_user1',
      email: 'user1@test.com',
      is_active: true
    }
  }
}

/**
 * 用户登出
 */
export async function logout(): Promise<void> {
  await mockDelay()
}
