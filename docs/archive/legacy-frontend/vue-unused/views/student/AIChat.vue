<template>
  <div class="ai-chat">
    <el-card class="chat-card">
      <template #header>
        <span>AI 学习助手</span>
      </template>

      <div class="chat-hints">
        <p>我可以帮你：</p>
        <div class="hint-tags">
          <el-tag v-for="hint in hints" :key="hint" @click="sendHint(hint)" class="hint-tag">
            {{ hint }}
          </el-tag>
        </div>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          <div class="message-content">{{ msg.content }}</div>
        </div>
      </div>

      <div class="chat-input">
        <el-input v-model="inputMessage" placeholder="输入你的问题..." @keyup.enter="sendMsg">
          <template #append>
            <el-button @click="sendMsg" :loading="loading">发送</el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { sendMessage } from '@/api/chat'
import { ElMessage } from 'element-plus'

const inputMessage = ref('')
const messages = ref([
  { role: 'assistant', content: '你好！我是AI学习助手，有什么可以帮你的吗？' }
])
const loading = ref(false)
const messagesContainer = ref(null)

const hints = [
  '帮我解释勾股定理',
  '推荐一些学习方法',
  '什么是人工智能？',
  '如何提高写作能力？'
]

const sendHint = (hint) => {
  inputMessage.value = hint
  sendMsg()
}

const sendMsg = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''

  await nextTick()
  scrollToBottom()

  loading.value = true
  try {
    const { data } = await sendMessage({ message: userMessage })
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
.ai-chat {
  max-width: 800px;
  margin: 0 auto;
}
.chat-card {
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}
.chat-hints {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.chat-hints p {
  margin-bottom: 10px;
  color: #666;
}
.hint-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.hint-tag {
  cursor: pointer;
}
.hint-tag:hover {
  background: #409eff;
  color: #fff;
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
