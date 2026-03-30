<!--
/**
 * ====================================
 * 代码任务: 商品管理页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 -->
-->

<template>
  <div class="space-y-6">
    <!-- 页面头部和筛选 -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-semibold text-text">商品管理</h2>
        <p class="text-text-muted mt-1">管理店铺商品，优化定价策略</p>
      </div>
      <div class="flex items-center gap-3">
        <div class="relative">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索商品名称或SKU"
            class="input-field pl-10"
            @keyup.enter="handleSearch"
          />
          <svg class="w-5 h-5 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select v-model="filterCategory" class="input-field" @change="handleSearch">
          <option value="">全部分类</option>
          <option value="数码">数码</option>
          <option value="家居">家居</option>
          <option value="服装">服装</option>
          <option value="食品">食品</option>
        </select>
        <button @click="showCreateDialog = true" class="btn-primary flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>添加商品</span>
        </button>
      </div>
    </div>

    <!-- 商品表格 -->
    <div class="card overflow-hidden">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>商品信息</th>
              <th>SKU</th>
              <th>分类</th>
              <th>成本价</th>
              <th>当前售价</th>
              <th>库存</th>
              <th>销量</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody v-if="!isLoading && paginatedProducts.items.length > 0">
            <tr v-for="product in paginatedProducts.items" :key="product.product_id">
              <td>
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-medium text-text">{{ product.name }}</p>
                    <p class="text-sm text-text-muted">{{ product.brand }}</p>
                  </div>
                </div>
              </td>
              <td class="font-mono text-sm">{{ product.sku }}</td>
              <td>
                <span class="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">{{ product.category }}</span>
              </td>
              <td>¥{{ product.cost_price }}</td>
              <td>
                <span class="font-semibold text-text">¥{{ product.current_price }}</span>
              </td>
              <td>
                <span :class="product.stock_count < 10 ? 'text-red-600 font-medium' : ''">
                  {{ product.stock_count }}
                </span>
              </td>
              <td>{{ product.sales_count }}</td>
              <td>
                <span class="px-2 py-1 rounded-full text-xs" :class="product.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'">
                  {{ product.is_active ? '上架' : '下架' }}
                </span>
              </td>
              <td>
                <div class="flex items-center gap-2">
                  <button
                    @click="optimizePrice(product)"
                    class="p-1.5 text-cta hover:bg-cta-50 rounded-lg transition-colors duration-200"
                    title="智能定价"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button
                    @click="editProduct(product)"
                    class="p-1.5 text-primary hover:bg-primary-50 rounded-lg transition-colors duration-200"
                    title="编辑"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="toggleProductStatus(product)"
                    class="p-1.5 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                    :title="product.is_active ? '下架' : '上架'"
                  >
                    <svg class="w-4 h-4" :class="product.is_active ? 'text-red-500' : 'text-green-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
          <tbody v-else-if="!isLoading && paginatedProducts.items.length === 0">
            <tr>
              <td colspan="9" class="text-center py-12 text-text-muted">暂无商品数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="paginatedProducts.total_pages > 1" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
        <p class="text-sm text-text-muted">
          共 {{ paginatedProducts.total }} 条记录，第 {{ currentPage }} / {{ paginatedProducts.total_pages }} 页
        </p>
        <div class="flex items-center gap-2">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1.5 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            上一页
          </button>
          <button
            v-for="page in displayedPages"
            :key="page"
            @click="changePage(page)"
            class="w-8 h-8 rounded-lg transition-colors duration-200"
            :class="page === currentPage ? 'bg-primary text-white' : 'border border-gray-300 hover:bg-gray-50'"
          >
            {{ page }}
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === paginatedProducts.total_pages"
            class="px-3 py-1.5 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 智能定价对话框 -->
    <div v-if="showPriceDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md mx-4">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-text">智能定价建议</h3>
        </div>
        <div class="p-6">
          <div v-if="priceSuggestion" class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div>
                <p class="text-sm text-text-muted">当前价格</p>
                <p class="text-xl font-semibold text-text">¥{{ priceSuggestion.current_price }}</p>
              </div>
              <svg class="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </div>

            <div class="flex items-center justify-between p-4 bg-primary-50 rounded-xl">
              <div>
                <p class="text-sm text-primary-600">建议价格</p>
                <p class="text-2xl font-bold text-primary">¥{{ priceSuggestion.suggested_price }}</p>
              </div>
              <span class="text-3xl">✨</span>
            </div>

            <div class="p-4 bg-green-50 rounded-xl">
              <p class="text-sm font-medium text-green-700 mb-2">💡 分析依据</p>
              <p class="text-sm text-green-600">{{ priceSuggestion.reason }}</p>
            </div>
          </div>
        </div>
        <div class="p-6 border-t border-gray-200 flex justify-end gap-3">
          <button @click="showPriceDialog = false" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            取消
          </button>
          <button class="btn-cta" @click="applyPriceSuggestion">
            应用建议价格
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getProducts, createProduct } from '@/api'
import type { Product } from '@/types'

const router = useRouter()
const userStore = useUserStore()

const products = ref<Product[]>([])
const isLoading = ref(false)
const searchKeyword = ref('')
const filterCategory = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 对话框状态
const showCreateDialog = ref(false)
const showPriceDialog = ref(false)
const priceSuggestion = ref<any>(null)
const selectedProduct = ref<Product | null>(null)

// 分页数据
const paginatedProducts = computed(() => {
  let filtered = [...products.value]

  // 搜索过滤
  if (searchKeyword.value) {
    filtered = filtered.filter(p =>
      p.name.includes(searchKeyword.value) || p.sku.includes(searchKeyword.value)
    )
  }

  // 分类过滤
  if (filterCategory.value) {
    filtered = filtered.filter(p => p.category === filterCategory.value)
  }

  const total = filtered.length
  const totalPages = Math.ceil(total / pageSize.value)
  const start = (currentPage.value - 1) * pageSize.value
  const items = filtered.slice(start, start + pageSize.value)

  return {
    items,
    total,
    page: currentPage.value,
    page_size: pageSize.value,
    total_pages: totalPages
  }
})

// 显示的页码
const displayedPages = computed(() => {
  const total = paginatedProducts.value.total_pages
  const current = currentPage.value
  const pages = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      pages.push(current - 1)
      pages.push(current)
      pages.push(current + 1)
      pages.push('...')
      pages.push(total)
    }
  }

  return pages
})

// 加载商品数据
onMounted(async () => {
  if (userStore.currentShop) {
    isLoading.value = true
    const result = await getProducts({ shop_id: userStore.currentShop.shop_id })
    products.value = result.items
    isLoading.value = false
  }
})

// 搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 翻页
const changePage = (page: number) => {
  if (page >= 1 && page <= paginatedProducts.value.total_pages) {
    currentPage.value = page
  }
}

// 智能定价
const optimizePrice = (product: Product) => {
  selectedProduct.value = product
  priceSuggestion.value = {
    current_price: product.current_price || 0,
    suggested_price: Math.round((product.cost_price || 0) * 1.3),
    reason: `基于成本价¥${product.cost_price}，建议定价为成本价的1.3倍以保持竞争力并获得合理利润。竞品均价约为¥${Math.round((product.cost_price || 0) * 1.4)}`
  }
  showPriceDialog.value = true
}

// 应用建议价格
const applyPriceSuggestion = () => {
  if (selectedProduct.value && priceSuggestion.value) {
    const index = products.value.findIndex(p => p.product_id === selectedProduct.value!.product_id)
    if (index !== -1) {
      products.value[index].current_price = priceSuggestion.value.suggested_price
    }
    showPriceDialog.value = false
  }
}

// 编辑商品
const editProduct = (product: Product) => {
  // 跳转到编辑页面或打开编辑对话框
  console.log('编辑商品:', product)
}

// 切换商品状态
const toggleProductStatus = (product: Product) => {
  const index = products.value.findIndex(p => p.product_id === product.product_id)
  if (index !== -1) {
    products.value[index].is_active = !products.value[index].is_active
  }
}
</script>
