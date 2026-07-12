<template>
  <div class="guidance-container">
    <el-card class="guidance-card">
      <h2>探索你的学习需求</h2>
      <p class="subtitle">让我帮你找到最适合的学习工具</p>

      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择学科" />
        <el-step title="明确目标" />
        <el-step title="获取推荐" />
      </el-steps>

      <div v-if="currentStep === 0" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-grid">
          <el-card
            v-for="option in guidanceData.options"
            :key="option.value"
            class="option-card"
            :class="{ active: selectedCategory === option.value }"
            @click="selectCategory(option.value)"
          >
            <div class="option-icon">{{ option.value === '文科' ? '📚' : '🔬' }}</div>
            <div class="option-label">{{ option.label }}</div>
            <div class="option-desc">{{ option.desc }}</div>
          </el-card>
        </div>
      </div>

      <div v-if="currentStep === 1" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-list">
          <el-radio-group v-model="selectedGoal" @change="handleGoalSelect">
            <el-radio
              v-for="option in guidanceData.options"
              :key="option.value"
              :value="option.value"
              class="goal-option"
            >
              <span class="goal-label">{{ option.label }}</span>
              <span class="goal-desc">{{ option.desc }}</span>
            </el-radio>
          </el-radio-group>
        </div>
      </div>

      <div v-if="currentStep === 2" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="tools-grid">
          <el-card v-for="tool in guidanceData.tools" :key="tool.id" class="tool-card">
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-subject">{{ tool.subject }}</div>
            <el-button type="primary" size="small" @click="useTool(tool)">立即体验</el-button>
          </el-card>
        </div>
        <div class="action-buttons">
          <el-button @click="resetGuidance">重新选择</el-button>
          <el-button type="primary" @click="goToPlaza">去工具广场看看</el-button>
        </div>
      </div>

      <div class="nav-buttons" v-if="currentStep < 2">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button type="primary" @click="nextStep" :disabled="!canProceed">下一步</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendation } from '@/api/recommend'
import { ElMessage } from 'element-plus'

const router = useRouter()
const currentStep = ref(0)
const selectedCategory = ref('')
const selectedGoal = ref('')
const guidanceData = ref({ message: '', options: [] })
const canProceed = ref(false)

const STUDENT_GUIDANCE = {
  1: {
    message: '你想学习哪个方向？',
    options: [
      { value: '文科', label: '文科', desc: '语文/英语/历史/政治/地理' },
      { value: '理科', label: '理科', desc: '数学/物理/化学/生物/信息技术' }
    ]
  },
  2: {
    '文科': {
      message: '你最想做什么？',
      options: [
        { value: '学习新知识', label: '学习新知识', desc: '理解概念、背诵诗词、学习语法' },
        { value: '完成作业', label: '完成作业', desc: '写作文、做阅读、翻译句子' },
        { value: '准备考试', label: '准备考试', desc: '复习重点、练习题目、查漏补缺' },
        { value: '探索兴趣', label: '探索兴趣', desc: '玩飞花令、趣味学习、拓展视野' }
      ]
    },
    '理科': {
      message: '你最想做什么？',
      options: [
        { value: '学习新知识', label: '学习新知识', desc: '理解公式、学习概念、掌握方法' },
        { value: '完成作业', label: '完成作业', desc: '解题思路、分析错题、推导公式' },
        { value: '准备考试', label: '准备考试', desc: '复习重点、练习题目、总结技巧' },
        { value: '探索兴趣', label: '探索兴趣', desc: '逻辑训练、实验模拟、数据分析' }
      ]
    }
  }
}

onMounted(() => {
  guidanceData.value = STUDENT_GUIDANCE[1]
})

const selectCategory = (value) => {
  selectedCategory.value = value
  canProceed.value = true
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    guidanceData.value = STUDENT_GUIDANCE[2][selectedCategory.value]
    currentStep.value++
    canProceed.value = false
  } else if (currentStep.value === 1) {
    try {
      const { data } = await getRecommendation({
        step: 3,
        category: selectedCategory.value,
        need_type: selectedGoal.value
      })
      guidanceData.value = data
      currentStep.value++
    } catch (error) {
      ElMessage.error('获取推荐失败')
    }
  }
}

const prevStep = () => {
  currentStep.value--
  if (currentStep.value === 0) {
    guidanceData.value = STUDENT_GUIDANCE[1]
    canProceed.value = true
  }
}

const handleGoalSelect = () => {
  canProceed.value = true
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.id}`)
}

const resetGuidance = () => {
  currentStep.value = 0
  selectedCategory.value = ''
  selectedGoal.value = ''
  guidanceData.value = STUDENT_GUIDANCE[1]
  canProceed.value = false
}

const goToPlaza = () => {
  router.push('/student/plaza')
}
</script>

<style scoped>
.guidance-container {
  max-width: 800px;
  margin: 0 auto;
}
.guidance-card {
  padding: 20px;
}
.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 30px;
}
.step-content {
  margin-top: 30px;
}
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}
.option-card {
  cursor: pointer;
  text-align: center;
  transition: all 0.3s;
}
.option-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.option-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}
.option-icon {
  font-size: 48px;
  margin-bottom: 10px;
}
.option-label {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}
.option-desc {
  color: #666;
  font-size: 14px;
}
.goal-option {
  display: block;
  margin: 15px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
}
.goal-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.goal-desc {
  color: #666;
  font-size: 14px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.tool-card {
  text-align: center;
}
.tool-icon {
  font-size: 36px;
  margin-bottom: 10px;
}
.tool-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}
.tool-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}
.tool-subject {
  color: #999;
  font-size: 12px;
  margin-bottom: 15px;
}
.action-buttons {
  text-align: center;
  margin-top: 30px;
}
.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}
</style>
