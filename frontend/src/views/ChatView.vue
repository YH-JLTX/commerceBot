<!--
/**
 * ====================================
 * 代码任务: AI对话页面
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */
-->

<template>
  <div class="h-[calc(100vh-120px)] flex">
    <!-- 聊天主区域 -->
    <div class="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <!-- 消息列表 -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- 欢迎消息 -->
        <div v-if="!chatStore.hasMessages" class="text-center py-12">
          <div class="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-10 h-10 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-text mb-2">您好！我是您的电商智能运营助手</h3>
          <p class="text-text-muted mb-6">我可以帮您分析数据、优化定价、管理库存、跟踪物流等</p>

          <!-- 快捷问题 -->
          <div class="max-w-2xl mx-auto">
            <p class="text-sm text-text-muted mb-3">试试问我：</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button
                v-for="prompt in quickPrompts"
                :key="prompt"
                @click="sendQuickPrompt(prompt)"
                class="p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-left text-sm text-text transition-colors duration-200"
              >
                {{ prompt }}
              </button>
            </div>
          </div>
        </div>

        <!-- 消息列表 -->
        <div
          v-for="(message, index) in chatStore.messages"
          :key="index"
          class="flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <!-- 用户消息 -->
          <div v-if="message.role === 'user'" class="max-w-[70%]">
            <div class="bg-primary text-white px-4 py-3 rounded-2xl rounded-tr-sm">
              <p class="whitespace-pre-wrap">{{ message.content }}</p>
            </div>
            <p class="text-xs text-text-muted mt-1 text-right">{{ formatTime(message.timestamp) }}</p>
          </div>

          <!-- AI消息 -->
          <div v-else class="max-w-[70%]">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-secondary rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div class="flex-1">
                <!-- 思考过程 -->
                <div v-if="message.thought_process && message.thought_process.length > 0" class="mb-3">
                  <details class="text-sm">
                    <summary class="cursor-pointer text-text-muted hover:text-text transition-colors duration-200">
                      🔍 查看思考过程
                    </summary>
                    <div class="mt-2 p-3 bg-gray-50 rounded-lg space-y-2">
                      <div
                        v-for="(step, i) in message.thought_process"
                        :key="i"
                        class="flex items-start gap-2"
                      >
                        <span class="font-medium" :class="{
                          'text-blue-600': step.step === 'thought',
                          'text-green-600': step.step === 'action',
                          'text-purple-600': step.step === 'observation'
                        }">
                          {{ step.step }}:
                        </span>
                        <span class="text-text-muted text-xs">{{ step.content }}</span>
                      </div>
                    </div>
                  </details>
                </div>

                <!-- AI回复 -->
                <div class="bg-gray-100 text-text px-4 py-3 rounded-2xl rounded-tl-sm">
                  <div class="prose prose-sm max-w-none whitespace-pre-wrap">{{ message.content }}</div>
                </div>

                <!-- Agent信息 -->
                <div v-if="message.agent_used" class="mt-1 text-xs text-text-muted">
                  🤖 {{ message.agent_used }}
                </div>

                <p class="text-xs text-text-muted mt-1">{{ formatTime(message.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 思考中状态 -->
        <div v-if="chatStore.isLoading" class="flex justify-start">
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 bg-secondary rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="bg-gray-100 px-4 py-3 rounded-2xl rounded-tl-sm">
              <div v-if="chatStore.currentThinking" class="text-sm text-text-muted">
                {{ chatStore.currentThinking }}
              </div>
              <div v-else class="flex gap-1">
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-gray-200 p-4">
        <div class="flex gap-3">
          <textarea
            v-model="userInput"
            @keydown.enter.exact.prevent="sendMessage"
            placeholder="输入您的问题，如：分析一下上周的销售情况..."
            rows="2"
            class="flex-1 resize-none px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
            :disabled="chatStore.isLoading"
          ></textarea>
          <button
            @click="sendMessage"
            :disabled="!userInput.trim() || chatStore.isLoading"
            class="self-end px-6 py-3 bg-primary text-white rounded-xl hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <span>发送</span>
          </button>
        </div>
        <div class="flex items-center justify-between mt-3 text-sm text-text-muted">
          <div class="flex items-center gap-4">
            <button class="hover:text-text transition-colors duration-200">📎 附件</button>
            <button class="hover:text-text transition-colors duration-200">📷 图片</button>
          </div>
          <button
            @click="chatStore.clearHistory()"
            class="hover:text-red-500 transition-colors duration-200"
          >
            清空对话
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧快捷功能面板 -->
    <div class="w-80 ml-6 space-y-4">
      <!-- Agent状态 -->
      <div class="card">
        <h3 class="font-semibold text-text mb-3">Agent状态</h3>
        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span class="text-text-muted">Master Agent</span>
            <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">运行中</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-text-muted">子Agent</span>
            <span class="text-text">7个可用</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-text-muted">WebSocket</span>
            <span class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">已连接</span>
          </div>
        </div>
      </div>

      <!-- 常用功能 -->
      <div class="card">
        <h3 class="font-semibold text-text mb-3">常用功能</h3>
        <div class="space-y-2">
          <button
            @click="sendQuickPrompt('生成今日销售日报')"
            class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200 text-left"
          >
            <span class="text-xl">📊</span>
            <span class="text-sm">生成今日销售日报</span>
          </button>
          <button
            @click="sendQuickPrompt('检查库存预警')"
            class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200 text-left"
          >
            <span class="text-xl">📦</span>
            <span class="text-sm">检查库存预警</span>
          </button>
          <button
            @click="sendQuickPrompt('查看物流异常')"
            class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200 text-left"
          >
            <span class="text-xl">🚚</span>
            <span class="text-sm">查看物流异常</span>
          </button>
          <button
            @click="sendQuickPrompt('帮我优化商品定价')"
            class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200 text-left"
          >
            <span class="text-xl">💰</span>
            <span class="text-sm">优化商品定价</span>
          </button>
        </div>
      </div>

      <!-- 对话历史 -->
      <div class="card">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-semibold text-text">最近对话</h3>
          <button @click="chatStore.clearHistory()" class="text-sm text-text-muted hover:text-red-500">
            清空
          </button>
        </div>
        <div v-if="chatStore.hasMessages" class="space-y-2 max-h-40 overflow-y-auto">
          <div
            v-for="(msg, i) in chatStore.messages.slice(-5).reverse()"
            :key="i"
            class="p-2 bg-gray-50 rounded-lg text-sm"
          >
            <p class="text-text-muted truncate">{{ msg.role === 'user' ? '我' : 'AI' }}: {{ msg.content }}</p>
          </div>
        </div>
        <p v-else class="text-sm text-text-muted text-center py-4">暂无对话记录</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'

const chatStore = useChatStore()
const userStore = useUserStore()

const userInput = ref('')
const messagesContainer = ref<HTMLElement>()

// 快捷问题
const quickPrompts = [
  '分析一下上周的销售情况',
  '帮我优化商品定价',
  '检查库存预警',
  '查看物流异常',
  '生成今日销售日报',
  '哪个商品销量最好？'
]

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || chatStore.isLoading) return

  const query = userInput.value
  userInput.value = ''

  await chatStore.sendMessage(query)

  await nextTick()
  scrollToBottom()
}

// 发送快捷问题
const sendQuickPrompt = async (prompt: string) => {
  userInput.value = prompt
  await sendMessage()
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  // 加载历史消息
  chatStore.loadHistory()

  // 连接WebSocket
  if (userStore.user) {
    chatStore.connectWebSocket(userStore.user.user_id.toString())
  }

  nextTick(() => scrollToBottom())
})

onUnmounted(() => {
  chatStore.disconnectWebSocket()
})
</script>
