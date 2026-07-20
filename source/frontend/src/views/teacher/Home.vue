<template>
  <div class="teacher-guidance vintage-theme">
    <header class="page-hero">
      <VintageOrnament name="swallow" />
      <VintageRibbonTitle label="NEED DISCOVERY" />
      <h1>把教学难题，变成清晰的工具路径</h1>
      <p>四步完成需求定位。推荐来自规则与真实工具库，不把简单匹配包装成 AI。</p>
      <VintageDivider />
    </header>

    <div class="guidance-map">
      <!-- 步骤一：选择学科领域 -->
      <section class="guidance-step" :class="`is-${stepStatus(1)}`" aria-labelledby="step-1-title">
        <div class="step-header">
          <VintageStepBadge :step="1" :status="stepStatus(1)" />
          <div class="step-title">
            <h2 id="step-1-title">选择学科<br>领域</h2>
            <p>先从文理科大类入手</p>
          </div>
        </div>
        <VintageTextBox variant="sage">
          <div class="choice-grid two-col">
            <button
              v-for="item in categories"
              :key="item.value"
              :aria-pressed="category === item.value"
              @click="chooseCategory(item.value)"
            >
              <strong>{{ item.label }}</strong>
              <small>{{ item.desc }}</small>
            </button>
          </div>
        </VintageTextBox>
      </section>

      <!-- 步骤二：选择具体学科 -->
      <section class="guidance-step" :class="`is-${stepStatus(2)}`" aria-labelledby="step-2-title">
        <div class="step-header">
          <VintageStepBadge :step="2" :status="stepStatus(2)" />
          <div class="step-title">
            <h2 id="step-2-title">选择具体<br>学科</h2>
            <p>细化到具体教学科目</p>
          </div>
        </div>
        <VintageTextBox variant="blue">
          <div class="choice-grid goals">
            <button
              v-for="name in (subjectsByCategory[category] || [])"
              :key="name"
              :disabled="!category"
              :aria-pressed="subject === name"
              @click="chooseSubject(name)"
            >
              <strong>{{ name }}</strong>
            </button>
          </div>
          <p v-if="!category" class="step-hint">请先完成第一步，再选择具体学科。</p>
        </VintageTextBox>
      </section>

      <!-- 步骤三：明确教学目标 -->
      <section class="guidance-step" :class="`is-${stepStatus(3)}`" aria-labelledby="step-3-title">
        <div class="step-header">
          <VintageStepBadge :step="3" :status="stepStatus(3)" />
          <div class="step-title">
            <h2 id="step-3-title">明确教学<br>目标</h2>
            <p>定位课堂真实需求</p>
          </div>
        </div>
        <VintageTextBox variant="parchment">
          <div class="choice-grid goals">
            <button
              v-for="item in goals"
              :key="item.value"
              :disabled="!subject"
              :aria-pressed="goal === item.value"
              @click="chooseGoal(item.value)"
            >
              <strong>{{ item.label }}</strong>
              <small>{{ item.desc }}</small>
            </button>
          </div>
          <p v-if="!subject" class="step-hint">请先选择学科，再明确教学目标。</p>
        </VintageTextBox>
      </section>

      <!-- 步骤四：获得工具推荐 -->
      <section class="guidance-step is-result" :class="`is-${stepStatus(4)}`" aria-labelledby="step-4-title">
        <div class="step-header">
          <VintageStepBadge :step="4" :status="stepStatus(4)" />
          <div class="step-title">
            <h2 id="step-4-title">获得工具<br>推荐</h2>
            <p>从真实工具库中匹配</p>
          </div>
        </div>

        <VintageFrame tone="gold" class="result-frame">
          <StatusState
            v-if="loading"
            type="loading"
            title="正在连接工具知识库"
            description="根据你的学科和目标筛选现有工具。"
          />
          <StatusState
            v-else-if="errorMessage"
            type="error"
            title="推荐暂时不可用"
            :description="errorMessage"
            @retry="loadRecommendations"
          />
          <StatusState
            v-else-if="goal && !tools.length"
            type="empty"
            title="暂未找到匹配工具"
            description="可以更换教学目标，或前往工具广场继续探索。"
          />
          <div v-else-if="tools.length" class="recommendations">
            <article v-for="tool in tools" :key="tool.id">
              <div class="tool-meta">
                <span>{{ tool.subject || category }}</span>
                <VintagePostmark text="MATCH" />
              </div>
              <h3>{{ tool.name }}</h3>
              <p>{{ tool.description || '基于当前教学目标匹配的课堂工具。' }}</p>
              <VintageButton variant="primary" as-child>
                <RouterLink :to="`/tool/${tool.id}`">立即体验</RouterLink>
              </VintageButton>
            </article>
          </div>
          <p v-else class="waiting-copy">完成前三步后，匹配结果将在这里展开。</p>
        </VintageFrame>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StatusState from '../../components/ui/StatusState.vue'
import VintageButton from '../../components/vintage/VintageButton.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageFrame from '../../components/vintage/VintageFrame.vue'
import VintageOrnament from '../../components/vintage/VintageOrnament.vue'
import VintagePostmark from '../../components/vintage/VintagePostmark.vue'
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import VintageStepBadge from '../../components/vintage/VintageStepBadge.vue'
import VintageTextBox from '../../components/vintage/VintageTextBox.vue'
import { getRecommendation } from '../../api/recommend'
import { useDemoMode } from '../../composables/useDemoMode'

const categories = [
  { value: '文科', label: '人文与表达', desc: '语文 / 英语 / 历史 / 政治 / 地理' },
  { value: '理科', label: '科学与推演', desc: '数学 / 物理 / 化学 / 生物 / 信息技术' }
]
const subjectsByCategory = {
  '文科': ['语文', '英语', '历史', '地理', '政治'],
  '理科': ['数学', '物理', '化学', '生物', '信息技术'],
}
const goals = [
  { value: '课前备课', label: '课前备课', desc: '组织资料与课堂结构' },
  { value: '课堂教学', label: '课堂互动', desc: '提问、演示与实时参与' },
  { value: '课后辅导', label: '课后辅导', desc: '答疑与个性化支持' },
  { value: '兴趣激发', label: '兴趣激发', desc: '让知识变得可探索' }
]
const category = ref(''), subject = ref(''), goal = ref(''), tools = ref([]), loading = ref(false), errorMessage = ref('')
const { enabled: demoEnabled, getDemoData } = useDemoMode()

function stepStatus(n) {
  if (n === 1) return category.value ? 'complete' : 'active'
  if (n === 2) return !category.value ? 'pending' : subject.value ? 'complete' : 'active'
  if (n === 3) return !subject.value ? 'pending' : goal.value ? 'complete' : 'active'
  return goal.value ? 'active' : 'pending'
}
function chooseCategory(value) { category.value = value; subject.value = ''; goal.value = ''; tools.value = []; errorMessage.value = '' }
function chooseSubject(value) { subject.value = value; goal.value = ''; tools.value = []; errorMessage.value = '' }
function chooseGoal(value) { goal.value = value; loadRecommendations() }
async function loadRecommendations() {
  if (!category.value || !goal.value) return
  loading.value = true
  errorMessage.value = ''
  try {
    if (demoEnabled.value) {
      tools.value = getDemoData('recommendations').tools
      return
    }
    const { data } = await getRecommendation({ step: 4, category: category.value, subject: subject.value || null, need_type: goal.value })
    tools.value = data.tools || []
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || '无法连接推荐服务，请确认后端已启动。'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.teacher-guidance.vintage-theme {
  max-width: 1120px;
  margin: auto;
  padding: clamp(28px, 4vw, 58px);
  background:
    radial-gradient(circle at 10% 5%, rgba(184, 161, 110, 0.08), transparent 30%),
    radial-gradient(circle at 90% 95%, rgba(138, 154, 140, 0.08), transparent 35%),
    #f5f1e8;
  color: #4a4333;
}

/* 旧纸张质感 */
.teacher-guidance.vintage-theme::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.04;
  background-image:
    radial-gradient(circle at 25% 25%, #6b5d3e 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, #6b5d3e 1px, transparent 1px);
  background-size: 80px 80px;
  z-index: 0;
}

.page-hero {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto 2.5rem;
  text-align: center;
}

.page-hero .vintage-ornament {
  margin-bottom: 0.75rem;
}

.page-hero h1 {
  margin: 1rem 0 0.75rem;
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 5vw, 4rem);
  font-weight: 500;
  line-height: 1.12;
  color: #3d3526;
}

.page-hero > p {
  max-width: 620px;
  margin: 0 auto 1.5rem;
  color: #6b5d3e;
  line-height: 1.75;
}

.page-hero .vintage-divider {
  margin-top: 1.5rem;
}

/* 步骤布局 */
.guidance-map {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.guidance-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.25rem;
  align-items: start;
  padding: 1.5rem;
  border-radius: 4px;
  background: rgba(250, 248, 242, 0.45);
  border: 1px solid rgba(196, 180, 154, 0.25);
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.05);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.guidance-step.is-pending {
  opacity: 0.65;
}

.guidance-step.is-active {
  opacity: 1;
  background: rgba(250, 248, 242, 0.7);
  border-color: rgba(184, 161, 110, 0.4);
}

.step-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  width: 90px;
}

.step-title {
  text-align: center;
}

.step-title h2 {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 600;
  color: #4a4333;
  line-height: 1.3;
}

.step-title p {
  font-size: 0.72rem;
  color: #8b6f47;
  letter-spacing: 0.04em;
  margin-top: 0.25rem;
}

/* 选项按钮 */
.choice-grid {
  display: grid;
  gap: 0.875rem;
}

.choice-grid.two-col {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.choice-grid.goals {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.choice-grid button {
  position: relative;
  min-height: 88px;
  padding: 1rem;
  border: 1px solid #c4b49a;
  border-radius: 2px;
  background:
    linear-gradient(135deg, rgba(250, 248, 242, 0.95), rgba(242, 239, 230, 0.9));
  color: #4a4333;
  text-align: left;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

/* 卷边效果 */
.choice-grid button::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 22px 22px;
  border-color: transparent transparent #e0d6be transparent;
  pointer-events: none;
  z-index: 2;
  transition: border-width 0.25s ease, border-color 0.25s ease;
}

.choice-grid button:hover::after {
  border-width: 0 0 30px 30px;
  border-color: transparent transparent #d4c9a8 transparent;
}

.choice-grid button::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px dashed rgba(139, 111, 71, 0.25);
  pointer-events: none;
}

.choice-grid button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(107, 93, 62, 0.12);
  border-color: #b8a16e;
}

.choice-grid button[aria-pressed="true"] {
  background: rgba(138, 154, 140, 0.15);
  border-color: #8a9a8c;
  box-shadow: inset 0 0 0 1px rgba(138, 154, 140, 0.25);
}

.choice-grid button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.choice-grid button strong,
.choice-grid button small {
  display: block;
}

.choice-grid button strong {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 600;
}

.choice-grid button small {
  margin-top: 0.4rem;
  color: #6b5d3e;
  font-size: 0.78rem;
  line-height: 1.5;
}

.step-hint {
  margin-top: 0.875rem;
  padding-top: 0.875rem;
  border-top: 1px dashed rgba(196, 180, 154, 0.5);
  color: #8b6f47;
  font-size: 0.82rem;
  font-style: italic;
}

/* 推荐结果区 */
.result-frame {
  min-height: 180px;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}

.recommendations article {
  position: relative;
  padding: 1.25rem;
  background: rgba(250, 248, 242, 0.8);
  border: 1px solid #d8d0b8;
  border-radius: 2px;
  color: #4a4333;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.recommendations article::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(139, 111, 71, 0.2);
  pointer-events: none;
}

.recommendations article:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(107, 93, 62, 0.1);
}

.tool-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.recommendations article > span,
.tool-meta > span {
  color: #8a9a8c;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.recommendations h3 {
  margin: 0.5rem 0;
  font-family: var(--font-display);
  font-size: 1.25rem;
  color: #3d3526;
}

.recommendations p,
.waiting-copy {
  color: #6b5d3e;
  line-height: 1.65;
  font-size: 0.88rem;
}

.recommendations .vintage-button {
  margin-top: 1rem;
}

.recommendations .vintage-button :deep(a) {
  color: inherit;
  text-decoration: none;
}

.waiting-copy {
  text-align: center;
  padding: 2rem;
  font-style: italic;
}

/* 响应式 */
@media (max-width: 900px) {
  .guidance-step {
    grid-template-columns: 1fr;
  }

  .step-header {
    flex-direction: row;
    width: auto;
    text-align: left;
  }

  .step-title {
    text-align: left;
  }

  .choice-grid.goals {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .recommendations {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .choice-grid.two-col,
  .choice-grid.goals,
  .recommendations {
    grid-template-columns: 1fr;
  }

  .step-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (prefers-reduced-motion: reduce) {
  .guidance-step,
  .choice-grid button,
  .recommendations article {
    transition: none;
  }
}
</style>
