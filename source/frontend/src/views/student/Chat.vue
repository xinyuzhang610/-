<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2 class="chat-title">🤖 AI 学习助手</h2>
      <p class="chat-desc">我可以帮你解答学科问题、解释概念、提供学习建议</p>
    </div>

    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message-item"
        :class="message.role"
      >
        <div class="message-avatar">
          <span v-if="message.role === 'user'">👤</span>
          <span v-else>🤖</span>
        </div>
        <div class="message-content">
          <div class="message-text">{{ message.content }}</div>
          <div class="message-time">{{ message.time }}</div>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="message-item assistant">
        <div class="message-avatar">🤖</div>
        <div class="message-content">
          <div class="message-text loading">
            <span class="dot">.</span>
            <span class="dot">.</span>
            <span class="dot">.</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <el-input
        v-model="inputMessage"
        placeholder="输入你的问题..."
        size="large"
        class="message-input"
        @keyup.enter="sendMessage"
      >
        <template #append>
          <el-button @click="sendMessage" :loading="loading">发送</el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const messageListRef = ref(null)
const inputMessage = ref('')
const loading = ref(false)

// 消息列表
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    content: '你好！我是AI学习助手，可以帮你：\n· 解答学科问题\n· 解释概念和公式\n· 提供学习建议\n· 趣味科普\n\n有什么问题尽管问我吧！',
    time: '14:30'
  }
])

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  messages.value.push(userMessage)
  inputMessage.value = ''
  loading.value = true
  scrollToBottom()

  // TODO: 调用后端AI接口
  // 模拟AI回复
  setTimeout(() => {
    const aiMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: '这是一个模拟回复。后续会接入DeepSeek API，提供真实的AI对话体验。\n\n您可以问一些学习相关的问题，比如：\n· "静夜思"的赏析\n· 勾股定理的推导过程\n· 牛顿第三定律是什么',
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    }

    messages.value.push(aiMessage)
    loading.value = false
    scrollToBottom()
  }, 1500)
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

/* 头部 */
.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-chip-bg);
  background: var(--color-bg);
}

.chat-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 4px;
}

.chat-desc {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: var(--color-chip-bg);
  border-radius: 50%;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
}

.message-text {
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-ink);
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  white-space: pre-wrap;
}

.message-item.assistant .message-text {
  background: var(--color-chip-bg);
}

.message-item.user .message-text {
  background: var(--color-ink);
  color: white;
}

.message-time {
  font-family: var(--font-sans);
  font-size: 11px;
  color: var(--color-ink-soft);
  margin-top: 4px;
}

.message-item.user .message-time {
  text-align: right;
}

/* 加载动画 */
.message-text.loading {
  display: flex;
  gap: 4px;
}

.dot {
  animation: dot-bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 输入区域 */
.input-area {
  padding: 16px 24px;
  border-top: 1px solid var(--color-chip-bg);
  background: var(--color-bg);
}

.message-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: 0 0 0 1px var(--color-border) inset;
}

.message-input :deep(.el-input-group__append) {
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  background: var(--color-ink);
  border-color: var(--color-ink);
}

.message-input :deep(.el-input-group__append .el-button) {
  color: white;
}
</style>
