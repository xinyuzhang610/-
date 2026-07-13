<script setup>
import { onMounted, ref } from 'vue'
import { getPlaza } from '../../api/plaza'
import StatusState from '../../components/ui/StatusState.vue'
import ToolCard from '../../components/student/ToolCard.vue'

const categories = ref([]), tools = ref([]), hotTools = ref([])
const category = ref(''), search = ref(''), loading = ref(true), error = ref('')
async function load() {
  loading.value = true; error.value = ''
  try {
    const { data } = await getPlaza({ category: category.value, search: search.value.trim() })
    categories.value = data.categories || []; tools.value = data.tools || []; hotTools.value = data.hot_tools || []
  } catch (cause) { error.value = cause?.response?.data?.detail || '工具广场暂时无法连接，请稍后重试。' }
  finally { loading.value = false }
}
async function pick(value) { category.value = category.value === value ? '' : value; await load() }
onMounted(load)
</script>

<template>
  <main class="plaza-page">
    <header><p class="eyebrow">KNOWLEDGE TOOL ATLAS</p><h1>工具广场</h1><p>从真实的公共工具库中，找到与你此刻问题最接近的解法。</p></header>
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
    <section v-else aria-labelledby="tools-title"><div class="section-heading"><h2 id="tools-title">探索工具</h2><span>{{ tools.length }} 个结果</span></div><div class="tool-grid"><ToolCard v-for="tool in tools" :key="tool.id" :tool="tool" :hot="hotTools.some(item => item.id === tool.id)" /></div></section>
  </main>
</template>

<style scoped>
.plaza-page{min-height:100%;padding:clamp(28px,4vw,58px);background:radial-gradient(circle at 86% 6%,rgb(213 166 79 / 12%),transparent 24%),#101916;color:var(--moon-50)}header{max-width:760px}.eyebrow{color:var(--jade-400);font-size:.72rem;letter-spacing:.22em}h1{margin:10px 0;font:500 clamp(2.5rem,5vw,4.5rem) var(--font-display)}header p:last-child{color:var(--moon-300);line-height:1.8}.search-panel{display:grid;grid-template-columns:1fr auto;max-width:860px;margin:34px 0 18px;padding:6px;border:1px solid rgb(213 166 79 / 30%);border-radius:18px;background:rgb(255 255 255 / 5%)}.search-panel label span{position:absolute;overflow:hidden;width:1px;height:1px;clip:rect(0,0,0,0)}.search-panel input{width:100%;min-height:48px;padding:0 16px;border:0;background:transparent;color:var(--moon-50);font:inherit;outline:0}.search-panel button,.category-tabs button{min-height:44px;border:0;border-radius:12px;cursor:pointer}.search-panel button{padding:0 26px;background:var(--gold-400);color:var(--ink-950);font-weight:700}.category-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:42px}.category-tabs button{padding:0 18px;border:1px solid rgb(203 211 201 / 20%);background:transparent;color:var(--moon-300)}.category-tabs button[aria-pressed="true"]{border-color:var(--jade-400);background:rgb(66 185 154 / 12%);color:var(--moon-50)}.section-heading{display:flex;align-items:end;justify-content:space-between;margin-bottom:18px}.section-heading h2{font:500 1.8rem var(--font-heading)}.section-heading span{color:var(--ink-300)}.tool-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}@media(max-width:1000px){.tool-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:620px){.plaza-page{padding:24px 16px}.search-panel{grid-template-columns:1fr}.search-panel button{width:100%}.tool-grid{grid-template-columns:1fr}}
</style>
