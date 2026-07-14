<template>
  <div class="my-tools">
    <div class="header">
      <h2>我的工具</h2>
      <el-button type="primary" @click="showCreateDialog">+ 创建新工具</el-button>
    </div>
    <div class="tools-list">
      <el-card v-for="tool in tools" :key="tool.id" class="tool-card">
        <div class="tool-header">
          <span class="tool-icon">{{ tool.icon }}</span>
          <span class="tool-name">{{ tool.name }}</span>
        </div>
        <div class="tool-info">
          <el-tag :type="tool.category === '文科' ? 'success' : 'primary'" size="small">
            {{ tool.category }}
          </el-tag>
          <span class="tool-usage">使用次数: {{ tool.usage_count }}</span>
        </div>
        <div class="tool-actions">
          <el-button size="small" type="danger" @click="deleteTool(tool)">删除</el-button>
        </div>
      </el-card>
      <el-empty v-if="tools.length === 0" description="还没有工具，快去创建吧！" />
    </div>

    <el-dialog v-model="dialogVisible" title="创建工具" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="工具名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入工具名称" />
        </el-form-item>
        <el-form-item label="工具描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入工具描述" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-radio-group v-model="form.category">
            <el-radio value="文科">文科</el-radio>
            <el-radio value="理科">理科</el-radio>
            <el-radio value="通用">通用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学科" prop="subject">
          <el-input v-model="form.subject" placeholder="如：语文、数学" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="form.icon" placeholder="输入emoji图标" />
        </el-form-item>
        <el-form-item label="提示词模板" prop="prompt_template">
          <el-input v-model="form.prompt_template" type="textarea" :rows="4"
            placeholder="输入AI系统的提示词，如：你是一个古诗词赏析助手..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitTool" :loading="loading">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPresetTools, createTool, deleteTool as apiDeleteTool } from '@/api/tools'
import { ElMessage, ElMessageBox } from 'element-plus'

const tools = ref([])
const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref(null)

const form = ref({
  name: '',
  description: '',
  category: '文科',
  subject: '',
  icon: '🤖',
  prompt_template: ''
})

const rules = {
  name: [{ required: true, message: '请输入工具名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  prompt_template: [{ required: true, message: '请输入提示词模板', trigger: 'blur' }]
}

onMounted(async () => {
  await loadTools()
})

const loadTools = async () => {
  try {
    const { data } = await getPresetTools()
    tools.value = data.items
  } catch (error) {
    ElMessage.error('加载工具列表失败')
  }
}

const showCreateDialog = () => {
  form.value = {
    name: '',
    description: '',
    category: '文科',
    subject: '',
    icon: '🤖',
    prompt_template: ''
  }
  dialogVisible.value = true
}

const submitTool = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    await createTool(form.value)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    await loadTools()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '创建失败')
  } finally {
    loading.value = false
  }
}

const deleteTool = async (tool) => {
  try {
    await ElMessageBox.confirm('确定要删除这个工具吗？', '提示', { type: 'warning' })
    await apiDeleteTool(tool.id)
    ElMessage.success('删除成功')
    await loadTools()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.my-tools {
  max-width: 1000px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.tools-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
.tool-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.tool-icon {
  font-size: 24px;
  margin-right: 10px;
}
.tool-name {
  font-size: 16px;
  font-weight: bold;
}
.tool-info {
  margin-bottom: 15px;
}
.tool-usage {
  color: #666;
  font-size: 14px;
  margin-left: 10px;
}
.tool-actions {
  display: flex;
  gap: 10px;
}
</style>
