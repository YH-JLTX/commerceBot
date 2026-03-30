<!--
/**
 * ====================================
 * 代码任务: 数据看板页面
 * 最后修改: 2026-03-30 19:40
 * ====================================
 -->
-->

<template>
  <div class="space-y-6">
    <!-- 顶部指标卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <MetricCard
        title="GMV"
        :value="formatCurrency(metrics.gmv)"
        :growth="metrics.gmv_growth"
        icon="dollar"
      />
      <MetricCard
        title="订单量"
        :value="metrics.order_count"
        :growth="metrics.order_growth"
        icon="shopping"
      />
      <MetricCard
        title="客单价"
        :value="formatCurrency(metrics.aov)"
        icon="chart"
      />
      <MetricCard
        title="待处理预警"
        :value="metrics.low_stock_count + metrics.logistics_anomaly_count"
        type="alert"
        icon="alert"
      />
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 销售趋势图 -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-text">销售趋势</h3>
          <select class="text-sm border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option>最近7天</option>
            <option>最近30天</option>
          </select>
        </div>
        <div ref="salesChartRef" class="h-64"></div>
      </div>

      <!-- 品类分布图 -->
      <div class="card">
        <h3 class="font-semibold text-text mb-4">品类分布</h3>
        <div ref="categoryChartRef" class="h-64"></div>
      </div>
    </div>

    <!-- 热销商品和最近订单 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 热销商品 -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-text">热销商品</h3>
          <router-link :to="{ name: 'Products' }" class="text-sm text-primary hover:text-primary-600">
            查看全部 →
          </router-link>
        </div>
        <div class="space-y-3">
          <div
            v-for="product in metrics.top_products"
            :key="product.product_id"
            class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
          >
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-text truncate">{{ product.name }}</p>
              <p class="text-sm text-text-muted">SKU: {{ product.sku }}</p>
            </div>
            <div class="text-right">
              <p class="font-semibold text-text">¥{{ product.current_price }}</p>
              <p class="text-sm text-text-muted">销量: {{ product.sales_count }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近订单 -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-text">最近订单</h3>
          <router-link :to="{ name: 'Orders' }" class="text-sm text-primary hover:text-primary-600">
            查看全部 →
          </router-link>
        </div>
        <div class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>订单号</th>
                <th>金额</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in metrics.recent_orders.slice(0, 5)" :key="order.order_id">
                <td class="font-mono text-sm">{{ order.order_no }}</td>
                <td>¥{{ order.total_amount }}</td>
                <td>
                  <span
                    class="px-2 py-1 text-xs rounded-full"
                    :class="getStatusClass(order.status)"
                  >
                    {{ getStatusLabel(order.status) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="card">
      <h3 class="font-semibold text-text mb-4">快速操作</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <QuickActionCard
          title="销售分析"
          description="查看详细销售数据"
          icon="chart"
          @click="$router.push({ name: 'Chat' })"
        />
        <QuickActionCard
          title="库存检查"
          :description="`${metrics.low_stock_count}个商品库存不足`"
          icon="inventory"
          @click="$router.push({ name: 'Inventory' })"
        />
        <QuickActionCard
          title="物流异常"
          :description="`${metrics.logistics_anomaly_count}个异常订单`"
          icon="logistics"
          @click="$router.push({ name: 'Logistics' })"
        />
        <QuickActionCard
          title="定价优化"
          description="AI智能定价建议"
          icon="pricing"
          @click="$router.push({ name: 'Chat' })"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getDashboardMetrics } from '@/api'
import type { DashboardMetrics } from '@/types'
import * as echarts from 'echarts'
import MetricCard from '@/components/MetricCard.vue'
import QuickActionCard from '@/components/QuickActionCard.vue'

const router = useRouter()
const userStore = useUserStore()

const metrics = ref<DashboardMetrics>({
  gmv: 0,
  order_count: 0,
  aov: 0,
  gmv_growth: 0,
  order_growth: 0,
  top_products: [],
  recent_orders: [],
  low_stock_count: 0,
  logistics_anomaly_count: 0
})

const salesChartRef = ref<HTMLElement>()
const categoryChartRef = ref<HTMLElement>()

// 加载数据
const loadData = async () => {
  if (userStore.currentShop) {
    metrics.value = await getDashboardMetrics(userStore.currentShop.shop_id)
    await nextTick()
    initCharts()
  }
}

// 初始化图表
const initCharts = () => {
  if (salesChartRef.value) {
    const salesChart = echarts.init(salesChartRef.value)
    salesChart.setOption({
      grid: { top: 10, right: 10, bottom: 20, left: 40 },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: { type: 'value' },
      series: [{
        data: [12000, 15000, 18000, 14000, 20000, 25000, 22000],
        type: 'line',
        smooth: true,
        itemStyle: { color: '#6366F1' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(99, 102, 241, 0.3)' },
            { offset: 1, color: 'rgba(99, 102, 241, 0)' }
          ])
        }
      }]
    })
  }

  if (categoryChartRef.value) {
    const categoryChart = echarts.init(categoryChartRef.value)
    categoryChart.setOption({
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 65, name: '数码', itemStyle: { color: '#6366F1' } },
          { value: 25, name: '家居', itemStyle: { color: '#818CF8' } },
          { value: 10, name: '其他', itemStyle: { color: '#A5B4FC' } }
        ]
      }]
    })
  }
}

// 工具函数
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0
  }).format(value)
}

const getStatusClass = (status: string) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    paid: 'bg-blue-100 text-blue-700',
    shipped: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-gray-100 text-gray-700'
  }
  return classes[status as keyof typeof classes] || ''
}

const getStatusLabel = (status: string) => {
  const labels = {
    pending: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status as keyof typeof labels] || status
}

onMounted(() => {
  loadData()
})
</script>
