<template>
  <div class="dashboard-container">
    <h2 class="page-title">数据看板</h2>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon">🔧</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.toolCount }}</div>
          <div class="stat-label">工具总数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.studentCount }}</div>
          <div class="stat-label">学生人数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.todayUsage }}</div>
          <div class="stat-label">今日使用</div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="chart-section">
      <div class="chart-card">
        <h3 class="chart-title">使用趋势</h3>
        <div class="chart-placeholder">
          <div class="chart-bars">
            <div
              v-for="(item, index) in trendData"
              :key="index"
              class="chart-bar"
              :style="{ height: item.value + '%' }"
            >
              <span class="bar-label">{{ item.value }}</span>
            </div>
          </div>
          <div class="chart-labels">
            <span v-for="(item, index) in trendData" :key="index">
              {{ item.date }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 排行榜和记录 -->
    <div class="bottom-section">
      <!-- 热门工具排行 -->
      <div class="ranking-card">
        <h3 class="section-title">热门工具排行</h3>
        <div class="ranking-list">
          <div
            v-for="(tool, index) in hotTools"
            :key="tool.id"
            class="ranking-item"
          >
            <span class="ranking-number" :class="{ top: index < 3 }">
              {{ index + 1 }}
            </span>
            <span class="ranking-icon">{{ tool.icon }}</span>
            <span class="ranking-name">{{ tool.name }}</span>
            <span class="ranking-count">{{ tool.usageCount }}次</span>
          </div>
        </div>
      </div>

      <!-- 最近使用记录 -->
      <div class="records-card">
        <h3 class="section-title">最近使用记录</h3>
        <el-table :data="recentRecords" style="width: 100%">
          <el-table-column prop="student" label="学生" width="80" />
          <el-table-column prop="toolName" label="使用工具" width="150" />
          <el-table-column prop="input" label="输入内容" />
          <el-table-column prop="time" label="时间" width="150" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 统计数据
const stats = ref({
  toolCount: 5,
  studentCount: 42,
  todayUsage: 18
})

// 趋势数据
const trendData = ref([
  { date: '7/10', value: 30 },
  { date: '7/11', value: 45 },
  { date: '7/12', value: 35 },
  { date: '7/13', value: 60 },
  { date: '7/14', value: 50 },
  { date: '7/15', value: 75 },
  { date: '7/16', value: 65 }
])

// 热门工具
const hotTools = ref([
  { id: 1, name: '古诗词趣味赏析', icon: '🏮', usageCount: 23 },
  { id: 2, name: '公式推导助手', icon: '🧮', usageCount: 15 },
  { id: 3, name: '作文灵感助手', icon: '✍️', usageCount: 8 },
  { id: 4, name: '实验模拟讲解', icon: '🔬', usageCount: 6 },
  { id: 5, name: '逻辑思维训练', icon: '🧠', usageCount: 4 }
])

// 最近使用记录
const recentRecords = ref([
  {
    student: '小明',
    toolName: '古诗词赏析',
    input: '静夜思',
    time: '7/15 14:30'
  },
  {
    student: '小红',
    toolName: '公式推导',
    input: '勾股定理',
    time: '7/15 15:20'
  },
  {
    student: '小刚',
    toolName: '作文助手',
    input: '我的梦想',
    time: '7/15 16:45'
  },
  {
    student: '小丽',
    toolName: '实验模拟',
    input: '光的折射',
    time: '7/15 17:10'
  }
])
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 24px;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  font-size: 40px;
  margin-right: 16px;
}

.stat-value {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 600;
  color: var(--color-ink);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 图表区域 */
.chart-section {
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.chart-title {
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 20px;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 200px;
  padding: 0 20px;
  border-bottom: 2px solid var(--color-chip-bg);
}

.chart-bar {
  width: 40px;
  background: linear-gradient(to top, var(--color-ink), #3a3933);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  position: relative;
  transition: height 0.5s;
}

.bar-label {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--color-ink-soft);
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  padding: 8px 20px 0;
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--color-ink-soft);
}

/* 底部区域 */
.bottom-section {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
}

.ranking-card,
.records-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.section-title {
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 16px;
}

/* 排行榜 */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-chip-bg);
}

.ranking-item:last-child {
  border-bottom: none;
}

.ranking-number {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-ink-soft);
  background: var(--color-chip-bg);
  border-radius: 50%;
}

.ranking-number.top {
  background: var(--color-ink);
  color: white;
}

.ranking-icon {
  font-size: 20px;
}

.ranking-name {
  flex: 1;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink);
}

.ranking-count {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 表格样式 */
.records-card :deep(.el-table) {
  font-family: var(--font-sans);
}

.records-card :deep(.el-table th) {
  background: var(--color-chip-bg);
  color: var(--color-ink);
  font-weight: 600;
}

.records-card :deep(.el-table td) {
  color: var(--color-ink-soft);
}
</style>
