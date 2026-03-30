<!--
/**
 * ====================================
 * 代码任务: 登录页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */
-->

<template>
  <div class="min-h-screen bg-background flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-text">智营电商智能体</h1>
        <p class="text-text-muted mt-2">CommerceBot - 您的AI运营专家</p>
      </div>

      <!-- 登录表单 -->
      <div class="card">
        <h2 class="text-xl font-semibold text-text mb-6">登录账号</h2>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-text mb-2">用户名</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              class="input-field"
              placeholder="请输入用户名"
              required
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-text mb-2">密码</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="input-field"
              placeholder="请输入密码"
              required
            />
          </div>

          <div
            v-if="errorMessage"
            class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600"
          >
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg
              v-if="isLoading"
              class="w-5 h-5 animate-spin"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ isLoading ? '登录中...' : '登录' }}</span>
          </button>
        </form>

        <div class="mt-6 text-center text-sm text-text-muted">
          <p>测试账号：test_user1 / password123</p>
        </div>
      </div>

      <!-- 功能介绍 -->
      <div class="mt-8 grid grid-cols-2 gap-4">
        <div class="card text-center">
          <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="font-medium text-text">智能分析</h3>
          <p class="text-xs text-text-muted mt-1">AI驱动的数据洞察</p>
        </div>

        <div class="card text-center">
          <div class="w-12 h-12 bg-secondary-100 rounded-xl flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="font-medium text-text">自动运营</h3>
          <p class="text-xs text-text-muted mt-1">24/7智能决策执行</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formData = ref({
  username: 'test_user1',
  password: 'password123'
})

const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const success = await userStore.login(formData.value.username, formData.value.password)
    if (success) {
      router.push({ name: 'Dashboard' })
    } else {
      errorMessage.value = '用户名或密码错误'
    }
  } catch (error) {
    errorMessage.value = '登录失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>
