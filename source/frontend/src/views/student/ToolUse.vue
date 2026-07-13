<template>
  <div class="tool-use-container">
    <!-- 顶部导航 -->
    <div class="tool-header">
      <div class="header-left">
        <el-button @click="goBack" text>
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <span class="tool-icon">{{ toolInfo.icon }}</span>
        <h1 class="tool-name">{{ toolInfo.name }}</h1>
      </div>
      <div class="header-right">
        <el-button @click="shareTool">分享</el-button>
        <el-button @click="collectTool">
          {{ isCollected ? '已收藏' : '收藏' }}
        </el-button>
      </div>
    </div>

    <!-- 工具描述 -->
    <div class="tool-desc">
      <p>{{ toolInfo.description }}</p>
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
          <span v-else>{{ toolInfo.icon }}</span>
        </div>
        <div class="message-content">
          <div class="message-text">{{ message.content }}</div>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="message-item assistant">
        <div class="message-avatar">{{ toolInfo.icon }}</div>
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
        :placeholder="toolInfo.inputPlaceholder"
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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const messageListRef = ref(null)
const inputMessage = ref('')
const loading = ref(false)
const isCollected = ref(false)

// 工具信息（模拟数据，后续从后端获取）
const toolInfo = ref({
  id: route.params.id,
  name: '古诗词趣味小助手',
  icon: '🏮',
  description: '输入你想了解的古诗词，获得趣味化的赏析、背景知识和知识卡片'
})

// 消息列表
const messages = ref([])

// 获取工具信息
onMounted(() => {
  // TODO: 根据工具ID从后端获取工具信息
  // 模拟数据
  const toolId = route.params.id
  const toolMap = {
    '1': { name: '古诗词趣味小助手', icon: '🏮', description: '输入你想了解的古诗词，获得趣味化的赏析、背景知识和知识卡片', inputPlaceholder: '请输入你想了解的古诗词...' },
    '2': { name: '作文灵感助手', icon: '✍️', description: '输入作文题目或主题，获得写作思路和素材建议', inputPlaceholder: '请输入作文题目或主题...' },
    '7': { name: '公式推导助手', icon: '🧮', description: '输入公式名称，获得详细的推导过程和几何直觉解释', inputPlaceholder: '请输入公式名称...' }
  }

  if (toolMap[toolId]) {
    toolInfo.value = { ...toolMap[toolId], id: toolId }
  }

  // 添加欢迎消息
  messages.value = [{
    id: 1,
    role: 'assistant',
    content: `你好！我是${toolInfo.value.name}，${toolInfo.value.description}。\n\n请告诉我你想了解的内容吧！`
  }]
})

// 滚动到底部
const scrollToBottom = () => {
  setTimeout(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  }, 100)
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputMessage.value
  }

  messages.value.push(userMessage)
  const userInput = inputMessage.value
  inputMessage.value = ''
  loading.value = true
  scrollToBottom()

  // TODO: 调用后端AI接口
  // 模拟AI回复
  setTimeout(() => {
    const aiMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: `这是关于"${userInput}"的模拟回复。\n\n后续会接入DeepSeek API，提供真实的AI对话体验。`
    }

    messages.value.push(aiMessage)
    loading.value = false
    scrollToBottom()
  }, 1500)
}

// 返回
const goBack = () => {
  router.back()
}

// 分享工具
const shareTool = () => {
  const link = `${window.location.origin}/tool/${toolInfo.value.id}`
  navigator.clipboard.writeText(link)
  ElMessage.success('分享链接已复制')
}

// 收藏工具
const collectTool = () => {
  isCollected.value = !isCollected.value
  ElMessage.success(isCollected.value ? '已收藏' : '已取消收藏')
}
</script>

<style scoped>
.tool-use-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

/* 顶部导航 */
.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid var(--color-chip-bg);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tool-icon {
  font-size: 28px;
}

.tool-name {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
}

/* 工具描述 */
.tool-desc {
  padding: 12px 24px;
  background: white;
  border-bottom: 1px solid var(--color-chip-bg);
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
  background: white;
  box-shadow: var(--shadow-sm);
}

.message-item.user .message-text {
  background: var(--color-ink);
  color: white;
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
  background: white;
  border-top: 1px solid var(--color-chip-bg);
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
