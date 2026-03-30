/**
 * ====================================
 * 代码任务: 用户状态管理Store
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */

import { defineStore } from 'pinia'
import type { User, Shop } from '@/types'
import { login, logout, getShops } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem('token') || null,
    shops: [] as Shop[],
    currentShop: null as Shop | null,
    isLoading: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    hasShops: (state) => state.shops.length > 0
  },

  actions: {
    async login(username: string, password: string) {
      this.isLoading = true
      try {
        const result = await login(username, password)
        this.token = result.token
        this.user = result.user
        localStorage.setItem('token', result.token)
        await this.fetchShops()
        return true
      } catch (error) {
        console.error('登录失败:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      await logout()
      this.token = null
      this.user = null
      this.shops = []
      this.currentShop = null
      localStorage.removeItem('token')
    },

    async fetchShops() {
      if (!this.user) return
      this.shops = await getShops()
      // 自动选择第一个活跃店铺
      const activeShop = this.shops.find(s => s.status === 'active')
      if (activeShop) {
        this.setCurrentShop(activeShop)
      }
    },

    setCurrentShop(shop: Shop) {
      this.currentShop = shop
      localStorage.setItem('currentShopId', String(shop.shop_id))
    }
  }
})
