<template>
  <div class="records-container">
    <h2 class="page-title">📊 我的学习记录</h2>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-value">{{ stats.totalUsage }}</div>
        <div class="stat-label">使用次数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.toolCount }}</div>
        <div class="stat-label">使用工具数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.streakDays }}</div>
        <div class="stat-label">连续天数</div>
      </div>
    </div>

    <!-- 最近使用 -->
    <div class="section">
      <h3 class="section-title">最近使用</h3>
      <div class="record-list">
        <div
          v-for="record in recentRecords"
          :key="record.id"
          class="record-item"
        >
          <span class="record-time">{{ record.time }}</span>
          <span class="record-icon">{{ record.icon }}</span>
          <span class="record-tool">{{ record.toolName }}</span>
          <span class="record-input">输入："{{ record.input }}"</span>
        </div>
      </div>
    </div>

    <!-- 收藏的工具 -->
    <div class="section">
      <h3 class="section-title">收藏的工具</h3>
      <div class="favorite-list">
        <div
          v-for="tool in favoriteTools"
          :key="tool.id"
          class="favorite-item"
          @click="useTool(tool)"
        >
          <span class="favorite-icon">{{ tool.icon }}</span>
          <span class="favorite-name">{{ tool.name }}</span>
          <el-button type="primary" size="small">进入</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 统计数据
const stats = ref({
  totalUsage: 12,
  toolCount: 3,
  streakDays: 5
})

// 最近使用记录
const recentRecords = ref([
  {
    id: 1,
    time: '7/15 14:30',
    icon: '🏮',
    toolName: '古诗词赏析',
    input: '静夜思'
  },
  {
    id: 2,
    time: '7/15 10:20',
    icon: '🧮',
    toolName: '公式推导',
    input: '勾股定理'
  },
  {
    id: 3,
    time: '7/14 16:45',
    icon: '🤖',
    toolName: 'AI问答',
    input: '牛顿第三定律是什么'
  },
  {
    id: 4,
    time: '7/14 10:15',
    icon: '✍️',
    toolName: '作文辅助',
    input: '我的暑假计划'
  }
])

// 收藏的工具
const favoriteTools = ref([
  { id: 1, name: '古诗词赏析', icon: '🏮' },
  { id: 2, name: '作文辅助', icon: '✍️' },
  { id: 7, name: '公式推导', icon: '🧮' }
])

// 使用工具
const useTool = (tool) => {
  router.push(`/tool/${tool.id}`)
}
</script>

<style scoped>
.records-container {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-family: var(--font-heading);
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
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.stat-value {
  font-family: var(--font-heading);
  font-size: 36px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.stat-label {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 区块 */
.section {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
}

.section-title {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 16px;
}

/* 记录列表 */
.record-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--color-chip-bg);
  border-radius: var(--radius-md);
}

.record-time {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-soft);
  width: 100px;
}

.record-icon {
  font-size: 20px;
}

.record-tool {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-ink);
  width: 100px;
}

.record-input {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-soft);
  flex: 1;
}

/* 收藏列表 */
.favorite-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.favorite-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--color-chip-bg);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.3s;
}

.favorite-item:hover {
  background: var(--color-border);
}

.favorite-icon {
  font-size: 24px;
}

.favorite-name {
  flex: 1;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--color-ink);
}
</style>
