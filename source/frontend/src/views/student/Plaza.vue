<template>
  <div class="plaza">
    <div class="search-bar">
      <el-input v-model="searchKeyword" placeholder="搜索工具..." @input="handleSearch" clearable />
    </div>

    <div class="category-tabs">
      <el-radio-group v-model="selectedCategory" @change="loadTools">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button v-for="cat in categories" :key="cat.value" :value="cat.value">
          {{ cat.icon }} {{ cat.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <div class="tools-grid">
      <el-card v-for="tool in tools" :key="tool.id" class="tool-card" @click="useTool(tool)">
        <div class="tool-icon">{{ tool.icon }}</div>
        <div class="tool-name">{{ tool.name }}</div>
        <div class="tool-desc">{{ tool.description }}</div>
        <div class="tool-meta">
          <el-tag :type="tool.category === '文科' ? 'success' : 'primary'" size="small">
            {{ tool.category }}
          </el-tag>
          <span class="usage-count">{{ tool.usage_count }}次使用</span>
        </div>
      </el-card>
    </div>

    <el-empty v-if="tools.length === 0" description="暂无工具" />

    <el-card class="hot-section" v-if="hotTools.length > 0">
      <template #header>
        <span>热门推荐</span>
      </template>
      <div class="hot-list">
        <div v-for="(tool, index) in hotTools" :key="tool.id" class="hot-item" @click="useTool(tool)">
          <span class="hot-rank">{{ index + 1 }}</span>
          <span class="hot-icon">{{ tool.icon }}</span>
          <span class="hot-name">{{ tool.name }}</span>
          <span class="hot-count">{{ tool.usage_count }}次</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPlaza, getHotTools } from '@/api/plaza'
import { ElMessage } from 'element-plus'

const router = useRouter()
const tools = ref([])
const hotTools = ref([])
const categories = ref([])
const selectedCategory = ref('')
const searchKeyword = ref('')

onMounted(async () => {
  await loadCategories()
  await loadTools()
  await loadHotTools()
})

const loadCategories = async () => {
  try {
    const { data } = await getPlaza()
    categories.value = data.categories
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const loadTools = async () => {
  try {
    const { data } = await getPlaza(selectedCategory.value, searchKeyword.value)
    tools.value = data.tools
  } catch (error) {
    ElMessage.error('加载工具失败')
  }
}

const loadHotTools = async () => {
  try {
    const { data } = await getHotTools(5)
    hotTools.value = data
  } catch (error) {
    ElMessage.error('加载热门工具失败')
  }
}

const handleSearch = () => {
  loadTools()
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.id}`)
}
</script>

<style scoped>
.plaza {
  max-width: 1200px;
  margin: 0 auto;
}
.search-bar {
  margin-bottom: 20px;
}
.category-tabs {
  margin-bottom: 20px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}
.tool-card {
  cursor: pointer;
  transition: all 0.3s;
}
.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.tool-icon {
  font-size: 48px;
  text-align: center;
  margin-bottom: 15px;
}
.tool-name {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}
.tool-desc {
  color: #666;
  font-size: 14px;
  text-align: center;
  margin-bottom: 15px;
}
.tool-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.usage-count {
  color: #999;
  font-size: 12px;
}
.hot-section {
  margin-bottom: 20px;
}
.hot-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.hot-item:hover {
  background: #f5f7fa;
}
.hot-rank {
  width: 24px;
  height: 24px;
  background: #409eff;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 12px;
}
.hot-item:nth-child(1) .hot-rank {
  background: #f56c6c;
}
.hot-item:nth-child(2) .hot-rank {
  background: #e6a23c;
}
.hot-item:nth-child(3) .hot-rank {
  background: #67c23a;
}
.hot-icon {
  font-size: 20px;
  margin-right: 10px;
}
.hot-name {
  flex: 1;
}
.hot-count {
  color: #666;
  font-size: 14px;
}
</style>
