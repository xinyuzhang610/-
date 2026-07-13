<template>
  <div class="guidance-container">
    <!-- 背景小气泡 -->
    <div class="bg-bubbles">
      <div
        v-for="i in 20"
        :key="i"
        class="bg-bubble"
        :style="{
          left: (i * 5) % 100 + '%',
          width: (i % 3) * 10 + 10 + 'px',
          height: (i % 3) * 10 + 10 + 'px',
          animationDuration: (i % 5) * 3 + 10 + 's',
          animationDelay: (i % 4) * 2 + 's'
        }"
      />
    </div>

    <!-- 主要内容 -->
    <div class="guidance-card">
      <!-- 进度指示器 -->
      <div class="progress-bar">
        <div class="progress-dots">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="progress-dot"
            :class="{
              active: currentStep === index,
              completed: currentStep > index
            }"
          />
        </div>
      </div>

      <!-- 标题区域 -->
      <div class="guidance-title">
        <h1 class="title-text">{{ currentTitle }}</h1>
        <p class="title-desc">{{ currentDesc }}</p>
      </div>

      <!-- 气泡区域 -->
      <div class="bubble-container">
        <transition-group name="bubble" tag="div" class="bubble-grid">
          <div
            v-for="bubble in currentBubbles"
            :key="bubble.id"
            class="bubble"
            :class="[bubble.colorClass, { popping: bubble.isPopping }]"
            @click="popBubble(bubble)"
          >
            <span class="bubble-icon">{{ bubble.icon }}</span>
            <span class="bubble-label">{{ bubble.label }}</span>
          </div>
        </transition-group>
      </div>

      <!-- 推荐工具区域（第5层） -->
      <div v-if="currentStep === 4" class="recommend-section">
        <div class="recommend-list">
          <div
            v-for="tool in recommendedTools"
            :key="tool.id"
            class="recommend-card"
            @click="useTool(tool)"
          >
            <div class="recommend-icon">{{ tool.icon }}</div>
            <div class="recommend-info">
              <h3 class="recommend-name">{{ tool.name }}</h3>
              <p class="recommend-desc">{{ tool.desc }}</p>
            </div>
            <el-button type="primary" size="small">开始体验</el-button>
          </div>
        </div>
        <div class="recommend-footer">
          <el-button @click="goToPlaza">🔍 去工具广场看看</el-button>
        </div>
      </div>

      <!-- 底部提示 -->
      <div class="guidance-footer">
        <p class="footer-tip">{{ footerTip }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 5层步骤配置
const steps = [
  { label: '学习困惑' },
  { label: '具体问题' },
  { label: '困难原因' },
  { label: '确认需求' },
  { label: '推荐工具' }
]

// 引导状态
const currentStep = ref(0)
const selectedDifficulty = ref('')
const selectedSubject = ref('')
const selectedReason = ref('')
const isAnimating = ref(false)

// 当前标题
const currentTitle = computed(() => {
  const titles = [
    '🎓 你好呀，同学！',
    '📚 哪个科目让你头疼呢？',
    '🤔 为什么会觉得难呢？',
    '✨ 确认一下你的需求',
    '🎁 为你推荐这些工具！'
  ]
  return titles[currentStep.value]
})

// 当前描述
const currentDesc = computed(() => {
  const descs = [
    '学习上遇到什么困难了？告诉我，我来帮你～',
    '告诉我具体是哪个科目的问题',
    '了解原因才能更好地帮助你',
    '看看我理解得对不对',
    '这些工具可以帮到你，点击开始体验吧～'
  ]
  return descs[currentStep.value]
})

// 底部提示
const footerTip = computed(() => {
  const tips = [
    '点击一个气泡选择你遇到的困难',
    '点击选择具体的科目',
    '点击选择困难的原因',
    '点击确认或返回修改',
    '点击工具开始体验'
  ]
  return tips[currentStep.value]
})

// 第1层：学习困惑（10+个泡泡，3个核心）
const difficultyBubbles = [
  { id: 'd1', icon: '📖', label: '读不懂题', value: '读不懂题', colorClass: 'bubble-blue', isPopping: false },
  { id: 'd2', icon: '❌', label: '不会做题', value: '不会做题', colorClass: 'bubble-purple', isPopping: false },
  { id: 'd3', icon: '😴', label: '没兴趣', value: '没兴趣', colorClass: 'bubble-pink', isPopping: false },
  { id: 'd4', icon: '📝', label: '记不住', value: '记不住', colorClass: 'bubble-green', isPopping: false },
  { id: 'd5', icon: '🤯', label: '太难了', value: '太难了', colorClass: 'bubble-orange', isPopping: false },
  { id: 'd6', icon: '⏰', label: '时间不够', value: '时间不够', colorClass: 'bubble-yellow', isPopping: false },
  { id: 'd7', icon: '😤', label: '容易粗心', value: '容易粗心', colorClass: 'bubble-blue', isPopping: false },
  { id: 'd8', icon: '❓', label: '不会总结', value: '不会总结', colorClass: 'bubble-purple', isPopping: false },
  { id: 'd9', icon: '📚', label: '基础差', value: '基础差', colorClass: 'bubble-green', isPopping: false },
  { id: 'd10', icon: '😰', label: '考试紧张', value: '考试紧张', colorClass: 'bubble-pink', isPopping: false },
  { id: 'd11', icon: '📱', label: '容易分心', value: '容易分心', colorClass: 'bubble-orange', isPopping: false },
  { id: 'd12', icon: '🤷', label: '不知道学什么', value: '不知道学什么', colorClass: 'bubble-yellow', isPopping: false }
]

// 第2层：具体科目
const subjectBubbles = [
  { id: 's1', icon: '📖', label: '语文', value: '语文', colorClass: 'bubble-blue', isPopping: false },
  { id: 's2', icon: '🔢', label: '数学', value: '数学', colorClass: 'bubble-purple', isPopping: false },
  { id: 's3', icon: '🔤', label: '英语', value: '英语', colorClass: 'bubble-pink', isPopping: false },
  { id: 's4', icon: '⚡', label: '物理', value: '物理', colorClass: 'bubble-green', isPopping: false },
  { id: 's5', icon: '🧪', label: '化学', value: '化学', colorClass: 'bubble-orange', isPopping: false },
  { id: 's6', icon: '🌿', label: '生物', value: '生物', colorClass: 'bubble-yellow', isPopping: false },
  { id: 's7', icon: '🌍', label: '历史', value: '历史', colorClass: 'bubble-blue', isPopping: false },
  { id: 's8', icon: '🗺️', label: '地理', value: '地理', colorClass: 'bubble-purple', isPopping: false },
  { id: 's9', icon: '⚖️', label: '政治', value: '政治', colorClass: 'bubble-green', isPopping: false }
]

// 第3层：困难原因
const reasonBubbles = ref([])

// 根据困惑和科目生成原因选项
const getReasonBubbles = () => {
  const difficulty = selectedDifficulty.value
  const subject = selectedSubject.value

  // 读不懂题的原因
  if (difficulty === '读不懂题') {
    return [
      { id: 'r1', icon: '📝', label: '词汇量不够', value: '词汇量不够', colorClass: 'bubble-blue', isPopping: false },
      { id: 'r2', icon: '📖', label: '题目太长', value: '题目太长', colorClass: 'bubble-purple', isPopping: false },
      { id: 'r3', icon: '🤔', label: '不理解题意', value: '不理解题意', colorClass: 'bubble-pink', isPopping: false },
      { id: 'r4', icon: '📊', label: '图表看不懂', value: '图表看不懂', colorClass: 'bubble-green', isPopping: false }
    ]
  }

  // 不会做题的原因
  if (difficulty === '不会做题') {
    return [
      { id: 'r1', icon: '📚', label: '知识点不熟', value: '知识点不熟', colorClass: 'bubble-blue', isPopping: false },
      { id: 'r2', icon: '🧩', label: '不会举一反三', value: '不会举一反三', colorClass: 'bubble-purple', isPopping: false },
      { id: 'r3', icon: '📋', label: '缺少方法', value: '缺少方法', colorClass: 'bubble-pink', isPopping: false },
      { id: 'r4', icon: '⏰', label: '练习不够', value: '练习不够', colorClass: 'bubble-green', isPopping: false }
    ]
  }

  // 没兴趣的原因
  if (difficulty === '没兴趣') {
    return [
      { id: 'r1', icon: '😴', label: '内容太枯燥', value: '内容太枯燥', colorClass: 'bubble-blue', isPopping: false },
      { id: 'r2', icon: '🎮', label: '想要趣味学习', value: '想要趣味学习', colorClass: 'bubble-purple', isPopping: false },
      { id: 'r3', icon: '🎯', label: '看不到意义', value: '看不到意义', colorClass: 'bubble-pink', isPopping: false },
      { id: 'r4', icon: '👨‍🏫', label: '教学方式不适应', value: '教学方式不适应', colorClass: 'bubble-green', isPopping: false }
    ]
  }

  // 默认原因
  return [
    { id: 'r1', icon: '📚', label: '基础不扎实', value: '基础不扎实', colorClass: 'bubble-blue', isPopping: false },
    { id: 'r2', icon: '⏰', label: '时间管理差', value: '时间管理差', colorClass: 'bubble-purple', isPopping: false },
    { id: 'r3', icon: '🎯', label: '学习方法不对', value: '学习方法不对', colorClass: 'bubble-pink', isPopping: false },
    { id: 'r4', icon: '💪', label: '需要更多练习', value: '需要更多练习', colorClass: 'bubble-green', isPopping: false }
  ]
}

// 第4层：确认需求
const confirmBubbles = [
  { id: 'c1', icon: '✅', label: '是的，就是这样', value: 'confirm', colorClass: 'bubble-green', isPopping: false },
  { id: 'c2', icon: '🔄', label: '重新选择', value: 'restart', colorClass: 'bubble-orange', isPopping: false }
]

// 当前气泡列表
const currentBubbles = computed(() => {
  if (currentStep.value === 0) return difficultyBubbles
  if (currentStep.value === 1) return subjectBubbles
  if (currentStep.value === 2) return reasonBubbles.value
  if (currentStep.value === 3) return confirmBubbles
  return []
})

// 推荐工具
const recommendedTools = ref([])

// 根据选择获取推荐工具
const getRecommendedTools = () => {
  const difficulty = selectedDifficulty.value
  const subject = selectedSubject.value
  const reason = selectedReason.value

  // 读不懂题 + 语文
  if (difficulty === '读不懂题' && subject === '语文') {
    return [
      { id: 1, icon: '📖', name: '阅读理解辅助', desc: '帮你分析文章结构，理解题意' },
      { id: 2, icon: '🏮', name: '古诗词趣味赏析', desc: '用有趣的方式理解古诗词' }
    ]
  }

  // 不会做题 + 数学
  if (difficulty === '不会做题' && subject === '数学') {
    return [
      { id: 3, icon: '🧮', name: '公式推导助手', desc: '一步步教你推导公式' },
      { id: 4, icon: '🧠', name: '逻辑思维训练', desc: '提升解题思路' }
    ]
  }

  // 没兴趣
  if (difficulty === '没兴趣') {
    return [
      { id: 5, icon: '🎮', name: '趣味学习工具', desc: '让学习变得有趣' },
      { id: 6, icon: '🌸', name: '诗词飞花令', desc: '边玩边学古诗词' }
    ]
  }

  // 默认推荐
  return [
    { id: 1, icon: '🏮', name: '古诗词趣味赏析', desc: '用有趣的方式理解古诗词' },
    { id: 3, icon: '🧮', name: '公式推导助手', desc: '一步步教你推导公式' },
    { id: 5, icon: '✍️', name: '作文灵感助手', desc: '帮你打开写作思路' }
  ]
}

// 戳泡泡
const popBubble = async (bubble) => {
  if (isAnimating.value) return

  isAnimating.value = true
  bubble.isPopping = true

  await new Promise(resolve => setTimeout(resolve, 400))

  // 第1层：选择困惑
  if (currentStep.value === 0) {
    selectedDifficulty.value = bubble.value
    currentStep.value = 1
  }
  // 第2层：选择科目
  else if (currentStep.value === 1) {
    selectedSubject.value = bubble.value
    reasonBubbles.value = getReasonBubbles()
    currentStep.value = 2
  }
  // 第3层：选择原因
  else if (currentStep.value === 2) {
    selectedReason.value = bubble.value
    currentStep.value = 3
  }
  // 第4层：确认需求
  else if (currentStep.value === 3) {
    if (bubble.value === 'confirm') {
      recommendedTools.value = getRecommendedTools()
      currentStep.value = 4
    } else {
      // 重新开始
      currentStep.value = 0
      selectedDifficulty.value = ''
      selectedSubject.value = ''
      selectedReason.value = ''
    }
  }

  isAnimating.value = false
}

// 使用工具
const useTool = (tool) => {
  router.push(`/tool/${tool.id}`)
}

// 去工具广场
const goToPlaza = () => {
  router.push('/student/plaza')
}
</script>

<style scoped>
.guidance-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e8f4f8 0%, #f0e6f6 50%, #fce4ec 100%);
  padding: 32px 16px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 背景小气泡 */
.bg-bubbles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.bg-bubble {
  position: absolute;
  bottom: -50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  animation: bgFloat linear infinite;
}

@keyframes bgFloat {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

/* 主要内容卡片 */
.guidance-card {
  max-width: 800px;
  width: 100%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 48px;
  box-shadow: var(--shadow-lg);
  position: relative;
  z-index: 1;
}

/* 进度条 */
.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 48px;
}

.progress-dots {
  display: flex;
  gap: 8px;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-border);
  transition: all var(--duration-normal) ease;
}

.progress-dot.active {
  background: var(--color-ink);
  transform: scale(1.2);
}

.progress-dot.completed {
  background: var(--color-success);
}

/* 标题区域 */
.guidance-title {
  text-align: center;
  margin-bottom: 32px;
}

.title-text {
  font-family: var(--font-body);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.title-desc {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-ink-soft);
}

/* 气泡容器 */
.bubble-container {
  margin-bottom: 32px;
}

.bubble-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
  padding: 16px 0;
}

/* 气泡样式 */
.bubble {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform var(--duration-normal) var(--ease-bounce);
  animation: float 3s ease-in-out infinite;
}

.bubble:nth-child(1) { animation-delay: 0s; }
.bubble:nth-child(2) { animation-delay: 0.5s; }
.bubble:nth-child(3) { animation-delay: 1s; }
.bubble:nth-child(4) { animation-delay: 1.5s; }
.bubble:nth-child(5) { animation-delay: 2s; }
.bubble:nth-child(6) { animation-delay: 2.5s; }

/* 气泡光泽效果 */
.bubble::before {
  content: '';
  position: absolute;
  top: 10%;
  left: 15%;
  width: 30%;
  height: 30%;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
  border-radius: 50%;
}

/* 气泡阴影 */
.bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 10px;
  background: radial-gradient(ellipse, rgba(0,0,0,0.1) 0%, transparent 70%);
}

.bubble:hover {
  transform: scale(1.1);
}

.bubble:active {
  transform: scale(0.95);
}

/* 气泡颜色 */
.bubble-blue { background: linear-gradient(135deg, #81d4fa 0%, #4fc3f7 100%); }
.bubble-purple { background: linear-gradient(135deg, #ce93d8 0%, #ba68c8 100%); }
.bubble-pink { background: linear-gradient(135deg, #f48fb1 0%, #ec407a 100%); }
.bubble-green { background: linear-gradient(135deg, #80cbc4 0%, #4db6ac 100%); }
.bubble-orange { background: linear-gradient(135deg, #ffcc80 0%, #ffa726 100%); }
.bubble-yellow { background: linear-gradient(135deg, #fff59d 0%, #ffee58 100%); }

/* 气泡内容 */
.bubble-icon {
  font-size: 36px;
  margin-bottom: 4px;
}

.bubble-label {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
  text-align: center;
}

/* 气泡漂浮动画 */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* 气泡戳破动画 */
.bubble.popping {
  animation: pop 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) forwards;
}

@keyframes pop {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(0); opacity: 0; }
}

/* 推荐工具区域 */
.recommend-section {
  margin-top: 24px;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.recommend-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  transition: all var(--duration-normal) ease;
  box-shadow: var(--shadow-sm);
}

.recommend-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.recommend-icon {
  font-size: 40px;
  flex-shrink: 0;
}

.recommend-info {
  flex: 1;
}

.recommend-name {
  font-family: var(--font-title);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 4px;
}

.recommend-desc {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.recommend-footer {
  text-align: center;
}

/* 底部提示 */
.guidance-footer {
  text-align: center;
  margin-top: 24px;
}

.footer-tip {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 响应式 */
@media (max-width: 768px) {
  .guidance-card {
    padding: 24px;
  }

  .title-text {
    font-size: 20px;
  }

  .bubble {
    width: 90px;
    height: 90px;
  }

  .bubble-icon {
    font-size: 28px;
  }

  .bubble-label {
    font-size: 12px;
  }

  .bubble-grid {
    gap: 16px;
  }
}
</style>
