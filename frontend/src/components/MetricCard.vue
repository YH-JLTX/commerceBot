<!--
/**
 * ====================================
 * 代码任务: 指标卡片子组件
 * 最后修改: 2026-03-30 19:40
 * ====================================
 -->
-->

<template>
  <div class="card">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-text-muted">{{ title }}</p>
        <p class="text-2xl font-bold text-text mt-1">{{ value }}</p>
        <p
          v-if="growth !== undefined"
          class="text-sm mt-1"
          :class="growth >= 0 ? 'text-green-600' : 'text-red-600'"
        >
          {{ growth >= 0 ? '↑' : '↓' }} {{ Math.abs(growth) }}%
        </p>
      </div>
      <div
        class="w-12 h-12 rounded-xl flex items-center justify-center"
        :class="type === 'alert' ? 'bg-red-100' : 'bg-primary-100'"
      >
        <svg class="w-6 h-6" :class="type === 'alert' ? 'text-red-600' : 'text-primary'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="icon === 'dollar'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0-0V7m0 1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path v-else-if="icon === 'shopping'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 2.707M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8-2V9a2 2 0 00-2-2H9a2 2 0 00-2 2v2m8-4H4m8 0V5a2 2 0 00-2-2H9a2 2 0 00-2 2v14a2 2 0 002 2h2a2 2 0 002-2v-6m0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          <path v-else-if="icon === 'chart'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          <path v-else-if="icon === 'alert'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface MetricCardProps {
  title: string
  value: string | number
  growth?: number
  type?: 'default' | 'alert'
  icon: string
}

defineProps<MetricCardProps>()
</script>
