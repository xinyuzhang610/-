<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPlaza } from '../../api/plaza'
import { getRecommendedTools } from '../../api/tools'
import StatusState from '../../components/ui/StatusState.vue'
import ToolCard from '../../components/student/ToolCard.vue'
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageOrnament from '../../components/vintage/VintageOrnament.vue'
import { useDemoMode } from '../../composables/useDemoMode'

const categories = ref([]), tools = ref([]), hotTools = ref([])
const category = ref(''), search = ref(''), loading = ref(true), error = ref('')
const recommendation = ref('')
const { enabled: demoEnabled, getDemoData } = useDemoMode()
const route = useRoute()
const router = useRouter()
async function load() {
  loading.value = true; error.value = ''
  try {
    if (demoEnabled.value) {
      const demo = getDemoData('plaza'); categories.value = demo.categories; hotTools.value = demo.hot_tools
      tools.value = demo.tools.filter(item => (!category.value || item.category === category.value) && (!search.value.trim() || `${item.name} ${item.description}`.includes(search.value.trim())))
      return
    }
    if (route.query.subject && !search.value.trim()) {
      const { data } = await getRecommendedTools(category.value, route.query.subject, route.query.difficulty || route.query.approach || '兴趣激发')
      tools.value = data.tools || []
      categories.value = [{ value: '文科', label: '文科' }, { value: '理科', label: '理科' }, { value: '通用', label: '通用' }]
      hotTools.value = tools.value.slice(0, 3)
      recommendation.value = `根据"${route.query.difficulty || '当前困惑'} · ${route.query.subject} · ${route.query.approach || '学习方式'}"为你匹配`
      return
    }
    recommendation.value = ''
    const { data } = await getPlaza({ category: category.value, search: search.value.trim() })
    categories.value = data.categories || []; tools.value = data.tools || []; hotTools.value = data.hot_tools || []
  } catch (cause) { error.value = cause?.response?.data?.detail || '工具广场暂时无法连接，请稍后重试。' }
  finally { loading.value = false }
}
async function pick(value) { category.value = category.value === value ? '' : value; if (route.query.subject) await router.replace({ query: {} }); await load() }
onMounted(() => { category.value = route.query.subject === '语文' || route.query.subject === '英语' || route.query.subject === '历史' ? '文科' : ['数学', '物理', '化学'].includes(route.query.subject) ? '理科' : ''; load() })
watch(() => route.query, () => { category.value = route.query.subject === '语文' || route.query.subject === '英语' || route.query.subject === '历史' ? '文科' : ['数学', '物理', '化学'].includes(route.query.subject) ? '理科' : ''; load() }, { deep: true })
</script>

<template>
  <main class="plaza-page vintage-theme">
    <header class="page-hero">
      <VintageOrnament name="swallow" />
      <VintageRibbonTitle label="KNOWLEDGE TOOL ATLAS" />
      <h1>工具广场</h1>
      <p>从真实的公共工具库中，找到与你此刻问题最接近的解法。</p>
      <VintageDivider />
    </header>

    <p v-if="recommendation" class="recommendation" role="status">{{ recommendation }}</p>

    <form class="search-panel" role="search" @submit.prevent="load">
      <label aria-label="搜索工具"><span>搜索工具</span><input v-model="search" type="search" placeholder="输入工具名称或能力关键词" /></label>
      <button type="submit">搜索</button>
    </form>

    <nav class="category-tabs" aria-label="工具分类">
      <button type="button" :aria-pressed="category === ''" @click="pick('')">全部工具</button>
      <button v-for="item in categories" :key="item.value" type="button" :aria-label="item.label" :aria-pressed="category === item.value" @click="pick(item.value)">{{ item.label }}</button>
    </nav>

    <StatusState v-if="loading" type="loading" title="正在绘制工具星图" description="从公共工具库读取最新数据。" />
    <StatusState v-else-if="error" type="error" title="工具星图暂时失联" :description="error" @retry="load" />
    <StatusState v-else-if="!tools.length" title="没有匹配的工具" description="调整分类或搜索词，再探索一次。" />

    <section v-else aria-labelledby="tools-title">
      <div class="section-heading">
        <h2 id="tools-title">探索工具</h2>
        <span>{{ tools.length }} 个结果</span>
      </div>
      <div class="tool-grid">
        <ToolCard v-for="tool in tools" :key="tool.id" :tool="tool" :hot="hotTools.some(item => item.id === tool.id)" />
      </div>
    </section>
  </main>
</template>

<style scoped>
.plaza-page.vintage-theme {
  min-height: 100%;
  padding: clamp(28px, 4vw, 58px) clamp(20px, 4vw, 48px) 80px;
  background:
    radial-gradient(circle at 86% 6%, rgba(184, 161, 110, 0.08), transparent 28%),
    radial-gradient(circle at 15% 90%, rgba(138, 154, 140, 0.06), transparent 25%),
    #f5f1e8;
  color: #4a4333;
}

.plaza-page.vintage-theme::before {
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
  font: 500 clamp(2.5rem, 5vw, 4.2rem)/1.1 var(--font-display);
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

/* 推荐标签 */
.recommendation {
  position: relative;
  z-index: 1;
  display: inline-block;
  margin: 0 0 16px;
  padding: 8px 16px;
  border: 1px solid rgba(138, 154, 140, 0.4);
  border-radius: 2px;
  background: rgba(138, 154, 140, 0.08);
  color: #6e7d70;
  font-size: 0.82rem;
  font-family: var(--font-display);
}

/* 搜索栏 */
.search-panel {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr auto;
  max-width: 860px;
  margin: 28px 0 18px;
  padding: 5px;
  border: 1px solid rgba(196, 180, 154, 0.4);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
}

.search-panel label span {
  position: absolute;
  overflow: hidden;
  width: 1px;
  height: 1px;
  clip: rect(0, 0, 0, 0);
}

.search-panel input {
  width: 100%;
  min-height: 48px;
  padding: 0 16px;
  border: 0;
  background: transparent;
  color: #4a4333;
  font: inherit;
  outline: 0;
}

.search-panel input::placeholder {
  color: #b0a590;
}

.search-panel button {
  padding: 0 28px;
  min-height: 44px;
  border: 1px solid #b8a16e;
  border-radius: 2px;
  background: linear-gradient(135deg, rgba(250, 248, 242, 0.95), rgba(242, 239, 230, 0.85));
  color: #5c4f34;
  font: inherit;
  font-family: var(--font-display);
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.search-panel button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(107, 93, 62, 0.1);
}

/* 分类标签 */
.category-tabs {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 36px;
}

.category-tabs button {
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.45);
  color: #6b5d3e;
  font: inherit;
  font-family: var(--font-display);
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tabs button:hover {
  border-color: rgba(184, 161, 110, 0.5);
  background: rgba(250, 248, 242, 0.75);
}

.category-tabs button[aria-pressed="true"] {
  border-color: rgba(138, 154, 140, 0.5);
  background: rgba(138, 154, 140, 0.12);
  color: #4a4333;
  font-weight: 600;
}

/* 结果区 */
.section-heading {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: end;
  justify-content: space-between;
  margin-bottom: 18px;
}

.section-heading h2 {
  font: 500 1.7rem var(--font-display);
  color: #3d3526;
  margin: 0;
}

.section-heading span {
  color: #8b7e60;
  font-size: 0.85rem;
}

.tool-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

@media (max-width: 1000px) {
  .tool-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 620px) {
  .plaza-page { padding: 24px 16px 60px; }
  .search-panel { grid-template-columns: 1fr; }
  .search-panel button { width: 100%; }
  .tool-grid { grid-template-columns: 1fr; }
}
</style>
