<!--
/**
 * ====================================
 * 代码任务: 主布局组件（侧边栏+顶部栏+内容区）
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */
-->

<template>
  <div class="min-h-screen bg-background flex">
    <!-- 侧边栏 -->
    <aside
      class="w-64 bg-white border-r border-gray-200 flex flex-col fixed h-full z-20 transition-all duration-300"
      :class="{ '-translate-x-full lg:translate-x-0': !sidebarOpen }"
    >
      <!-- Logo区域 -->
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold text-text">智营电商智能体</h1>
            <p class="text-xs text-text-muted">CommerceBot</p>
          </div>
        </div>
      </div>

      <!-- 店铺选择 -->
      <div class="p-4 border-b border-gray-200">
        <label class="text-xs font-medium text-text-muted uppercase tracking-wider">当前店铺</label>
        <select
          v-if="userStore.hasShops"
          v-model="userStore.currentShop"
          @change="handleShopChange"
          class="w-full mt-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 cursor-pointer"
        >
          <option v-for="shop in userStore.shops" :key="shop.shop_id" :value="shop">
            {{ shop.shop_name }}
          </option>
        </select>
        <div v-else class="mt-2 text-sm text-text-muted">暂无店铺</div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="{ name: item.name }"
          class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200"
          :class="
            $route.name === item.name
              ? 'bg-primary-100 text-primary-700'
              : 'text-text-muted hover:bg-gray-100 hover:text-text'
          "
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="font-medium">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- 用户信息 -->
      <div class="p-4 border-t border-gray-200">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-secondary rounded-full flex items-center justify-center text-white font-medium">
            {{ userStore.user?.username?.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-text truncate">{{ userStore.user?.username }}</p>
            <p class="text-xs text-text-muted truncate">{{ userStore.user?.email }}</p>
          </div>
          <button
            @click="handleLogout"
            class="p-2 text-text-muted hover:text-red-500 transition-colors duration-200"
            title="退出登录"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="flex-1 lg:ml-64">
      <!-- 顶部栏 -->
      <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div class="flex items-center justify-between px-6 py-4">
          <div class="flex items-center gap-4">
            <button
              @click="sidebarOpen = !sidebarOpen"
              class="lg:hidden p-2 text-text-muted hover:text-text transition-colors duration-200"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h2 class="text-xl font-semibold text-text">{{ currentPageTitle }}</h2>
          </div>

          <div class="flex items-center gap-4">
            <!-- 快速操作按钮 -->
            <router-link
              :to="{ name: 'Chat' }"
              class="flex items-center gap-2 px-4 py-2 bg-cta text-white rounded-lg hover:bg-cta-600 transition-colors duration-200"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span class="font-medium">AI助手</span>
            </router-link>
          </div>
        </div>
      </header>

      <!-- 内容区域 -->
      <main class="p-6">
        <router-view />
      </main>
    </div>

    <!-- 移动端遮罩 -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black bg-opacity-50 z-10 lg:hidden"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const sidebarOpen = ref(false)

// 菜单项配置
const menuItems = [
  {
    name: 'Dashboard',
    label: '数据看板',
    icon: 'DashboardIcon'
  },
  {
    name: 'Shops',
    label: '店铺管理',
    icon: 'StoreIcon'
  },
  {
    name: 'Products',
    label: '商品管理',
    icon: 'ProductIcon'
  },
  {
    name: 'Orders',
    label: '订单管理',
    icon: 'OrderIcon'
  },
  {
    name: 'Inventory',
    label: '库存管理',
    icon: 'InventoryIcon'
  },
  {
    name: 'Logistics',
    label: '物流管理',
    icon: 'LogisticsIcon'
  },
  {
    name: 'Chat',
    label: 'AI对话',
    icon: 'ChatIcon'
  }
]

// 当前页面标题
const currentPageTitle = computed(() => {
  const item = menuItems.find(i => i.name === router.currentRoute.value.name)
  return item?.label || '智营电商智能体'
})

// 处理店铺切换
const handleShopChange = () => {
  // 店铺切换后刷新当前页面数据
  router.go(0)
}

// 退出登录
const handleLogout = async () => {
  if (confirm('确定要退出登录吗？')) {
    await userStore.logout()
    router.push({ name: 'Login' })
  }
}

// 图标组件（简化版，实际应使用独立组件）
const DashboardIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
    </svg>
  `
}

const StoreIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
    </svg>
  `
}

const ProductIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
    </svg>
  `
}

const OrderIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
    </svg>
  `
}

const InventoryIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4m0 0H4m8 0h8" />
    </svg>
  `
}

const LogisticsIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
    </svg>
  `
}

const ChatIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
    </svg>
  `
}
</script>

<style scoped>
/* 移动端侧边栏动画 */
@media (max-width: 1024px) {
  aside {
    transition: transform 0.3s ease;
  }
}
</style>
