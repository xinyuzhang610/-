<template>
  <div class="plaza-container">
    <!-- 搜索栏 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索工具..."
        size="large"
        class="search-input"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 文科专区 -->
    <div class="category-section">
      <h2 class="section-title">📚 文科专区</h2>
      <div class="tool-grid">
        <transition-group name="stagger" tag="div" class="tool-grid-inner"
                          @before-enter="beforeEnter" @enter="enter">
          <div
            v-for="(tool, index) in liberalArtsTools"
            :key="tool.id"
            class="tool-card"
            :data-index="index"
            @click="useTool(tool)"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <h3 class="tool-name">{{ tool.name }}</h3>
            <p class="tool-subject">{{ tool.subject }} · 文科</p>
            <el-button type="primary" size="small" class="use-btn">立即使用</el-button>
          </div>
        </transition-group>
      </div>
    </div>

    <!-- 理科专区 -->
    <div class="category-section">
      <h2 class="section-title">🔬 理科专区</h2>
      <div class="tool-grid">
        <transition-group name="stagger" tag="div" class="tool-grid-inner"
                          @before-enter="beforeEnter" @enter="enter">
          <div
            v-for="(tool, index) in scienceTools"
            :key="tool.id"
            class="tool-card"
            :data-index="index"
            @click="useTool(tool)"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <h3 class="tool-name">{{ tool.name }}</h3>
            <p class="tool-subject">{{ tool.subject }} · 理科</p>
            <el-button type="primary" size="small" class="use-btn">立即使用</el-button>
          </div>
        </transition-group>
      </div>
    </div>

    <!-- 热门推荐 -->
    <div class="category-section">
      <h2 class="section-title">🔥 热门推荐</h2>
      <div class="hot-list">
        <div
          v-for="(tool, index) in hotTools"
          :key="tool.id"
          class="hot-item"
          @click="useTool(tool)"
        >
          <span class="hot-number" :class="{ top: index < 3 }">{{ index + 1 }}</span>
          <span class="hot-icon">{{ tool.icon }}</span>
          <span class="hot-name">{{ tool.name }}</span>
          <span class="hot-count">本周使用 {{ tool.weeklyUsage }} 次</span>
        </div>
      </div>
    </div>

    <!-- 底部提示 -->
    <div class="more-section">
      <h2 class="section-title">🛠️ 想要更多工具？</h2>
      <p class="more-desc">你可以：</p>
      <div class="more-actions">
        <p>· 告诉老师你的需求，让老师为你创建工具</p>
        <el-button type="primary" @click="goToPlatform">去智能体平台自己搭建 →</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const searchQuery = ref('')

// 文科工具
const liberalArtsTools = ref([
  { id: 1, name: '古诗词赏析', icon: '🏮', subject: '语文' },
  { id: 2, name: '作文辅助', icon: '✍️', subject: '语文' },
  { id: 3, name: '阅读理解', icon: '📖', subject: '语文' },
  { id: 4, name: '名词解释', icon: '📝', subject: '历史' },
  { id: 5, name: '英语单词卡片', icon: '🔤', subject: '英语' },
  { id: 6, name: '诗词飞花令', icon: '🌸', subject: '语文' }
])

// 理科工具
const scienceTools = ref([
  { id: 7, name: '公式推导', icon: '🧮', subject: '数学' },
  { id: 8, name: '实验模拟', icon: '🔬', subject: '物理' },
  { id: 9, name: '逻辑训练', icon: '🧠', subject: '数学' },
  { id: 10, name: '错题分析', icon: '❌', subject: '数学' },
  { id: 11, name: '概念辨析', icon: '💡', subject: '物理' },
  { id: 12, name: '数据分析', icon: '📊', subject: '数学' }
])

// 热门工具
const hotTools = ref([
  { id: 1, name: '古诗词赏析', icon: '🏮', weeklyUsage: 156 },
  { id: 7, name: '公式推导', icon: '🧮', weeklyUsage: 89 },
  { id: 2, name: '作文辅助', icon: '✍️', weeklyUsage: 67 },
  { id: 8, name: '实验模拟', icon: '🔬', weeklyUsage: 45 },
  { id: 9, name: '逻辑训练', icon: '🧠', weeklyUsage: 38 }
])

// 搜索
const handleSearch = () => {
  if (searchQuery.value) {
    ElMessage.info(`搜索：${searchQuery.value}`)
  }
}

// 使用工具
const useTool = (tool) => {
  router.push(`/tool/${tool.id}`)
}

// 前往平台
const goToPlatform = () => {
  ElMessage.info('即将跳转到师大智能体平台')
}

// Stagger动画
const beforeEnter = (el) => {
  el.style.opacity = 0
  el.style.transform = 'translateY(16px)'
}

const enter = (el, done) => {
  const delay = el.dataset.index * 50
  setTimeout(() => {
    el.style.transition = 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
    el.style.opacity = 1
    el.style.transform = 'translateY(0)'
    done()
  }, delay)
}
</script>

<style scoped>
.plaza-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 搜索栏 */
.search-section {
  margin-bottom: 32px;
}

.search-input {
  max-width: 600px;
  margin: 0 auto;
  display: block;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: 0 0 0 1px var(--color-border) inset;
}

.search-input :deep(.el-input-group__append) {
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  background: var(--color-ink);
  border-color: var(--color-ink);
}

.search-input :deep(.el-input-group__append .el-button) {
  color: white;
}

/* 分类区域 */
.category-section {
  margin-bottom: 40px;
}

.section-title {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 20px;
}

/* 工具网格 */
.tool-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.tool-grid-inner {
  display: contents;
}

.tool-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow-sm);
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.tool-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.tool-name {
  font-family: var(--font-title);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 4px;
}

.tool-subject {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-ink-soft);
  margin-bottom: 12px;
}

.use-btn {
  width: 100%;
}

/* 热门列表 */
.hot-list {
  background: white;
  border-radius: var(--radius-lg);
  padding: 16px 24px;
  box-shadow: var(--shadow-sm);
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-chip-bg);
  cursor: pointer;
  transition: background 0.3s;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  background: var(--color-chip-bg);
  border-radius: var(--radius-md);
}

.hot-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-ui);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-soft);
  background: var(--color-chip-bg);
  border-radius: 50%;
}

.hot-number.top {
  background: var(--color-ink);
  color: white;
}

.hot-icon {
  font-size: 24px;
}

.hot-name {
  flex: 1;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--color-ink);
}

.hot-count {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 底部更多 */
.more-section {
  background: white;
  border-radius: var(--radius-lg);
  padding: 32px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.more-desc {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
  margin-bottom: 16px;
}

.more-actions {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.more-actions p {
  margin-bottom: 16px;
}
</style>
