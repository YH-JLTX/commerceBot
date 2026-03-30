<!--
/**
 * ====================================
 * 代码任务: 快速操作卡片子组件
 * 最后修改: 2026-03-30 19:40
 * ====================================
 */
-->

<template>
  <div class="card text-center hover:shadow-md transition-shadow duration-200 cursor-pointer" @click="$emit('click')">
    <div class="w-12 h-12 bg-cta-100 rounded-xl flex items-center justify-center mx-auto mb-3">
      <svg class="w-6 h-6 text-cta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path v-if="icon === 'chart'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        <path v-else-if="icon === 'inventory'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        <path v-else-if="icon === 'logistics'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
        <path v-else-if="icon === 'pricing'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </div>
    <h4 class="font-semibold text-text">{{ title }}</h4>
    <p class="text-sm text-text-muted mt-1">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
interface QuickActionCardProps {
  title: string
  description: string
  icon: string
}

defineProps<QuickActionCardProps>()
defineEmits<{
  click: []
}>()
</script>
