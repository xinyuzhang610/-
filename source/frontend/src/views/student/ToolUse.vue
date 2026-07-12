<template>
  <div class="tool-use">
    <el-card class="tool-card" v-if="tool">
      <template #header>
        <div class="tool-header">
          <span class="tool-icon">{{ tool.icon }}</span>
          <span class="tool-name">{{ tool.name }}</span>
        </div>
      </template>

      <div class="tool-description">
        <p>{{ tool.description }}</p>
      </div>

      <div class="chat-section">
        <div class="chat-messages" ref="messagesContainer">
          <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>

        <div class="chat-input">
          <el-input v-model="inputMessage" :placeholder="'输入内容开始使用...'" @keyup.enter="sendMessage">
            <template #append>
              <el-button @click="sendMessage" :loading="loading">发送</el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>

    <el-card v-else class="loading-card">
      <el-skeleton :rows="5" animated />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { getTool } from '@/api/tools'
import { sendMessage as sendChatMessage } from '@/api/chat'
import { ElMessage } from 'element-plus'

const route = useRoute()
const tool = ref(null)
const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

onMounted(async () => {
  const toolId = route.params.toolId
  try {
    const { data } = await getTool(toolId)
    tool.value = data
    messages.value.push({
      role: 'assistant',
      content: `你好！我是${data.name}，${data.description}。请输入内容开始使用。`
    })
  } catch (error) {
    ElMessage.error('加载工具失败')
  }
})

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value || !tool.value) return

  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''

  await nextTick()
  scrollToBottom()

  loading.value = true
  try {
    const { data } = await sendChatMessage({
      message: userMessage,
      tool_id: tool.value.id
    })
    messages.value.push({ role: 'assistant', content: data.reply })
  } catch (error) {
    ElMessage.error('发送失败，请重试')
    messages.value.pop()
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.tool-use {
  max-width: 800px;
  margin: 0 auto;
}
.tool-card {
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}
.tool-header {
  display: flex;
  align-items: center;
}
.tool-icon {
  font-size: 24px;
  margin-right: 10px;
}
.tool-name {
  font-size: 18px;
  font-weight: bold;
}
.tool-description {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 15px;
  max-height: 400px;
}
.message {
  margin-bottom: 15px;
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
}
.message.assistant .message-content {
  background: #fff;
  border: 1px solid #eee;
}
.message.user .message-content {
  background: #409eff;
  color: #fff;
}
.chat-input {
  padding: 15px 0;
}
</style>
