<template>
  <div class="guidance-container">
    <div class="dialogue-area">
      <!-- 系统消息 -->
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="system-message"
        :style="{ animationDelay: index * 0.3 + 's' }"
      >
        <div class="system-avatar">🤖</div>
        <div class="system-bubble" v-html="msg.content"></div>
      </div>

      <!-- 选项区域 -->
      <div v-if="showOptions" class="options-area">
        <!-- 文理分科选项 -->
        <div v-if="currentStep === 0" class="category-options">
          <div
            v-for="option in categoryOptions"
            :key="option.value"
            class="category-card"
            :class="{ selected: selectedCategory === option.value }"
            @click="selectCategory(option.value)"
          >
            <div class="category-icon">{{ option.icon }}</div>
            <div class="category-name">{{ option.name }}</div>
            <div class="category-subjects">{{ option.subjects }}</div>
          </div>
        </div>

        <!-- 需求选项 -->
        <div v-if="currentStep === 1" class="need-options">
          <div
            v-for="option in needOptions"
            :key="option.value"
            class="need-option"
            :class="{ selected: selectedNeed === option.value }"
            @click="selectNeed(option.value)"
          >
            <div class="need-label">{{ option.label }}</div>
            <div class="need-desc">{{ option.description }}</div>
          </div>
        </div>

        <!-- 推荐工具 -->
        <div v-if="currentStep === 2" class="tool-recommendations">
          <div
            v-for="tool in recommendedTools"
            :key="tool.id"
            class="tool-recommendation-card"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-info">
              <div class="tool-name">{{ tool.name }}</div>
              <div class="tool-desc">{{ tool.description }}</div>
            </div>
            <div class="tool-actions">
              <button class="btn-primary" @click="useTool(tool)">立即体验</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 对话状态
const currentStep = ref(0)
const selectedCategory = ref('')
const selectedNeed = ref('')
const messages = ref([])
const showOptions = ref(false)

// 分类选项
const categoryOptions = [
  { value: '文科', icon: '📚', name: '文科', subjects: '语文 / 英语 / 历史 / 政治 / 地理' },
  { value: '理科', icon: '🔬', name: '理科', subjects: '数学 / 物理 / 化学 / 生物 / 信息技术' }
]

// 需求选项
const needOptions = [
  { value: 'preparation', label: '课前备课', description: '找资料、做课件、设计教学方案' },
  { value: 'teaching', label: '课堂教学', description: '互动、提问、演示、课堂管理' },
  { value: 'tutoring', label: '课后辅导', description: '作业批改、答疑、个性化辅导' },
  { value: 'interest', label: '学生兴趣激发', description: '趣味学习、游戏化教学、知识拓展' }
]

// 推荐工具
const getRecommendedTools = () => {
  if (selectedCategory.value === '文科') {
    return [
      { id: 1, icon: '🏮', name: '古诗词趣味赏析', description: '输入诗词名，获得趣味化赏析、背景知识、知识卡片' },
      { id: 2, icon: '✍️', name: '作文灵感助手', description: '输入作文题目/主题，获得写作思路和素材建议' },
      { id: 3, icon: '📖', name: '名词解释器', description: '输入专业名词，获得通俗易懂的解释' }
    ]
  } else {
    return [
      { id: 4, icon: '🧮', name: '公式推导助手', description: '输入公式名，获得推导过程和几何直觉解释' },
      { id: 5, icon: '🔬', name: '实验模拟讲解', description: '输入实验名，获得步骤讲解和注意事项' },
      { id: 6, icon: '🧠', name: '逻辑思维训练', description: '提供逻辑题并引导思考过程' }
    ]
  }
}

const recommendedTools = ref([])

// 添加消息
const addMessage = (content) => {
  messages.value.push({ content })
}

// 初始化对话
onMounted(() => {
  addMessage('你好！我是智教通助手。让我帮你找到最合适的AI教学工具。')

  setTimeout(() => {
    addMessage('首先，请告诉我你的教学方向：')
    showOptions.value = true
  }, 1000)
})

// 选择分类
const selectCategory = (value) => {
  selectedCategory.value = value
  showOptions.value = false

  addMessage(`太好了！你选择了${value}。`)

  setTimeout(() => {
    addMessage('接下来，告诉我你目前最需要帮助的是：')
    currentStep.value = 1
    showOptions.value = true
  }, 800)
}

// 选择需求
const selectNeed = (value) => {
  selectedNeed.value = value
  showOptions.value = false

  const need = needOptions.find(n => n.value === value)
  addMessage(`明白了！你需要帮助的是"${need.label}"。`)

  setTimeout(() => {
    addMessage('根据你的选择，我为你推荐以下工具：')
    recommendedTools.value = getRecommendedTools()
    currentStep.value = 2
    showOptions.value = true
  }, 800)
}

// 使用工具
const useTool = (tool) => {
  router.push(`/tool/${tool.id}`)
}
</script>

<style scoped>
.guidance-container {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-xl);
}

.dialogue-area {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

/* 系统消息 */
.system-message {
  display: flex;
  gap: var(--space-md);
  align-items: flex-start;
  opacity: 0;
  transform: translateY(12px);
  animation: messageIn var(--duration-normal) var(--ease-out) forwards;
}

.system-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-chip-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.system-bubble {
  background: white;
  border: 1px solid var(--color-chip-bg);
  border-radius: var(--radius-lg);
  border-bottom-left-radius: 4px;
  padding: var(--space-md) var(--space-lg);
  max-width: 85%;
  box-shadow: var(--shadow-sm);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.6;
  color: var(--color-ink);
}

@keyframes messageIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 选项区域 */
.options-area {
  margin-top: var(--space-md);
  animation: fadeIn var(--duration-normal) var(--ease-out);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 分类选项 */
.category-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.category-card {
  background: white;
  border: 2px solid var(--color-chip-bg);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  text-align: center;
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-out);
}

.category-card:hover {
  border-color: var(--color-ink);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.category-card.selected {
  border-color: var(--color-ink);
  background: var(--color-chip-bg);
}

.category-icon {
  font-size: 40px;
  margin-bottom: var(--space-sm);
}

.category-name {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-xs);
}

.category-subjects {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 需求选项 */
.need-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.need-option {
  background: white;
  border: 2px solid var(--color-chip-bg);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-out);
}

.need-option:hover {
  border-color: var(--color-ink);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.need-option.selected {
  border-color: var(--color-ink);
  background: var(--color-chip-bg);
}

.need-label {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-xs);
}

.need-desc {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 推荐工具 */
.tool-recommendations {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.tool-recommendation-card {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  background: white;
  border: 2px solid var(--color-chip-bg);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  transition: all var(--duration-normal) var(--ease-out);
}

.tool-recommendation-card:hover {
  border-color: var(--color-ink);
  box-shadow: var(--shadow-md);
}

.tool-recommendation-card .tool-icon {
  font-size: 40px;
  flex-shrink: 0;
}

.tool-recommendation-card .tool-info {
  flex: 1;
}

.tool-recommendation-card .tool-name {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-xs);
}

.tool-recommendation-card .tool-desc {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-sm) var(--space-lg);
  background: var(--color-primary);
  color: white;
  font-family: var(--font-ui);
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: background var(--duration-fast) ease;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}

/* 响应式 */
@media (max-width: 768px) {
  .guidance-container {
    padding: var(--space-md);
  }

  .category-options {
    grid-template-columns: 1fr;
  }

  .tool-recommendation-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>
