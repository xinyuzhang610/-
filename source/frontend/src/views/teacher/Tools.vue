<template>
  <div class="tools-container">
    <div class="tools-header">
      <h2 class="page-title">我的工具</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        创建新工具
      </el-button>
    </div>

    <!-- 工具列表 -->
    <div class="tools-list">
      <div
        v-for="tool in tools"
        :key="tool.id"
        class="tool-card"
      >
        <div class="tool-icon">{{ tool.icon }}</div>
        <div class="tool-info">
          <h3 class="tool-name">{{ tool.name }}</h3>
          <div class="tool-meta">
            <el-tag size="small" :type="tool.category === '文科' ? 'primary' : 'success'">
              {{ tool.category }}
            </el-tag>
            <span class="tool-subject">{{ tool.subject }}</span>
            <span class="tool-date">创建于 {{ tool.createdAt }}</span>
          </div>
          <p class="tool-usage">使用次数：{{ tool.usageCount }}次</p>
        </div>
        <div class="tool-actions">
          <el-button size="small" @click="editTool(tool)">编辑</el-button>
          <el-button size="small" @click="shareTool(tool)">生成分享链接</el-button>
          <el-button size="small" @click="viewUsage(tool)">查看使用数据</el-button>
          <el-button size="small" type="danger" @click="deleteTool(tool)">删除</el-button>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="tools.length === 0" class="empty-state">
        <el-empty description="还没有创建任何工具">
          <el-button type="primary" @click="showCreateDialog = true">
            创建第一个工具
          </el-button>
        </el-empty>
      </div>
    </div>

    <!-- 创建工具对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建新工具"
      width="500px"
    >
      <div class="create-options">
        <div class="create-option" @click="startAICreate">
          <div class="option-icon">🤖</div>
          <h3 class="option-name">AI对话创建</h3>
          <p class="option-desc">直接告诉AI你的需求，系统自动生成工具配置</p>
        </div>

        <div class="create-option" @click="goToPlatform">
          <div class="option-icon">🔧</div>
          <h3 class="option-name">平台创建工作流</h3>
          <p class="option-desc">跳转到师大智能体平台，创建完成后返回本系统</p>
        </div>
      </div>
    </el-dialog>

    <!-- 分享对话框 -->
    <el-dialog
      v-model="showShareDialog"
      title="分享工具"
      width="400px"
    >
      <div class="share-content">
        <p class="share-label">分享链接：</p>
        <el-input
          v-model="shareLink"
          readonly
          class="share-input"
        >
          <template #append>
            <el-button @click="copyLink">复制</el-button>
          </template>
        </el-input>

        <div class="share-qr">
          <p class="share-label">二维码：</p>
          <div class="qr-placeholder">
            <span>二维码图片</span>
          </div>
          <el-button size="small" class="download-qr">下载二维码</el-button>
        </div>

        <div class="share-settings">
          <el-checkbox v-model="allowAnonymous">允许匿名使用</el-checkbox>
          <div class="expire-setting">
            <span>有效期：</span>
            <el-select v-model="expireType" size="small">
              <el-option label="永久" value="forever" />
              <el-option label="7天" value="7days" />
              <el-option label="30天" value="30days" />
            </el-select>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()

// 工具列表（模拟数据）
const tools = ref([
  {
    id: 1,
    name: '古诗词趣味赏析',
    icon: '🏮',
    category: '文科',
    subject: '语文',
    createdAt: '2026-07-15',
    usageCount: 23
  },
  {
    id: 2,
    name: '作文灵感助手',
    icon: '✍️',
    category: '文科',
    subject: '语文',
    createdAt: '2026-07-15',
    usageCount: 15
  },
  {
    id: 3,
    name: '公式推导助手',
    icon: '🧮',
    category: '理科',
    subject: '数学',
    createdAt: '2026-07-16',
    usageCount: 8
  }
])

// 对话框状态
const showCreateDialog = ref(false)
const showShareDialog = ref(false)

// 分享相关
const shareLink = ref('')
const allowAnonymous = ref(true)
const expireType = ref('forever')

// 编辑工具
const editTool = (tool) => {
  ElMessage.info(`编辑工具：${tool.name}`)
}

// 分享工具
const shareTool = (tool) => {
  shareLink.value = `http://localhost:3000/tool/${tool.id}`
  showShareDialog.value = true
}

// 复制链接
const copyLink = () => {
  navigator.clipboard.writeText(shareLink.value)
  ElMessage.success('链接已复制')
}

// 查看使用数据
const viewUsage = (tool) => {
  router.push('/teacher/dashboard')
}

// 删除工具
const deleteTool = (tool) => {
  ElMessageBox.confirm(
    `确定要删除工具"${tool.name}"吗？`,
    '确认删除',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    tools.value = tools.value.filter(t => t.id !== tool.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 开始AI创建
const startAICreate = () => {
  showCreateDialog.value = false
  router.push('/student/chat')
}

// 前往平台
const goToPlatform = () => {
  showCreateDialog.value = false
  ElMessage.info('即将跳转到师大智能体平台')
}
</script>

<style scoped>
.tools-container {
  max-width: 1000px;
  margin: 0 auto;
}

.tools-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
}

/* 工具列表 */
.tools-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tool-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s;
}

.tool-card:hover {
  box-shadow: var(--shadow-md);
}

.tool-icon {
  font-size: 40px;
  margin-right: 20px;
}

.tool-info {
  flex: 1;
}

.tool-name {
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.tool-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.tool-subject {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.tool-date {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.tool-usage {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.tool-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

/* 空状态 */
.empty-state {
  padding: 60px 0;
  background: white;
  border-radius: var(--radius-lg);
}

/* 创建选项 */
.create-options {
  display: flex;
  gap: 20px;
}

.create-option {
  flex: 1;
  padding: 24px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  text-align: center;
  transition: all 0.3s;
}

.create-option:hover {
  border-color: var(--color-ink);
  background: rgba(38, 37, 30, 0.05);
}

.option-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.option-name {
  font-family: var(--font-sans);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.option-desc {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

/* 分享内容 */
.share-content {
  padding: 10px 0;
}

.share-label {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.share-input {
  margin-bottom: 20px;
}

.share-qr {
  margin-bottom: 20px;
}

.qr-placeholder {
  width: 150px;
  height: 150px;
  background: var(--color-chip-bg);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.download-qr {
  margin-top: 8px;
}

.share-settings {
  padding-top: 16px;
  border-top: 1px solid var(--color-chip-bg);
}

.expire-setting {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink);
}
</style>
