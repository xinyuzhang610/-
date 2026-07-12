<template>
  <div class="dashboard">
    <h2>数据看板</h2>

    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_tools }}</div>
        <div class="stat-label">工具总数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_users }}</div>
        <div class="stat-label">学生人数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.today_usage }}</div>
        <div class="stat-label">今日使用</div>
      </el-card>
    </div>

    <el-card class="trend-card">
      <template #header>
        <span>本周使用趋势</span>
      </template>
      <div class="trend-chart">
        <div v-for="item in stats.weekly_trend" :key="item.date" class="trend-bar">
          <div class="bar" :style="{ height: getBarHeight(item.count) + 'px' }"></div>
          <div class="date">{{ item.date }}</div>
          <div class="count">{{ item.count }}</div>
        </div>
      </div>
    </el-card>

    <el-card class="ranking-card">
      <template #header>
        <span>热门工具排行</span>
      </template>
      <div class="ranking-list">
        <div v-for="(tool, index) in stats.top_tools" :key="tool.name" class="ranking-item">
          <span class="rank">{{ index + 1 }}</span>
          <span class="name">{{ tool.name }}</span>
          <span class="count">{{ tool.count }}次</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboard } from '@/api/usage'
import { ElMessage } from 'element-plus'

const stats = ref({
  total_tools: 0,
  total_users: 0,
  today_usage: 0,
  weekly_trend: [],
  top_tools: [],
  recent_logs: []
})

onMounted(async () => {
  await loadDashboard()
})

const loadDashboard = async () => {
  try {
    const { data } = await getDashboard()
    stats.value = data
  } catch (error) {
    ElMessage.error('加载数据看板失败')
  }
}

const getBarHeight = (count) => {
  const maxCount = Math.max(...stats.value.weekly_trend.map(i => i.count), 1)
  return (count / maxCount) * 100
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  color: #666;
  margin-top: 10px;
}
.trend-card, .ranking-card {
  margin-bottom: 20px;
}
.trend-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 150px;
  padding: 20px 0;
}
.trend-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.bar {
  width: 40px;
  background: linear-gradient(180deg, #409eff, #66b1ff);
  border-radius: 4px 4px 0 0;
  min-height: 5px;
}
.date {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}
.count {
  font-size: 12px;
  color: #409eff;
}
.ranking-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.rank {
  width: 30px;
  height: 30px;
  background: #409eff;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-weight: bold;
}
.ranking-item:nth-child(1) .rank {
  background: #f56c6c;
}
.ranking-item:nth-child(2) .rank {
  background: #e6a23c;
}
.ranking-item:nth-child(3) .rank {
  background: #67c23a;
}
.name {
  flex: 1;
}
.count {
  color: #666;
}
</style>
