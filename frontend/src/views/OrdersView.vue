<!--
/**
 * ====================================
 * 代码任务: 订单管理页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 -->
-->

<template>
  <div class="space-y-6">
    <!-- 页面头部 -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-semibold text-text">订单管理</h2>
        <p class="text-text-muted mt-1">查看和管理店铺订单</p>
      </div>
      <div class="flex items-center gap-3">
        <select v-model="filterStatus" class="input-field" @change="handleFilter">
          <option value="">全部状态</option>
          <option value="pending">待付款</option>
          <option value="paid">已付款</option>
          <option value="shipped">已发货</option>
          <option value="completed">已完成</option>
          <option value="cancelled">已取消</option>
        </select>
      </div>
    </div>

    <!-- 订单表格 -->
    <div class="card overflow-hidden">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>商品信息</th>
              <th>买家信息</th>
              <th>金额</th>
              <th>数量</th>
              <th>状态</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in paginatedOrders.items" :key="order.order_id">
              <td class="font-mono text-sm">{{ order.order_no }}</td>
              <td>
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 bg-gray-100 rounded flex items-center justify-center">
                    <svg class="w-5 h-5 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  <span class="text-sm text-text-muted">商品ID: {{ order.product_id }}</span>
                </div>
              </td>
              <td>
                <p class="text-sm">{{ order.buyer_name }}</p>
                <p class="text-xs text-text-muted">{{ order.buyer_phone }}</p>
              </td>
              <td class="font-semibold">¥{{ order.total_amount }}</td>
              <td>{{ order.quantity }}</td>
              <td>
                <span class="px-2 py-1 rounded-full text-xs" :class="getStatusClass(order.status)">
                  {{ getStatusLabel(order.status) }}
                </span>
              </td>
              <td class="text-sm text-text-muted">{{ formatDate(order.created_at) }}</td>
              <td>
                <div class="flex items-center gap-2">
                  <button
                    @click="viewOrderDetail(order)"
                    class="p-1.5 text-primary hover:bg-primary-50 rounded-lg transition-colors duration-200"
                    title="查看详情"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="paginatedOrders.total_pages > 1" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
        <p class="text-sm text-text-muted">
          共 {{ paginatedOrders.total }} 条记录
        </p>
        <div class="flex items-center gap-2">
          <button
            v-for="page in Math.min(5, paginatedOrders.total_pages)"
            :key="page"
            @click="currentPage = page"
            class="w-8 h-8 rounded-lg transition-colors duration-200"
            :class="page === currentPage ? 'bg-primary text-white' : 'border border-gray-300 hover:bg-gray-50'"
          >
            {{ page }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getOrders } from '@/api'
import type { Order } from '@/types'

const userStore = useUserStore()

const orders = ref<Order[]>([])
const filterStatus = ref<Order['status'] | ''>('')
const currentPage = ref(1)

const paginatedOrders = computed(() => {
  let filtered = [...orders.value]

  if (filterStatus.value) {
    filtered = filtered.filter(o => o.status === filterStatus.value)
  }

  const pageSize = 20
  const start = (currentPage.value - 1) * pageSize
  const items = filtered.slice(start, start + pageSize)

  return {
    items,
    total: filtered.length,
    page: currentPage.value,
    page_size: pageSize,
    total_pages: Math.ceil(filtered.length / pageSize)
  }
})

onMounted(async () => {
  if (userStore.currentShop) {
    const result = await getOrders({ shop_id: userStore.currentShop.shop_id })
    orders.value = result.items
  }
})

const handleFilter = () => {
  currentPage.value = 1
}

const getStatusClass = (status: Order['status']) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    paid: 'bg-blue-100 text-blue-700',
    shipped: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-gray-100 text-gray-700'
  }
  return classes[status] || ''
}

const getStatusLabel = (status: Order['status']) => {
  const labels = {
    pending: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || status
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const viewOrderDetail = (order: Order) => {
  console.log('查看订单详情:', order)
}
</script>
