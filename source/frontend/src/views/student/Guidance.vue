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
        <div class="progress-steps">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="progress-step"
            :class="{ active: currentStep >= index, current: currentStep === index }"
          >
            <div class="step-dot">{{ index + 1 }}</div>
            <span class="step-label">{{ step.label }}</span>
          </div>
        </div>
        <div class="progress-line">
          <div class="progress-fill" :style="{ width: (currentStep / (steps.length - 1)) * 100 + '%' }"></div>
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
            :class="[bubble.colorClass, { popping: bubble.isPopping, entering: bubble.isEntering }]"
            @click="popBubble(bubble)"
            @mouseenter="hoverBubble(bubble)"
            @mouseleave="leaveBubble(bubble)"
          >
            <span class="bubble-icon">{{ bubble.icon }}</span>
            <span class="bubble-label">{{ bubble.label }}</span>
          </div>
        </transition-group>
      </div>

      <!-- 底部提示 -->
      <div class="guidance-footer">
        <p class="footer-tip">{{ footerTip }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 步骤配置
const steps = [
  { label: '文理分科' },
  { label: '学习目标' },
  { label: '推荐工具' }
]

// 引导状态
const currentStep = ref(0)
const selectedSubject = ref('')
const selectedGoal = ref('')
const isAnimating = ref(false)

// 当前标题
const currentTitle = computed(() => {
  if (currentStep.value === 0) return '🎓 你好呀，同学！'
  if (currentStep.value === 1) return `🎉 太棒了！你选择了${selectedSubject.value}～`
  return '🎁 为你推荐这些超棒的工具！'
})

// 当前描述
const currentDesc = computed(() => {
  if (currentStep.value === 0) return '让我帮你找到最棒的学习工具吧～'
  if (currentStep.value === 1) return '告诉我，你最想做什么呢？'
  return '点击气泡开始体验吧～'
})

// 底部提示
const footerTip = computed(() => {
  if (currentStep.value === 0) return '点击一个气泡选择你的学科方向'
  if (currentStep.value === 1) return '点击一个气泡选择你的学习目标'
  return '点击工具气泡开始体验，或去工具广场看看'
})

// 气泡数据
const subjectBubbles = [
  { id: 's1', icon: '📚', label: '文科', value: '文科', colorClass: 'bubble-blue', isPopping: false, isEntering: true },
  { id: 's2', icon: '🔬', label: '理科', value: '理科', colorClass: 'bubble-purple', isPopping: false, isEntering: true },
  { id: 's3', icon: '🎨', label: '艺术', value: '艺术', colorClass: 'bubble-pink', isPopping: false, isEntering: true },
  { id: 's4', icon: '🌟', label: '全部', value: '全部', colorClass: 'bubble-yellow', isPopping: false, isEntering: true }
]

const goalBubbles = [
  { id: 'g1', icon: '📖', label: '学新知识', value: '学新知识', colorClass: 'bubble-blue', isPopping: false, isEntering: true },
  { id: 'g2', icon: '✍️', label: '写作业', value: '写作业', colorClass: 'bubble-green', isPopping: false, isEntering: true },
  { id: 'g3', icon: '📝', label: '考试复习', value: '考试复习', colorClass: 'bubble-orange', isPopping: false, isEntering: true },
  { id: 'g4', icon: '🎮', label: '趣味学习', value: '趣味学习', colorClass: 'bubble-pink', isPopping: false, isEntering: true }
]

// 推荐工具
const getRecommendedTools = () => {
  const subject = selectedSubject.value
  const goal = selectedGoal.value

  // 文科 + 学新知识
  if (subject === '文科' && goal === '学新知识') {
    return [
      { id: 't1', icon: '🏮', label: '古诗词趣味赏析', value: '/tool/1', colorClass: 'bubble-blue', isPopping: false, isEntering: true },
      { id: 't2', icon: '📖', label: '名词解释器', value: '/tool/3', colorClass: 'bubble-purple', isPopping: false, isEntering: true }
    ]
  }

  // 文科 + 写作业
  if (subject === '文科' && goal === '写作业') {
    return [
      { id: 't1', icon: '✍️', label: '作文灵感助手', value: '/tool/2', colorClass: 'bubble-pink', isPopping: false, isEntering: true },
      { id: 't2', icon: '📖', label: '阅读理解辅助', value: '/tool/4', colorClass: 'bubble-green', isPopping: false, isEntering: true }
    ]
  }

  // 理科 + 学新知识
  if (subject === '理科' && goal === '学新知识') {
    return [
      { id: 't1', icon: '🧮', label: '公式推导助手', value: '/tool/7', colorClass: 'bubble-purple', isPopping: false, isEntering: true },
      { id: 't2', icon: '🔬', label: '实验模拟讲解', value: '/tool/8', colorClass: 'bubble-blue', isPopping: false, isEntering: true }
    ]
  }

  // 理科 + 考试复习
  if (subject === '理科' && goal === '考试复习') {
    return [
      { id: 't1', icon: '🧠', label: '逻辑思维训练', value: '/tool/9', colorClass: 'bubble-orange', isPopping: false, isEntering: true },
      { id: 't2', icon: '❌', label: '错题分析器', value: '/tool/10', colorClass: 'bubble-pink', isPopping: false, isEntering: true }
    ]
  }

  // 默认推荐
  return [
    { id: 't1', icon: '🏮', label: '古诗词趣味赏析', value: '/tool/1', colorClass: 'bubble-blue', isPopping: false, isEntering: true },
    { id: 't2', icon: '🧮', label: '公式推导助手', value: '/tool/7', colorClass: 'bubble-purple', isPopping: false, isEntering: true },
    { id: 't3', icon: '✍️', label: '作文灵感助手', value: '/tool/2', colorClass: 'bubble-pink', isPopping: false, isEntering: true }
  ]
}

// 当前气泡列表
const currentBubbles = computed(() => {
  if (currentStep.value === 0) return subjectBubbles
  if (currentStep.value === 1) return goalBubbles
  return getRecommendedTools()
})

// 戳泡泡
const popBubble = async (bubble) => {
  if (isAnimating.value) return

  // 如果是工具气泡，直接跳转
  if (currentStep.value === 2) {
    router.push(bubble.value)
    return
  }

  isAnimating.value = true

  // 播放戳破动画
  bubble.isPopping = true

  // 等待动画完成
  await new Promise(resolve => setTimeout(resolve, 400))

  // 更新选择
  if (currentStep.value === 0) {
    selectedSubject.value = bubble.value
  } else if (currentStep.value === 1) {
    selectedGoal.value = bubble.value
  }

  // 进入下一步
  currentStep.value++
  isAnimating.value = false

  // 重置新气泡的进入动画
  setTimeout(() => {
    currentBubbles.value.forEach(b => {
      b.isPopping = false
      b.isEntering = true
    })
  }, 100)
}

// 气泡悬停效果
const hoverBubble = (bubble) => {
  if (!bubble.isPopping) {
    bubble.isHovered = true
  }
}

const leaveBubble = (bubble) => {
  bubble.isHovered = false
}

// 页面加载时播放进入动画
onMounted(() => {
  setTimeout(() => {
    currentBubbles.value.forEach((bubble, index) => {
      setTimeout(() => {
        bubble.isEntering = false
      }, index * 100)
    })
  }, 300)
})
</script>

<style scoped>
.guidance-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e8f4f8 0%, #f0e6f6 50%, #fce4ec 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  position: relative;
  overflow: hidden;
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  max-width: 600px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
}

/* 进度指示器 */
.progress-bar {
  margin-bottom: var(--space-2xl);
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-sm);
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
}

.step-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-chip-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-ui);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink-soft);
  transition: all var(--duration-normal) var(--ease-out);
}

.progress-step.active .step-dot {
  background: var(--color-primary);
  color: white;
}

.progress-step.current .step-dot {
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(38, 37, 30, 0.1);
}

.step-label {
  font-family: var(--font-ui);
  font-size: 12px;
  color: var(--color-ink-soft);
}

.progress-step.active .step-label {
  color: var(--color-ink);
}

.progress-line {
  height: 4px;
  background: var(--color-chip-bg);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 2px;
  transition: width var(--duration-normal) var(--ease-out);
}

/* 标题区域 */
.guidance-title {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.title-text {
  font-family: var(--font-cute);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-sm);
}

.title-desc {
  font-family: var(--font-cute);
  font-size: 16px;
  color: var(--color-ink-soft);
}

/* 气泡容器 */
.bubble-container {
  margin-bottom: var(--space-2xl);
}

.bubble-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-lg);
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
  font-family: var(--font-cute);
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* 气泡悬停效果 */
.bubble:hover {
  transform: scale(1.1);
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
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: scale(0);
    opacity: 0;
  }
}

/* 气泡进入动画 */
.bubble.entering {
  animation: bubbleEnter 0.6s var(--ease-bounce) forwards;
}

@keyframes bubbleEnter {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

/* 气泡过渡动画 */
.bubble-enter-active {
  transition: all var(--duration-normal) var(--ease-out);
}

.bubble-leave-active {
  transition: all var(--duration-fast) ease-in;
}

.bubble-enter-from {
  opacity: 0;
  transform: scale(0);
}

.bubble-leave-to {
  opacity: 0;
  transform: scale(0);
}

/* 底部提示 */
.guidance-footer {
  text-align: center;
}

.footer-tip {
  font-family: var(--font-cute);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 响应式 */
@media (max-width: 768px) {
  .guidance-container {
    padding: var(--space-md);
  }

  .guidance-card {
    padding: var(--space-lg);
  }

  .title-text {
    font-size: 22px;
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
    gap: var(--space-md);
  }
}
</style>
