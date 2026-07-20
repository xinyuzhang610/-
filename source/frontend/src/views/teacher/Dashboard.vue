<template>
  <div class="dashboard-page vintage-theme">
    <header class="dashboard-head">
      <div>
        <VintageRibbonTitle label="LEARNING SIGNALS" />
        <h1>数据洞察</h1>
        <p>从真实使用记录中，看见工具如何进入课堂。</p>
      </div>
      <div class="dashboard-actions">
        <label>时间范围<select v-model="days" @change="loadDashboard"><option :value="7">近 7 天</option><option :value="30">近 30 天</option></select></label>
        <button type="button" @click="downloadDashboard">导出 CSV</button>
      </div>
    </header>
    <VintageDivider />

    <StatusState v-if="loading" type="loading" title="正在汇聚课堂信号" />
    <StatusState v-else-if="errorMessage" type="error" title="数据暂时不可用" :description="errorMessage" @retry="loadDashboard" />
    <StatusState v-else-if="!dashboard" type="empty" title="还没有使用数据" description="学生开始使用工具后，趋势与记录会在这里出现。" />
    <template v-else>
      <section class="metrics" aria-label="关键指标">
        <MetricCard label="工具总数" :value="dashboard.total_tools" trend="已接入工具库"/>
        <MetricCard label="用户总数" :value="dashboard.total_users" tone="gold" trend="教师与学生"/>
        <MetricCard label="今日使用" :value="dashboard.today_usage" trend="实时累计"/>
      </section>

      <section class="dashboard-grid">
        <article class="panel trend-panel">
          <h2>七日使用趋势</h2>
          <div class="bars" role="img" aria-label="七日使用趋势柱状图">
            <div v-for="item in dashboard.weekly_trend" :key="item.date" class="bar-item">
              <span class="bar-value">{{ item.count }}</span>
              <div class="bar"><i :style="{height:barHeight(item.count)}"></i></div>
              <small>{{ item.date }}</small>
            </div>
          </div>
        </article>

        <article class="panel">
          <h2>热门工具</h2>
          <ol class="ranking">
            <li v-for="(tool,index) in dashboard.top_tools" :key="tool.name">
              <span>{{ String(index+1).padStart(2,'0') }}</span>
              <strong>{{ tool.name }}</strong>
              <small>{{ tool.count }} 次</small>
            </li>
          </ol>
        </article>
      </section>

      <section class="panel records">
        <h2>最近使用记录</h2>
        <div v-if="dashboard.recent_logs?.length" class="record-list">
          <div v-for="log in dashboard.recent_logs" :key="log.id">
            <span>{{ log.user_name || `用户 ${log.user_id || '-'}` }}</span>
            <strong>{{ log.tool_name || `工具 ${log.tool_id || '-'}` }}</strong>
            <time>{{ formatTime(log.created_at) }}</time>
          </div>
        </div>
        <p v-else class="empty-copy">暂无最近记录。</p>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import MetricCard from '../../components/data/MetricCard.vue'
import StatusState from '../../components/ui/StatusState.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import { getDashboard, exportDashboard } from '../../api/usage'
import { useDemoMode } from '../../composables/useDemoMode'
const dashboard=ref(null),loading=ref(true),errorMessage=ref(''),days=ref(7)
const {enabled:demoEnabled,getDemoData}=useDemoMode()
const maxCount=computed(()=>Math.max(1,...(dashboard.value?.weekly_trend||[]).map(i=>i.count)))
const barHeight=count=>`${Math.max(5,(count/maxCount.value)*100)}%`
const formatTime=value=>value?new Intl.DateTimeFormat('zh-CN',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(value)):'时间未知'
async function loadDashboard(){loading.value=true;errorMessage.value='';try{if(demoEnabled.value){dashboard.value=getDemoData('dashboard');return}const {data}=await getDashboard({ days: days.value });dashboard.value=data}catch(e){dashboard.value=null;errorMessage.value=e.response?.data?.detail||'无法连接统计服务，请确认后端已启动。'}finally{loading.value=false}}
async function downloadDashboard(){try{const {data}=await exportDashboard({days:days.value});const url=URL.createObjectURL(data);const link=document.createElement('a');link.href=url;link.download=`dashboard-${days.value}d.csv`;link.click();URL.revokeObjectURL(url)}catch(e){errorMessage.value=e.response?.data?.detail||'CSV 导出失败，请稍后重试。'}}
onMounted(loadDashboard)
</script>

<style scoped>
.dashboard-page.vintage-theme {
  max-width: 1240px;
  margin: auto;
  padding: clamp(24px, 4vw, 52px) clamp(20px, 3vw, 48px) 80px;
  background:
    radial-gradient(circle at 10% 5%, rgba(184, 161, 110, 0.06), transparent 30%),
    radial-gradient(circle at 90% 95%, rgba(138, 154, 140, 0.06), transparent 35%),
    #f5f1e8;
  color: #4a4333;
  min-height: 100%;
}

.dashboard-page.vintage-theme::before {
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

.dashboard-page > header {
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.dashboard-page h1 {
  margin: 10px 0;
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5vw, 4.2rem);
  font-weight: 500;
  color: #3d3526;
  line-height: 1.12;
}

.dashboard-page header p {
  color: #6b5d3e;
  font-size: 0.95rem;
  line-height: 1.7;
}

.vintage-divider {
  position: relative;
  z-index: 1;
  margin-bottom: 2rem;
}

.dashboard-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; }
.dashboard-actions { display: flex; align-items: end; gap: 10px; position: relative; z-index: 1; }
.dashboard-actions label { display: grid; gap: 6px; color: #6b5d3e; font-size: 0.75rem; }
.dashboard-actions select, .dashboard-actions button { min-height: 42px; padding: 0 12px; border: 1px solid rgba(196, 180, 154, 0.5); border-radius: 2px; background: rgba(250, 248, 242, 0.7); color: #4a4333; font: inherit; }
.dashboard-actions select option { color: #111; }
.dashboard-actions button { border-color: #b8a16e; background: #b8a16e; color: #3d3526; font-weight: 700; cursor: pointer; }

.metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  position: relative;
  z-index: 1;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
  margin-top: 16px;
  position: relative;
  z-index: 1;
}

.panel {
  padding: 24px;
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.55);
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.05);
  position: relative;
}

.panel::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(139, 111, 71, 0.12);
  pointer-events: none;
  border-radius: 1px;
}

.panel h2 {
  margin: 0 0 22px;
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 600;
  color: #4a4333;
}

/* 柱状图 */
.bars {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 260px;
}

.bar-item {
  display: grid;
  grid-template-rows: 20px 1fr 24px;
  align-items: end;
  flex: 1;
  height: 100%;
  text-align: center;
}

.bar-value, .bar-item small {
  color: #6b5d3e;
  font-size: 0.72rem;
}

.bar {
  position: relative;
  height: 100%;
  border-bottom: 1px solid rgba(196, 180, 154, 0.4);
}

.bar i {
  position: absolute;
  bottom: 0;
  left: 20%;
  width: 60%;
  border-radius: 3px 3px 0 0;
  background: linear-gradient(180deg, #8a9a8c, #6e7d70);
  box-shadow: 0 0 14px rgba(138, 154, 140, 0.25);
}

/* 排行榜 */
.ranking {
  display: grid;
  gap: 2px;
  padding: 0;
  list-style: none;
}

.ranking li {
  display: grid;
  grid-template-columns: 38px 1fr auto;
  align-items: center;
  min-height: 50px;
  border-bottom: 1px solid rgba(196, 180, 154, 0.25);
}

.ranking li > span {
  color: #b8a16e;
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
}

.ranking strong {
  color: #4a4333;
  font-weight: 500;
}

.ranking small {
  color: #6b5d3e;
  font-size: 0.8rem;
}

/* 使用记录 */
.records {
  margin-top: 16px;
}

.record-list > div {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr;
  gap: 18px;
  padding: 14px 0;
  border-top: 1px solid rgba(196, 180, 154, 0.25);
}

.record-list span, .record-list time, .empty-copy {
  color: #6b5d3e;
  font-size: 0.85rem;
}

.record-list strong {
  color: #4a4333;
  font-weight: 500;
  font-size: 0.9rem;
}

.empty-copy {
  font-style: italic;
  padding: 1rem 0;
}

@media (max-width: 800px) {
  .dashboard-head { align-items: flex-start; flex-direction: column; }
  .dashboard-actions { align-items: stretch; width: 100%; }
  .dashboard-actions label { flex: 1; }
  .metrics, .dashboard-grid { grid-template-columns: 1fr; }
  .bars { height: 220px; }
  .record-list > div { grid-template-columns: 1fr; }
  .record-list time { text-align: left; }
}
</style>
