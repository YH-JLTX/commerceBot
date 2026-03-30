<!--
/**
 * ====================================
 * 代码任务: 库存管理页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 -->
-->

<template>
  <div class="space-y-6">
    <!-- 页面头部 -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-semibold text-text">库存管理</h2>
        <p class="text-text-muted mt-1">监控库存状态，管理补货计划</p>
      </div>
      <div class="flex items-center gap-3">
        <button class="btn-primary flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>补货入库</span>
        </button>
      </div>
    </div>

    <!-- 库存预警卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card border-l-4 border-red-500">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold text-red-700">库存不足</h3>
          <span class="text-2xl">🔴</span>
        </div>
        <p class="text-3xl font-bold text-red-600">{{ lowStockCount }}</p>
        <p class="text-sm text-red-500 mt-1">件商品库存低于安全库存</p>
      </div>
      <div class="card border-l-4 border-yellow-500">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold text-yellow-700">库存预警</h3>
          <span class="text-2xl">🟡</span>
        </div>
        <p class="text-3xl font-bold text-yellow-600">{{ warningStockCount }}</p>
        <p class="text-sm text-yellow-500 mt-1">件商品库存接近安全线</p>
      </div>
      <div class="card border-l-4 border-green-500">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold text-green-700">库存正常</h3>
          <span class="text-2xl">🟢</span>
        </div>
        <p class="text-3xl font-bold text-green-600">{{ normalStockCount }}</p>
        <p class="text-sm text-green-500 mt-1">件商品库存充足</p>
      </div>
    </div>

    <!-- 库存列表 -->
    <div class="card overflow-hidden">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>商品信息</th>
              <th>SKU</th>
              <th>当前库存</th>
              <th>安全库存</th>
              <th>在途库存</th>
              <th>日均销量</th>
              <th>可售天数</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in inventoryProducts" :key="product.product_id">
              <td>
                <p class="font-medium text-text">{{ product.name }}</p>
                <p class="text-sm text-text-muted">{{ product.category }}</p>
              </td>
              <td class="font-mono text-sm">{{ product.sku }}</td>
              <td>
                <span :class="product.stock_count < 10 ? 'text-red-600 font-bold' : 'font-semibold'">
                  {{ product.stock_count }}
                </span>
              </td>
              <td>{{ Math.round(product.cost_price / 10) }}</td>
              <td class="text-text-muted">0</td>
              <td>{{ Math.round(product.sales_count / 30) }}</td>
              <td>
                <span :class="getDaysClass(product.stock_count, Math.round(product.sales_count / 30))">
                  {{ product.sales_count > 0 ? Math.round(product.stock_count / (product.sales_count / 30)) : 0 }} 天
                </span>
              </td>
              <td>
                <span class="px-2 py-1 rounded-full text-xs" :class="getStockStatusClass(product.stock_count)">
                  {{ getStockStatusLabel(product.stock_count) }}
                </span>
              </td>
              <td>
                <button
                  v-if="product.stock_count < 10"
                  @click="createRestockOrder(product)"
                  class="px-3 py-1.5 text-sm bg-cta text-white rounded-lg hover:bg-cta-600 transition-colors duration-200"
                >
                  补货
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getProducts } from '@/api'
import type { Product } from '@/types'

const userStore = useUserStore()

const products = ref<Product[]>([])

const inventoryProducts = computed(() => {
  return products.value.map(p => ({
    ...p,
    safetyStock: Math.round(p.cost_price / 10)
  }))
})

const lowStockCount = computed(() => inventoryProducts.value.filter(p => p.stock_count < 10).length)
const warningStockCount = computed(() => inventoryProducts.value.filter(p => p.stock_count >= 10 && p.stock_count < 30).length)
const normalStockCount = computed(() => inventoryProducts.value.filter(p => p.stock_count >= 30).length)

onMounted(async () => {
  if (userStore.currentShop) {
    const result = await getProducts({ shop_id: userStore.currentShop.shop_id })
    products.value = result.items
  }
})

const getDaysClass = (stock: number, dailySales: number) => {
  if (dailySales === 0) return 'text-text-muted'
  const days = stock / dailySales
  if (days < 7) return 'text-red-600 font-medium'
  if (days < 14) return 'text-yellow-600'
  return 'text-green-600'
}

const getStockStatusClass = (stock: number) => {
  if (stock < 10) return 'bg-red-100 text-red-700'
  if (stock < 30) return 'bg-yellow-100 text-yellow-700'
  return 'bg-green-100 text-green-700'
}

const getStockStatusLabel = (stock: number) => {
  if (stock < 10) return '缺货'
  if (stock < 30) return '预警'
  return '正常'
}

const createRestockOrder = (product: Product) => {
  alert(`创建补货单: ${product.name}\n建议补货量: ${100 - product.stock_count} 件`)
}
</script>
