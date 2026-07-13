<template>
  <div class="guide-container">
    <!-- 步骤条 -->
    <el-steps :active="currentStep" finish-status="success" class="guide-steps">
      <el-step title="选择方向" description="文科或理科" />
      <el-step title="需求引导" description="发现真实需求" />
      <el-step title="工具推荐" description="为您推荐" />
      <el-step title="创建工具" description="AI对话或平台" />
    </el-steps>

    <!-- 步骤内容 -->
    <div class="step-content">
      <!-- 步骤1：文理分科 -->
      <div v-if="currentStep === 0" class="step-card">
        <h2 class="step-title">请选择您的教学方向</h2>
        <p class="step-desc">选择后将为您推荐对应领域的工具</p>

        <div class="category-cards">
          <div
            class="category-card"
            :class="{ active: selectedCategory === '文科' }"
            @click="selectCategory('文科')"
          >
            <div class="category-icon">📚</div>
            <h3 class="category-name">文科</h3>
            <p class="category-subjects">语文 / 英语 / 历史 / 政治 / 地理</p>
          </div>

          <div
            class="category-card"
            :class="{ active: selectedCategory === '理科' }"
            @click="selectCategory('理科')"
          >
            <div class="category-icon">🔬</div>
            <h3 class="category-name">理科</h3>
            <p class="category-subjects">数学 / 物理 / 化学 / 生物 / 信息技术</p>
          </div>
        </div>

        <el-button
          type="primary"
          size="large"
          :disabled="!selectedCategory"
          @click="nextStep"
        >
          下一步
        </el-button>
      </div>

      <!-- 步骤2：需求引导 -->
      <div v-if="currentStep === 1" class="step-card">
        <h2 class="step-title">您目前最需要帮助的是？</h2>
        <p class="step-desc">根据您的需求推荐最合适的工具</p>

        <div class="need-list">
          <div
            v-for="need in needOptions"
            :key="need.value"
            class="need-item"
            :class="{ active: selectedNeed === need.value }"
            @click="selectNeed(need.value)"
          >
            <el-radio :model-value="selectedNeed" :label="need.value">
              {{ need.label }}
            </el-radio>
            <p class="need-desc">{{ need.description }}</p>
          </div>
        </div>

        <div class="step-buttons">
          <el-button size="large" @click="prevStep">上一步</el-button>
          <el-button
            type="primary"
            size="large"
            :disabled="!selectedNeed"
            @click="nextStep"
          >
            下一步
          </el-button>
        </div>
      </div>

      <!-- 步骤3：工具推荐 -->
      <div v-if="currentStep === 2" class="step-card">
        <h2 class="step-title">根据您的选择，推荐以下工具</h2>
        <p class="step-desc">{{ selectedCategory }} · {{ getNeedLabel(selectedNeed) }}</p>

        <div class="tool-list">
          <div
            v-for="tool in recommendedTools"
            :key="tool.id"
            class="tool-card"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-info">
              <h3 class="tool-name">{{ tool.name }}</h3>
              <p class="tool-desc">{{ tool.description }}</p>
            </div>
            <div class="tool-actions">
              <el-button type="primary" size="small" @click="useTool(tool)">
                立即体验
              </el-button>
              <el-button size="small" @click="viewToolDetail(tool)">
                了解更多
              </el-button>
            </div>
          </div>
        </div>

        <div class="no-tool-section">
          <el-divider>没有找到想要的？</el-divider>
          <p class="no-tool-desc">您可以：</p>
          <div class="no-tool-actions">
            <el-button type="primary" @click="nextStep">
              🤖 AI对话创建
            </el-button>
            <el-button @click="goToPlatform">
              🔧 平台创建工作流
            </el-button>
          </div>
        </div>

        <div class="step-buttons">
          <el-button size="large" @click="prevStep">上一步</el-button>
          <el-button type="primary" size="large" @click="nextStep">
            下一步
          </el-button>
        </div>
      </div>

      <!-- 步骤4：创建工具 -->
      <div v-if="currentStep === 3" class="step-card">
        <h2 class="step-title">选择创建方式</h2>
        <p class="step-desc">推荐使用AI对话创建，简单快捷</p>

        <div class="create-methods">
          <div class="method-card" @click="startAICreate">
            <div class="method-icon">🤖</div>
            <h3 class="method-name">AI对话创建</h3>
            <p class="method-desc">直接告诉AI你的需求，系统自动生成工具配置</p>
            <el-button type="primary">开始对话</el-button>
          </div>

          <div class="method-card" @click="goToPlatform">
            <div class="method-icon">🔧</div>
            <h3 class="method-name">平台创建工作流</h3>
            <p class="method-desc">跳转到师大智能体平台，创建完成后返回本系统</p>
            <el-button>前往平台</el-button>
          </div>
        </div>

        <div class="step-buttons">
          <el-button size="large" @click="prevStep">上一步</el-button>
          <el-button size="large" @click="resetGuide">重新开始</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 当前步骤
const currentStep = ref(0)

// 选择的分类
const selectedCategory = ref('')

// 选择的需求
const selectedNeed = ref('')

// 需求选项
const needOptions = [
  {
    value: 'preparation',
    label: '课前备课',
    description: '找资料、做课件、设计教学方案'
  },
  {
    value: 'teaching',
    label: '课堂教学',
    description: '互动、提问、演示、课堂管理'
  },
  {
    value: 'tutoring',
    label: '课后辅导',
    description: '作业批改、答疑、个性化辅导'
  },
  {
    value: 'interest',
    label: '学生兴趣激发',
    description: '趣味学习、游戏化教学、知识拓展'
  },
  {
    value: 'custom',
    label: '自定义需求',
    description: '其他教学场景或特殊需求'
  }
]

// 推荐工具（模拟数据）
const recommendedTools = computed(() => {
  console.log('当前分类:', selectedCategory.value)
  if (selectedCategory.value === '文科') {
    return [
      {
        id: 1,
        name: '古诗词趣味赏析',
        icon: '🏮',
        description: '输入诗词名，获得趣味化赏析、背景知识、知识卡片'
      },
      {
        id: 2,
        name: '作文灵感助手',
        icon: '✍️',
        description: '输入作文题目/主题，获得写作思路和素材建议'
      },
      {
        id: 3,
        name: '名词解释器',
        icon: '📖',
        description: '输入专业名词，获得通俗易懂的解释'
      }
    ]
  } else {
    return [
      {
        id: 4,
        name: '公式推导助手',
        icon: '🧮',
        description: '输入公式名，获得推导过程和几何直觉解释'
      },
      {
        id: 5,
        name: '实验模拟讲解',
        icon: '🔬',
        description: '输入实验名，获得步骤讲解和注意事项'
      },
      {
        id: 6,
        name: '逻辑思维训练',
        icon: '🧠',
        description: '提供逻辑题并引导思考过程'
      }
    ]
  }
})

// 选择分类
const selectCategory = (category) => {
  console.log('选择了分类:', category)
  selectedCategory.value = category
  console.log('selectedCategory.value:', selectedCategory.value)
}

// 选择需求
const selectNeed = (need) => {
  selectedNeed.value = need
}

// 获取需求标签
const getNeedLabel = (value) => {
  const need = needOptions.find(n => n.value === value)
  return need ? need.label : ''
}

// 下一步
const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 使用工具
const useTool = (tool) => {
  ElMessage.success(`即将进入：${tool.name}`)
  router.push(`/tool/${tool.id}`)
}

// 查看工具详情
const viewToolDetail = (tool) => {
  ElMessage.info(`查看${tool.name}的详情`)
}

// 开始AI创建
const startAICreate = () => {
  router.push('/student/chat')
}

// 前往平台
const goToPlatform = () => {
  ElMessage.info('即将跳转到师大智能体平台')
  // window.open('https://platform.example.com', '_blank')
}

// 重置引导
const resetGuide = () => {
  currentStep.value = 0
  selectedCategory.value = ''
  selectedNeed.value = ''
}
</script>

<style scoped>
.guide-container {
  max-width: 800px;
  margin: 0 auto;
}

.guide-steps {
  margin-bottom: 40px;
}

.guide-steps :deep(.el-step__title) {
  font-family: var(--font-sans);
  font-size: 14px;
}

.guide-steps :deep(.el-step__description) {
  font-family: var(--font-sans);
  font-size: 12px;
}

.step-content {
  background: white;
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: var(--shadow-md);
}

.step-card {
  text-align: center;
}

.step-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.step-desc {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
  margin-bottom: 32px;
}

/* 分类卡片 */
.category-cards {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-bottom: 32px;
}

.category-card {
  flex: 1;
  max-width: 280px;
  padding: 32px 24px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s;
}

.category-card:hover {
  border-color: var(--color-ink);
  box-shadow: var(--shadow-md);
}

.category-card.active {
  border-color: var(--color-ink);
  background: rgba(38, 37, 30, 0.05);
}

.category-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.category-name {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.category-subjects {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 需求列表 */
.need-list {
  text-align: left;
  max-width: 500px;
  margin: 0 auto 32px;
}

.need-item {
  padding: 16px 20px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.need-item:hover {
  border-color: var(--color-ink);
}

.need-item.active {
  border-color: var(--color-ink);
  background: rgba(38, 37, 30, 0.05);
}

.need-item :deep(.el-radio__label) {
  font-family: var(--font-sans);
  font-size: 15px;
  color: var(--color-ink);
}

.need-desc {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
  margin-top: 4px;
  margin-left: 24px;
}

/* 工具列表 */
.tool-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.tool-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: all 0.3s;
}

.tool-card:hover {
  border-color: var(--color-ink);
  box-shadow: var(--shadow-sm);
}

.tool-icon {
  font-size: 36px;
  margin-right: 16px;
}

.tool-info {
  flex: 1;
  text-align: left;
}

.tool-name {
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 4px;
}

.tool-desc {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.tool-actions {
  display: flex;
  gap: 8px;
}

/* 无工具提示 */
.no-tool-section {
  margin-top: 24px;
}

.no-tool-desc {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
  margin-bottom: 16px;
}

.no-tool-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

/* 创建方式 */
.create-methods {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-bottom: 32px;
}

.method-card {
  flex: 1;
  max-width: 280px;
  padding: 32px 24px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s;
}

.method-card:hover {
  border-color: var(--color-ink);
  box-shadow: var(--shadow-md);
}

.method-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.method-name {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.method-desc {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
  margin-bottom: 20px;
}

/* 步骤按钮 */
.step-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}
</style>
