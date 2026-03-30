<!--
/**
 * ====================================
 * 代码任务: 物流管理页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 -->
-->

<template>
  <div class="space-y-6">
    <!-- 页面头部 -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-semibold text-text">物流管理</h2>
        <p class="text-text-muted mt-1">跟踪物流状态，处理异常订单</p>
      </div>
      <div class="flex items-center gap-3">
        <div class="relative">
          <input
            v-model="trackingNumber"
            type="text"
            placeholder="输入物流单号查询"
            class="input-field pl-10"
            @keyup.enter="searchTracking"
          />
          <svg class="w-5 h-5 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <button @click="searchTracking" class="btn-primary">
          查询
        </button>
      </div>
    </div>

    <!-- 物流异常卡片 -->
    <div v-if="anomalyOrders.length > 0" class="card border-l-4 border-red-500">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-3">
          <span class="text-2xl">⚠️</span>
          <div>
            <h3 class="font-semibold text-red-700">物流异常提醒</h3>
            <p class="text-sm text-red-600">发现 {{ anomalyOrders.length }} 个异常订单需要处理</p>
          </div>
        </div>
        <button class="text-sm text-red-600 hover:text-red-700">查看全部 →</button>
      </div>
      <div class="space-y-2">
        <div
          v-for="order in anomalyOrders.slice(0, 3)"
          :key="order.order_id"
          class="flex items-center justify-between p-3 bg-red-50 rounded-lg"
        >
          <div class="flex-1">
            <p class="text-sm font-medium text-text">{{ order.order_no }}</p>
            <p class="text-xs text-text-muted">{{ order.buyer_name }} - {{ order.buyer_phone }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm font-medium text-red-600">{{ order.anomalyType }}</p>
            <p class="text-xs text-text-muted">{{ order.anomalyTime }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 物流列表 -->
    <div class="card overflow-hidden">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>物流单号</th>
              <th>快递公司</th>
              <th>当前状态</th>
              <th>当前位置</th>
              <th>预计送达</th>
              <th>异常</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in logisticsList" :key="item.order_id">
              <td class="font-mono text-sm">{{ item.order_no }}</td>
              <td class="font-mono text-sm">{{ item.tracking_number }}</td>
              <td>
                <span class="flex items-center gap-2">
                  <span class="w-6 h-6 bg-primary-100 rounded flex items-center justify-center text-xs text-primary font-medium">
                    {{ item.carrier_code }}
                  </span>
                  {{ item.carrier }}
                </span>
              </td>
              <td>
                <span class="px-2 py-1 rounded-full text-xs" :class="getStatusClass(item.current_status)">
                  {{ item.current_status }}
                </span>
              </td>
              <td class="text-sm text-text-muted">{{ item.current_location }}</td>
              <td class="text-sm">
                {{ item.estimated_delivery ? formatDate(item.estimated_delivery) : '-' }}
              </td>
              <td>
                <span v-if="item.anomaly_detected" class="text-red-600">⚠️ {{ item.anomaly_type }}</span>
                <span v-else class="text-green-600">✓ 正常</span>
              </td>
              <td>
                <button
                  @click="viewTrackingDetail(item)"
                  class="p-1.5 text-primary hover:bg-primary-50 rounded-lg transition-colors duration-200"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 物流详情对话框 -->
    <div v-if="showTrackingDetail" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg mx-4">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-text">物流详情</h3>
            <button @click="showTrackingDetail = false" class="p-1 hover:bg-gray-100 rounded-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="p-6">
          <div v-if="selectedLogistics" class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p class="text-sm text-text-muted">物流单号</p>
                <p class="font-mono font-semibold text-text">{{ selectedLogistics.tracking_number }}</p>
              </div>
              <button class="text-sm text-primary hover:underline">复制</button>
            </div>

            <!-- 物流轨迹 -->
            <div class="space-y-3">
              <p class="text-sm font-medium text-text">物流轨迹</p>
              <div class="relative">
                <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
                <div class="space-y-4">
                  <div
                    v-for="(detail, index) in selectedLogistics.tracking_details"
                    :key="index"
                    class="relative flex gap-4"
                  >
                    <div class="w-8 h-8 rounded-full flex items-center justify-center z-10"
                      :class="index === 0 ? 'bg-primary text-white' : 'bg-gray-200 text-text-muted'"
                    >
                      <svg v-if="index === 0" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span v-else class="text-xs">{{ index + 1 }}</span>
                    </div>
                    <div class="flex-1 pb-4">
                      <p class="text-sm font-medium text-text">{{ detail.status }}</p>
                      <p class="text-xs text-text-muted">{{ detail.time }}</p>
                      <p v-if="detail.location" class="text-xs text-text-muted mt-1">{{ detail.location }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getOrders, getLogistics } from '@/api'
import type { Order, Logistics } from '@/types'

const userStore = useUserStore()

const trackingNumber = ref('')
const showTrackingDetail = ref(false)
const selectedLogistics = ref<Logistics | null>(null)

// 模拟物流列表数据
const logisticsList = ref<any[]>([])
const anomalyOrders = ref<any[]>([
  { order_id: 1, order_no: 'ON-20240325001', buyer_name: '张三', buyer_phone: '138****8888', anomalyType: '派送失败', anomalyTime: '2小时前' },
  { order_id: 2, order_no: 'ON-20240324005', buyer_name: '李四', buyer_phone: '139****9999', anomalyType: '物流停滞', anomalyTime: '48小时前' }
])

onMounted(async () => {
  if (userStore.currentShop) {
    const result = await getOrders({ shop_id: userStore.currentShop.shop_id })
    const shippedOrders = result.items.filter(o => ['shipped', 'completed'].includes(o.status))

    logisticsList.value = shippedOrders.slice(0, 10).map(order => ({
      order_id: order.order_id,
      order_no: order.order_no,
      tracking_number: `SF${Date.now()}${order.order_id}`.slice(0, 12),
      carrier: '顺丰速运',
      carrier_code: 'SF',
      current_status: order.status === 'completed' ? '已签收' : '运输中',
      current_location: order.status === 'completed' ? '北京市' : '深圳市',
      estimated_delivery: new Date(Date.now() + 86400000).toISOString(),
      anomaly_detected: Math.random() > 0.8,
      anomaly_type: '派送失败'
    }))
  }
})

const searchTracking = async () => {
  if (!trackingNumber.value.trim()) return
  alert(`查询物流单号: ${trackingNumber.value}`)
}

const viewTrackingDetail = async (item: any) => {
  selectedLogistics.value = await getLogistics(item.order_id)
  showTrackingDetail.value = true
}

const getStatusClass = (status: string) => {
  const classes = {
    '已揽收': 'bg-blue-100 text-blue-700',
    '运输中': 'bg-purple-100 text-purple-700',
    '派送中': 'bg-yellow-100 text-yellow-700',
    '已签收': 'bg-green-100 text-green-700',
    '派送失败': 'bg-red-100 text-red-700'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-700'
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}
</script>
