<template>
  <div class="dashboard-page"><header><span>LEARNING SIGNALS</span><h1>数据洞察</h1><p>从真实使用记录中，看见工具如何进入课堂。</p></header>
    <StatusState v-if="loading" type="loading" title="正在汇聚课堂信号" />
    <StatusState v-else-if="errorMessage" type="error" title="数据暂时不可用" :description="errorMessage" @retry="loadDashboard" />
    <StatusState v-else-if="!dashboard" type="empty" title="还没有使用数据" description="学生开始使用工具后，趋势与记录会在这里出现。" />
    <template v-else><section class="metrics" aria-label="关键指标"><MetricCard label="工具总数" :value="dashboard.total_tools" trend="已接入工具库"/><MetricCard label="用户总数" :value="dashboard.total_users" tone="gold" trend="教师与学生"/><MetricCard label="今日使用" :value="dashboard.today_usage" trend="实时累计"/></section>
      <section class="dashboard-grid"><article class="panel trend-panel"><h2>七日使用趋势</h2><div class="bars" role="img" aria-label="七日使用趋势柱状图"><div v-for="item in dashboard.weekly_trend" :key="item.date" class="bar-item"><span class="bar-value">{{ item.count }}</span><div class="bar"><i :style="{height:barHeight(item.count)}"></i></div><small>{{ item.date }}</small></div></div></article>
      <article class="panel"><h2>热门工具</h2><ol class="ranking"><li v-for="(tool,index) in dashboard.top_tools" :key="tool.name"><span>{{ String(index+1).padStart(2,'0') }}</span><strong>{{ tool.name }}</strong><small>{{ tool.count }} 次</small></li></ol></article></section>
      <section class="panel records"><h2>最近使用记录</h2><div v-if="dashboard.recent_logs?.length" class="record-list"><div v-for="log in dashboard.recent_logs" :key="log.id"><span>{{ log.user_name || `用户 ${log.user_id || '-'}` }}</span><strong>{{ log.tool_name || `工具 ${log.tool_id || '-'}` }}</strong><time>{{ formatTime(log.created_at) }}</time></div></div><p v-else class="empty-copy">暂无最近记录。</p></section>
    </template>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import MetricCard from '../../components/data/MetricCard.vue'
import StatusState from '../../components/ui/StatusState.vue'
import { getDashboard } from '../../api/usage'
const dashboard=ref(null),loading=ref(true),errorMessage=ref('')
const maxCount=computed(()=>Math.max(1,...(dashboard.value?.weekly_trend||[]).map(i=>i.count)))
const barHeight=count=>`${Math.max(5,(count/maxCount.value)*100)}%`
const formatTime=value=>value?new Intl.DateTimeFormat('zh-CN',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(value)):'时间未知'
async function loadDashboard(){loading.value=true;errorMessage.value='';try{const {data}=await getDashboard();dashboard.value=data}catch(e){dashboard.value=null;errorMessage.value=e.response?.data?.detail||'无法连接统计服务，请确认后端已启动。'}finally{loading.value=false}}
onMounted(loadDashboard)
</script>
<style scoped>
.dashboard-page{max-width:1240px;margin:auto}.dashboard-page>header{margin-bottom:34px}.dashboard-page header>span{color:var(--gold-300);font-size:.68rem;letter-spacing:.23em}.dashboard-page h1{margin:8px 0;font-family:var(--font-display);font-size:clamp(2.4rem,5vw,4.7rem);font-weight:500}.dashboard-page header p{color:var(--moon-300)}.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.dashboard-grid{display:grid;grid-template-columns:1.6fr 1fr;gap:16px;margin-top:16px}.panel{padding:24px;border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel-dark)}.panel h2{margin:0 0 22px;font-family:var(--font-display);font-size:1.5rem}.bars{display:flex;align-items:flex-end;gap:12px;height:260px}.bar-item{display:grid;grid-template-rows:20px 1fr 24px;align-items:end;flex:1;height:100%;text-align:center}.bar-value,.bar-item small{color:var(--moon-300);font-size:.72rem}.bar{position:relative;height:100%;border-bottom:1px solid var(--color-border)}.bar i{position:absolute;bottom:0;left:20%;width:60%;border-radius:6px 6px 0 0;background:linear-gradient(var(--jade-400),var(--jade-700));box-shadow:0 0 18px var(--effect-jade-soft)}.ranking{display:grid;gap:4px;padding:0;list-style:none}.ranking li{display:grid;grid-template-columns:38px 1fr auto;align-items:center;min-height:50px;border-bottom:1px solid var(--color-border)}.ranking li>span{color:var(--gold-300)}.ranking small{color:var(--moon-300)}.records{margin-top:16px}.record-list>div{display:grid;grid-template-columns:1fr 1.5fr 1fr;gap:18px;padding:14px 0;border-top:1px solid var(--color-border)}.record-list span,.record-list time,.empty-copy{color:var(--moon-300)}@media(max-width:800px){.metrics,.dashboard-grid{grid-template-columns:1fr}.bars{height:220px}.record-list>div{grid-template-columns:1fr}.record-list time{text-align:left}}
</style>
