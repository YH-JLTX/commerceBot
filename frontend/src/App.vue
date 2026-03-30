<!--
/**
 * ====================================
 * 代码任务: Vue应用根组件
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */
-->

<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  // 如果有token，恢复用户状态
  if (userStore.token) {
    userStore.fetchShops()
  }
})
</script>

<style>
/* 全局样式在 style.css 中定义 */
</style>
