<template>
  <div class="records">
    <h2>我的学习记录</h2>

    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_usage }}</div>
        <div class="stat-label">使用次数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.unique_tools }}</div>
        <div class="stat-label">使用工具数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.streak_days }}</div>
        <div class="stat-label">连续天数</div>
      </el-card>
    </div>

    <el-card class="recent-card">
      <template #header>
        <span>最近使用</span>
      </template>
      <div class="recent-list">
        <div v-for="record in records" :key="record.id" class="record-item">
          <div class="record-time">{{ formatDate(record.created_at) }}</div>
          <div class="record-content">
            <span class="record-tool">工具ID: {{ record.tool_id }}</span>
            <span class="record-input">{{ record.input_text }}</span>
          </div>
        </div>
      </div>
      <el-empty v-if="records.length === 0" description="还没有使用记录" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyUsage } from '@/api/usage'
import { ElMessage } from 'element-plus'

const records = ref([])
const stats = ref({
  total_usage: 0,
  unique_tools: 0,
  streak_days: 0
})

onMounted(async () => {
  await loadRecords()
})

const loadRecords = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (!user.id) {
      ElMessage.warning('请先登录')
      return
    }
    const { data } = await getMyUsage(user.id)
    records.value = data
    stats.value.total_usage = data.length
    const uniqueToolIds = new Set(data.map(r => r.tool_id))
    stats.value.unique_tools = uniqueToolIds.size
    const dates = [...new Set(data.map(r => new Date(r.created_at).toDateString()))]
    stats.value.streak_days = dates.length
  } catch (error) {
    ElMessage.error('加载记录失败')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.records {
  max-width: 800px;
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
.recent-card {
  margin-bottom: 20px;
}
.record-item {
  display: flex;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}
.record-time {
  width: 100px;
  color: #666;
  font-size: 14px;
}
.record-content {
  flex: 1;
}
.record-tool {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.record-input {
  color: #666;
  font-size: 14px;
}
</style>
