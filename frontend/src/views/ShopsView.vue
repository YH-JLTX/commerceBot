<!--
/**
 * ====================================
 * 代码任务: 店铺管理页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */
-->

<template>
  <div class="space-y-6">
    <!-- 页面头部 -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-semibold text-text">店铺管理</h2>
        <p class="text-text-muted mt-1">管理您的所有电商店铺</p>
      </div>
      <button @click="showCreateDialog = true" class="btn-primary flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>添加店铺</span>
      </button>
    </div>

    <!-- 店铺列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="shop in shops"
        :key="shop.shop_id"
        class="card hover:shadow-md transition-shadow duration-200"
        :class="{ 'ring-2 ring-primary': shop.shop_id === userStore.currentShop?.shop_id }"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-text">{{ shop.shop_name }}</h3>
              <span class="inline-block px-2 py-0.5 text-xs rounded-full mt-1" :class="getShopTypeClass(shop.shop_type)">
                {{ getShopTypeLabel(shop.shop_type) }}
              </span>
            </div>
          </div>
          <div class="relative">
            <button @click="toggleMenu(shop.shop_id)" class="p-1 hover:bg-gray-100 rounded-lg transition-colors duration-200">
              <svg class="w-5 h-5 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
              </svg>
            </button>
            <div v-if="activeMenu === shop.shop_id" class="absolute right-0 top-full mt-1 w-32 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
              <button @click="editShop(shop)" class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 transition-colors duration-200">
                编辑
              </button>
              <button @click="deleteShop(shop)" class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 transition-colors duration-200">
                删除
              </button>
            </div>
          </div>
        </div>

        <p class="text-sm text-text-muted mb-4 line-clamp-2">{{ shop.description }}</p>

        <!-- 店铺状态 -->
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm text-text-muted">状态</span>
          <span class="px-2 py-1 text-xs rounded-full" :class="getStatusClass(shop.status)">
            {{ getStatusLabel(shop.status) }}
          </span>
        </div>

        <!-- 店铺数据概览 -->
        <div class="grid grid-cols-3 gap-2 pt-4 border-t border-gray-200">
          <div class="text-center">
            <p class="text-lg font-semibold text-text">{{ getShopStats(shop.shop_id).products }}</p>
            <p class="text-xs text-text-muted">商品</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-text">{{ getShopStats(shop.shop_id).orders }}</p>
            <p class="text-xs text-text-muted">订单</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-semibold text-text">¥{{ getShopStats(shop.shop_id).gmv }}</p>
            <p class="text-xs text-text-muted">GMV</p>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-2 mt-4 pt-4 border-t border-gray-200">
          <button
            @click="selectShop(shop)"
            class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
          >
            切换
          </button>
          <button
            @click="goToDashboard(shop)"
            class="flex-1 px-3 py-2 text-sm bg-primary text-white rounded-lg hover:bg-primary-600 transition-colors duration-200"
          >
            管理店铺
          </button>
        </div>
      </div>
    </div>

    <!-- 创建/编辑对话框 -->
    <div v-if="showCreateDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md mx-4">
        <div class="p-6 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-text">{{ editingShop ? '编辑店铺' : '添加店铺' }}</h3>
        </div>
        <form @submit.prevent="saveShop" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-text mb-2">店铺名称 *</label>
            <input
              v-model="shopForm.name"
              type="text"
              class="input-field"
              placeholder="请输入店铺名称"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-text mb-2">平台类型 *</label>
            <select v-model="shopForm.type" class="input-field" required>
              <option value="taobao">淘宝</option>
              <option value="jd">京东</option>
              <option value="pinduoduo">拼多多</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text mb-2">店铺描述</label>
            <textarea
              v-model="shopForm.description"
              rows="3"
              class="input-field"
              placeholder="请输入店铺描述"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-text mb-2">店铺URL</label>
            <input
              v-model="shopForm.url"
              type="url"
              class="input-field"
              placeholder="https://"
            />
          </div>
        </form>
        <div class="p-6 border-t border-gray-200 flex justify-end gap-3">
          <button
            @click="closeDialog"
            class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
          >
            取消
          </button>
          <button @click="saveShop" class="btn-primary">
            保存
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
import { getShops, createShop } from '@/api'
import type { Shop } from '@/types'

const router = useRouter()
const userStore = useUserStore()

const shops = ref<Shop[]>([])
const showCreateDialog = ref(false)
const editingShop = ref<Shop | null>(null)
const activeMenu = ref<number | null>(null)

const shopForm = ref({
  name: '',
  type: 'taobao',
  description: '',
  url: ''
})

// 加载店铺列表
onMounted(async () => {
  shops.value = await getShops()
})

// 选择店铺
const selectShop = (shop: Shop) => {
  userStore.setCurrentShop(shop)
  activeMenu.value = null
}

// 切换到店铺仪表板
const goToDashboard = (shop: Shop) => {
  userStore.setCurrentShop(shop)
  router.push({ name: 'Dashboard' })
}

// 编辑店铺
const editShop = (shop: Shop) => {
  editingShop.value = shop
  shopForm.value = {
    name: shop.shop_name,
    type: shop.shop_type,
    description: shop.description || '',
    url: shop.shop_url || ''
  }
  showCreateDialog.value = true
  activeMenu.value = null
}

// 删除店铺
const deleteShop = (shop: Shop) => {
  if (confirm(`确定要删除店铺"${shop.shop_name}"吗？`)) {
    shops.value = shops.value.filter(s => s.shop_id !== shop.shop_id)
    activeMenu.value = null
  }
}

// 保存店铺
const saveShop = async () => {
  if (editingShop.value) {
    // 更新店铺
    const index = shops.value.findIndex(s => s.shop_id === editingShop.value!.shop_id)
    if (index !== -1) {
      shops.value[index] = {
        ...shops.value[index],
        shop_name: shopForm.value.name,
        shop_type: shopForm.value.type as any,
        description: shopForm.value.description,
        shop_url: shopForm.value.url
      }
    }
  } else {
    // 创建新店铺
    const newShop = await createShop({
      shop_name: shopForm.value.name,
      shop_type: shopForm.value.type as any,
      description: shopForm.value.description,
      shop_url: shopForm.value.url
    })
    shops.value.push(newShop)
  }
  closeDialog()
}

// 关闭对话框
const closeDialog = () => {
  showCreateDialog.value = false
  editingShop.value = null
  shopForm.value = { name: '', type: 'taobao', description: '', url: '' }
}

// 切换菜单
const toggleMenu = (shopId: number) => {
  activeMenu.value = activeMenu.value === shopId ? null : shopId
}

// 工具函数
const getShopTypeLabel = (type: string) => {
  const labels = { taobao: '淘宝', jd: '京东', pinduoduo: '拼多多', other: '其他' }
  return labels[type as keyof typeof labels] || type
}

const getShopTypeClass = (type: string) => {
  const classes = {
    taobao: 'bg-orange-100 text-orange-700',
    jd: 'bg-red-100 text-red-700',
    pinduoduo: 'bg-pink-100 text-pink-700',
    other: 'bg-gray-100 text-gray-700'
  }
  return classes[type as keyof typeof classes] || ''
}

const getStatusLabel = (status: string) => {
  const labels = { active: '正常', inactive: '未激活', suspended: '已封禁' }
  return labels[status as keyof typeof labels] || status
}

const getStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-700',
    inactive: 'bg-gray-100 text-gray-700',
    suspended: 'bg-red-100 text-red-700'
  }
  return classes[status as keyof typeof classes] || ''
}

const getShopStats = (shopId: number) => {
  // 模拟数据，实际应从API获取
  const stats = {
    1: { products: 45, orders: 156, gmv: '15.8万' },
    2: { products: 23, orders: 89, gmv: '8.2万' }
  }
  return stats[shopId as keyof typeof stats] || { products: 0, orders: 0, gmv: '0' }
}
</script>
