<script setup>
import { computed, onMounted, ref } from 'vue'
import { getMyUsage } from '../../api/usage'
import StatusState from '../../components/ui/StatusState.vue'
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageOrnament from '../../components/vintage/VintageOrnament.vue'
import { useDemoMode } from '../../composables/useDemoMode'

const logs = ref([]), loading = ref(true), error = ref('')
const { enabled: demoEnabled, getDemoData } = useDemoMode()
const uniqueTools = computed(() => new Set(logs.value.map(item => item.tool_id)).size)
const activeDays = computed(() => new Set(logs.value.map(item => item.created_at?.slice(0, 10)).filter(Boolean)).size)
const formatTime = value => value ? new Intl.DateTimeFormat('zh-CN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value)) : '时间未知'
async function load() { loading.value = true; error.value = ''; try { if (demoEnabled.value) { logs.value = getDemoData('studentHistory'); return } const { data } = await getMyUsage(); logs.value = data?.items || [] } catch (cause) { error.value = cause?.response?.data?.detail || '学习记录暂时无法读取。' } finally { loading.value = false } }
onMounted(load)
</script>

<template>
  <main class="records-page vintage-theme">
    <header class="page-hero">
      <VintageOrnament name="swallow" />
      <VintageRibbonTitle label="LEARNING CONSTELLATION" />
      <h1>学习轨迹</h1>
      <p>这里仅呈现真实记录，不会补造尚未发生的学习数据。</p>
      <VintageDivider />
    </header>

    <StatusState v-if="loading" type="loading" title="正在汇集学习轨迹" />
    <StatusState v-else-if="error" type="error" title="轨迹读取失败" :description="error" @retry="load" />

    <template v-else>
      <section class="metrics" aria-label="学习记录指标">
        <article aria-label="使用次数">
          <span>使用次数</span>
          <strong>{{ logs.length }}</strong>
        </article>
        <article aria-label="使用工具数">
          <span>使用工具数</span>
          <strong>{{ uniqueTools }}</strong>
        </article>
        <article aria-label="活跃学习日">
          <span>活跃学习日</span>
          <strong>{{ activeDays }}</strong>
        </article>
      </section>

      <StatusState v-if="!logs.length" title="还没有学习记录" description="第一次使用工具后，真实轨迹会出现在这里。" />

      <section v-else class="timeline" aria-labelledby="timeline-title">
        <h2 id="timeline-title">最近学习片段</h2>
        <ol>
          <li v-for="log in logs" :key="log.id">
            <time :datetime="log.created_at">{{ formatTime(log.created_at) }}</time>
            <div>
              <span>工具 #{{ log.tool_id }}</span>
              <h3>{{ log.input_text || '未记录输入内容' }}</h3>
              <p v-if="log.output_text">{{ log.output_text }}</p>
            </div>
          </li>
        </ol>
      </section>
    </template>
  </main>
</template>

<style scoped>
.records-page.vintage-theme {
  min-height: 100%;
  padding: clamp(28px, 5vw, 58px) clamp(20px, 4vw, 48px) 80px;
  background:
    radial-gradient(circle at 70% 15%, rgba(184, 161, 110, 0.07), transparent 30%),
    radial-gradient(circle at 20% 90%, rgba(138, 154, 140, 0.05), transparent 28%),
    #f5f1e8;
  color: #4a4333;
}

.records-page.vintage-theme::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.03;
  background-image:
    radial-gradient(circle at 25% 25%, #6b5d3e 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, #6b5d3e 1px, transparent 1px);
  background-size: 80px 80px;
  z-index: 0;
}

/* Hero */
.page-hero {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto 1.5rem;
  text-align: center;
}

.page-hero .vintage-ornament {
  margin-bottom: 0.5rem;
}

.page-hero h1 {
  margin: 0.75rem 0;
  font: 500 clamp(2.4rem, 5vw, 4.2rem)/1.1 var(--font-display);
  color: #3d3526;
}

.page-hero > p {
  max-width: 580px;
  margin: 0 auto;
  color: #6b5d3e;
  line-height: 1.75;
}

.page-hero .vintage-divider {
  margin-top: 1.25rem;
}

/* 指标卡片 */
.metrics {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 0 0 32px;
}

.metrics article {
  padding: 28px 24px;
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.05);
  position: relative;
}

.metrics article::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(139, 111, 71, 0.15);
  pointer-events: none;
  border-radius: 1px;
}

.metrics span, .metrics strong {
  display: block;
}

.metrics span {
  color: #6b5d3e;
  font-size: 0.78rem;
  font-family: var(--font-display);
  letter-spacing: 0.04em;
}

.metrics strong {
  margin-top: 8px;
  color: #8b6f47;
  font: 500 2.7rem var(--font-display);
}

/* 时间线 */
.timeline {
  position: relative;
  z-index: 1;
  max-width: 920px;
  padding: clamp(22px, 4vw, 42px);
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.55);
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.05);
}

.timeline::before {
  content: '';
  position: absolute;
  inset: 5px;
  border: 1px dashed rgba(139, 111, 71, 0.12);
  pointer-events: none;
  border-radius: 1px;
}

.timeline h2 {
  margin: 0 0 28px;
  font: 500 1.6rem var(--font-display);
  color: #3d3526;
}

.timeline ol {
  list-style: none;
  padding: 0;
  margin: 0;
}

.timeline li {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 24px;
  padding: 22px 0;
  border-top: 1px solid rgba(196, 180, 154, 0.25);
}

.timeline time {
  color: #8b7e60;
  font-size: 0.76rem;
  font-family: var(--font-display);
}

.timeline li span {
  color: #8a9a8c;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  font-family: var(--font-display);
}

.timeline h3 {
  margin: 5px 0;
  font: 500 1rem var(--font-display);
  color: #4a4333;
}

.timeline li p {
  display: -webkit-box;
  overflow: hidden;
  color: #6b5d3e;
  line-height: 1.6;
  font-size: 0.88rem;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

@media (max-width: 640px) {
  .records-page { padding: 24px 16px 60px; }
  .metrics { grid-template-columns: 1fr; }
  .timeline li { grid-template-columns: 1fr; gap: 8px; }
}
</style>
