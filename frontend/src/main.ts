/**
 * ====================================
 * 代码任务: Vue应用入口文件
 * 最后修改: 2026-03-30 19:30
 * ====================================
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
