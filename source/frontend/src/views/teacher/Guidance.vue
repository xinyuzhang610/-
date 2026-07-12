<template>
  <div class="guidance-container">
    <el-card class="guidance-card">
      <h2>需求引导</h2>
      <p class="subtitle">让我帮您找到最合适的AI工具</p>

      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择方向" />
        <el-step title="明确需求" />
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
          <el-radio-group v-model="selectedNeed" @change="handleNeedSelect">
            <el-radio
              v-for="option in guidanceData.options"
              :key="option.value"
              :value="option.value"
              class="need-option"
            >
              <span class="need-label">{{ option.label }}</span>
              <span class="need-desc">{{ option.desc }}</span>
            </el-radio>
          </el-radio-group>
        </div>
      </div>

      <div v-if="currentStep === 2" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="tools-grid">
          <el-card
            v-for="tool in guidanceData.tools"
            :key="tool.id"
            class="tool-card"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-subject">{{ tool.subject }}</div>
            <el-button type="primary" size="small" @click="useTool(tool)">
              立即体验
            </el-button>
          </el-card>
        </div>
        <div class="action-buttons">
          <el-button @click="resetGuidance">重新选择</el-button>
        </div>
      </div>

      <div class="nav-buttons" v-if="currentStep < 2">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button type="primary" @click="nextStep" :disabled="!canProceed">
          下一步
        </el-button>
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
const selectedNeed = ref('')
const guidanceData = ref({ message: '', options: [] })
const canProceed = ref(false)

onMounted(async () => {
  await loadStep1()
})

const loadStep1 = async () => {
  try {
    const { data } = await getRecommendation({ step: 1 })
    guidanceData.value = data
  } catch (error) {
    ElMessage.error('加载失败')
  }
}

const selectCategory = (value) => {
  selectedCategory.value = value
  canProceed.value = true
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    try {
      const { data } = await getRecommendation({ step: 2, category: selectedCategory.value })
      guidanceData.value = data
      currentStep.value++
      canProceed.value = false
    } catch (error) {
      ElMessage.error('加载失败')
    }
  } else if (currentStep.value === 1) {
    try {
      const { data } = await getRecommendation({
        step: 3,
        category: selectedCategory.value,
        need_type: selectedNeed.value
      })
      guidanceData.value = data
      currentStep.value++
    } catch (error) {
      ElMessage.error('加载失败')
    }
  }
}

const prevStep = () => {
  currentStep.value--
  if (currentStep.value === 0) {
    loadStep1()
    canProceed.value = true
  }
}

const handleNeedSelect = () => {
  canProceed.value = true
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.id}`)
}

const resetGuidance = () => {
  currentStep.value = 0
  selectedCategory.value = ''
  selectedNeed.value = ''
  loadStep1()
  canProceed.value = false
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
.need-option {
  display: block;
  margin: 15px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
}
.need-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.need-desc {
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
