<script setup>
import { computed, onMounted, ref } from 'vue'
import { getMyUsage } from '../../api/usage'
import StatusState from '../../components/ui/StatusState.vue'
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
  <main class="records-page"><header><p>LEARNING CONSTELLATION</p><h1>学习轨迹</h1><span>这里仅呈现真实记录，不会补造尚未发生的学习数据。</span></header>
    <StatusState v-if="loading" type="loading" title="正在汇集学习轨迹" />
    <StatusState v-else-if="error" type="error" title="轨迹读取失败" :description="error" @retry="load" />
    <template v-else><section class="metrics" aria-label="学习记录指标"><article aria-label="使用次数"><span>使用次数</span><strong>{{ logs.length }}</strong></article><article aria-label="使用工具数"><span>使用工具数</span><strong>{{ uniqueTools }}</strong></article><article aria-label="活跃学习日"><span>活跃学习日</span><strong>{{ activeDays }}</strong></article></section>
      <StatusState v-if="!logs.length" title="还没有学习记录" description="第一次使用工具后，真实轨迹会出现在这里。" />
      <section v-else class="timeline" aria-labelledby="timeline-title"><h2 id="timeline-title">最近学习片段</h2><ol><li v-for="log in logs" :key="log.id"><time :datetime="log.created_at">{{ formatTime(log.created_at) }}</time><div><span>工具 #{{ log.tool_id }}</span><h3>{{ log.input_text || '未记录输入内容' }}</h3><p v-if="log.output_text">{{ log.output_text }}</p></div></li></ol></section>
    </template>
  </main>
</template>

<style scoped>
.records-page{min-height:100%;padding:clamp(28px,5vw,64px);background:linear-gradient(160deg,#101916,#182923);color:var(--moon-50)}header p{color:var(--gold-300);font-size:.7rem;letter-spacing:.22em}header h1{margin:12px 0;font:500 clamp(2.4rem,5vw,4.5rem) var(--font-display)}header span{color:var(--moon-300)}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:38px 0}.metrics article{padding:24px;border:1px solid rgb(203 211 201 / 16%);border-radius:20px;background:rgb(255 255 255 / 4%)}.metrics span,.metrics strong{display:block}.metrics span{color:var(--moon-300);font-size:.78rem}.metrics strong{margin-top:8px;color:var(--gold-300);font:500 2.7rem var(--font-display)}.timeline{max-width:920px;padding:clamp(22px,4vw,42px);border:1px solid rgb(203 211 201 / 16%);border-radius:28px;background:rgb(255 255 255 / 4%)}.timeline h2{margin-bottom:28px;font:500 1.7rem var(--font-heading)}.timeline ol{list-style:none}.timeline li{display:grid;grid-template-columns:150px 1fr;gap:24px;padding:22px 0;border-top:1px solid rgb(255 255 255 / 10%)}.timeline time{color:var(--ink-300);font-size:.76rem}.timeline li span{color:var(--jade-200);font-size:.72rem}.timeline h3{margin:5px 0;font:500 1rem var(--font-heading)}.timeline li p{display:-webkit-box;overflow:hidden;color:var(--moon-300);line-height:1.6;-webkit-box-orient:vertical;-webkit-line-clamp:2}@media(max-width:640px){.records-page{padding:24px 16px}.metrics{grid-template-columns:1fr}.timeline li{grid-template-columns:1fr;gap:8px}}
</style>
