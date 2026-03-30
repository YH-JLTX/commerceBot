/**
 * ====================================
 * 代码任务: 聊天状态管理Store
 * 最后修改: 2026-03-30 18:00
 * ====================================
 */

import { defineStore } from 'pinia'
import type { ChatMessage } from '@/types'
import { sendChatMessage, getChatHistory, clearChatHistory, type AgentWebSocket } from '@/api/agent'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as ChatMessage[],
    isLoading: false,
    currentThinking: '',
    sessionId: null as string | null,
    ws: null as AgentWebSocket | null
  }),

  getters: {
    hasMessages: (state) => state.messages.length > 0
  },

  actions: {
    async loadHistory() {
      this.messages = await getChatHistory(this.sessionId || undefined)
    },

    async sendMessage(query: string) {
      if (!query.trim()) return

      this.isLoading = true
      this.currentThinking = ''

      try {
        const response = await sendChatMessage({
          query,
          shop_id: this.currentShopId,
          session_id: this.sessionId || undefined
        })

        this.sessionId = response.session_id || this.sessionId

        // 如果有思考过程，逐条显示
        if (response.thought_process) {
          for (const step of response.thought_process) {
            this.currentThinking = `${step.step}: ${step.content}`
            await new Promise(resolve => setTimeout(resolve, 300))
          }
        }

        this.currentThinking = ''
      } catch (error) {
        console.error('发送消息失败:', error)
      } finally {
        this.isLoading = false
      }
    },

    async clearHistory() {
      await clearChatHistory()
      this.messages = []
      this.sessionId = null
    },

    connectWebSocket(userId: string) {
      this.ws = new AgentWebSocket(userId)
      this.ws.onThinking = (content: string) => {
        this.currentThinking = content
      }
      this.ws.onMessage = (content: string) => {
        // WebSocket实时消息处理
      }
      this.ws.onAlert = (alert: any) => {
        // 预警消息处理
      }
      this.ws.connect()
    },

    disconnectWebSocket() {
      if (this.ws) {
        this.ws.disconnect()
        this.ws = null
      }
    }
  }
})
