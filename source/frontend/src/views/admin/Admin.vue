<script setup>
import { onMounted, reactive, ref } from 'vue'
import { getAdminUsers, updateAdminUser, setAdminToolPlazaStatus, getRecommendRules, createRecommendRule, updateRecommendRule, deleteRecommendRule, getAuditLogs, exportAuditLogs } from '../../api/admin'
import { getMyTools, restoreTool } from '../../api/tools'
import StatusState from '../../components/ui/StatusState.vue'

const tab = ref('users')
const loading = ref(true)
const error = ref('')
const notice = ref('')
const users = ref([])
const tools = ref([])
const rules = ref([])
const logs = ref([])
const ruleEditingId = ref(null)
const ruleForm = reactive({ subject: '', category: '', need_type: '', tool_ids: '', priority: 0, is_active: true })

function flash(message) { notice.value = message; window.setTimeout(() => { notice.value = '' }, 3200) }
function showError(cause, fallback) { error.value = cause?.response?.data?.detail || fallback }
async function loadUsers() { const { data } = await getAdminUsers({ page: 1, page_size: 100 }); users.value = data.items || [] }
async function loadTools() { const { data } = await getMyTools({ include_deleted: true, page: 1, page_size: 100 }); tools.value = data.items || [] }
async function loadRules() { const { data } = await getRecommendRules(); rules.value = data || [] }
async function loadLogs() { const { data } = await getAuditLogs({ page: 1, page_size: 100 }); logs.value = data.items || [] }
async function load() {
  loading.value = true; error.value = ''
  try {
    if (tab.value === 'users') await loadUsers()
    if (tab.value === 'tools') await loadTools()
    if (tab.value === 'rules') await loadRules()
    if (tab.value === 'audit') await loadLogs()
  } catch (cause) { showError(cause, '后台数据暂时无法读取。') }
  finally { loading.value = false }
}
async function switchTab(value) { tab.value = value; await load() }
async function toggleUser(user) {
  try { await updateAdminUser(user.id, { is_active: !user.is_active }); flash(user.is_active ? '账号已禁用。' : '账号已启用。'); await loadUsers() }
  catch (cause) { showError(cause, '账号状态更新失败。') }
}
async function changeRole(user, event) {
  try { await updateAdminUser(user.id, { role: event.target.value }); flash('用户角色已更新。'); await loadUsers() }
  catch (cause) { showError(cause, '角色更新失败。'); await loadUsers() }
}
async function updatePlaza(tool, status) {
  try { await setAdminToolPlazaStatus(tool.id, status); flash('工具广场状态已更新。'); await loadTools() }
  catch (cause) { showError(cause, '广场状态更新失败。') }
}
async function restore(tool) {
  try { await restoreTool(tool.id); flash('工具已恢复。'); await loadTools() }
  catch (cause) { showError(cause, '工具恢复失败。') }
}
function resetRule() { Object.assign(ruleForm, { subject: '', category: '', need_type: '', tool_ids: '', priority: 0, is_active: true }); ruleEditingId.value = null }
function editRule(rule) { Object.assign(ruleForm, { ...rule, tool_ids: (rule.tool_ids || []).join(',') }); ruleEditingId.value = rule.id }
async function saveRule() {
  const payload = { subject: ruleForm.subject || null, category: ruleForm.category || null, need_type: ruleForm.need_type || null, tool_ids: ruleForm.tool_ids.split(',').map(item => Number(item.trim())).filter(Number.isInteger), priority: Number(ruleForm.priority) || 0, is_active: ruleForm.is_active }
  try { if (ruleEditingId.value) await updateRecommendRule(ruleEditingId.value, payload); else await createRecommendRule(payload); flash(ruleEditingId.value ? '推荐规则已更新。' : '推荐规则已创建。'); resetRule(); await loadRules() }
  catch (cause) { showError(cause, '推荐规则保存失败。') }
}
async function removeRule(rule) {
  if (!window.confirm(`确认删除规则 #${rule.id} 吗？`)) return
  try { await deleteRecommendRule(rule.id); flash('推荐规则已删除。'); await loadRules() }
  catch (cause) { showError(cause, '推荐规则删除失败。') }
}
async function download(responsePromise, filename) {
  const response = await responsePromise
  const url = window.URL.createObjectURL(response.data)
  const link = document.createElement('a'); link.href = url; link.download = filename; link.click(); window.URL.revokeObjectURL(url)
}
async function downloadAudit() { try { await download(exportAuditLogs(), 'audit-logs.csv') } catch (cause) { showError(cause, '审计日志导出失败。') } }
onMounted(load)
</script>

<template>
  <main class="admin-page">
    <header class="admin-head"><div><span>OPERATIONS CONTROL</span><h1>运营后台</h1><p>管理账号、工具发布、推荐规则与审计记录。</p></div><button type="button" @click="load">刷新数据</button></header>
    <nav class="admin-tabs" aria-label="后台模块"><button v-for="item in [{id:'users',label:'用户管理'},{id:'tools',label:'工具管理'},{id:'rules',label:'推荐规则'},{id:'audit',label:'审计日志'}]" :key="item.id" type="button" :aria-pressed="tab === item.id" @click="switchTab(item.id)">{{ item.label }}</button></nav>
    <StatusState v-if="loading" type="loading" title="正在读取运营数据" />
    <StatusState v-else-if="error" type="error" title="后台读取失败" :description="error" @retry="load" />
    <section v-else class="admin-panel">
      <template v-if="tab === 'users'"><div class="panel-title"><h2>用户管理</h2><span>{{ users.length }} 个账号</span></div><div class="table-wrap"><table><thead><tr><th>账号</th><th>姓名</th><th>角色</th><th>状态</th><th>操作</th></tr></thead><tbody><tr v-for="user in users" :key="user.id"><td>{{ user.username }}</td><td>{{ user.name || '未填写' }}</td><td><select :value="user.role" @change="changeRole(user, $event)"><option value="teacher">教师</option><option value="student">学生</option><option value="admin">管理员</option></select></td><td>{{ user.is_active ? '启用' : '禁用' }}</td><td><button type="button" @click="toggleUser(user)">{{ user.is_active ? '禁用' : '启用' }}</button></td></tr></tbody></table></div></template>
      <template v-else-if="tab === 'tools'"><div class="panel-title"><h2>工具管理</h2><span>含软删除记录</span></div><div class="table-wrap"><table><thead><tr><th>工具</th><th>分类</th><th>创建者</th><th>广场状态</th><th>生命周期</th><th>操作</th></tr></thead><tbody><tr v-for="tool in tools" :key="tool.id"><td>{{ tool.name }}</td><td>{{ tool.category }}</td><td>{{ tool.creator_id || '预设' }}</td><td><select :value="tool.plaza_status" :disabled="Boolean(tool.deleted_at)" @change="updatePlaza(tool, $event.target.value)"><option value="published">已发布</option><option value="unlisted">未公开</option></select></td><td>{{ tool.deleted_at ? '已删除' : '正常' }}</td><td><button v-if="tool.deleted_at" type="button" @click="restore(tool)">恢复</button></td></tr></tbody></table></div></template>
      <template v-else-if="tab === 'rules'"><div class="panel-title"><h2>推荐规则</h2><span>规则匹配，不调用 AI</span></div><form class="rule-form" @submit.prevent="saveRule"><input v-model.trim="ruleForm.subject" placeholder="学科，如语文"><input v-model.trim="ruleForm.category" placeholder="分类，如文科"><input v-model.trim="ruleForm.need_type" placeholder="需求类型"><input v-model.trim="ruleForm.tool_ids" placeholder="工具 ID，逗号分隔"><input v-model.number="ruleForm.priority" type="number" placeholder="优先级"><label><input v-model="ruleForm.is_active" type="checkbox">启用</label><button type="submit">{{ ruleEditingId ? '保存修改' : '创建规则' }}</button><button v-if="ruleEditingId" type="button" @click="resetRule">取消</button></form><div class="table-wrap"><table><thead><tr><th>ID</th><th>条件</th><th>工具 ID</th><th>优先级</th><th>状态</th><th>操作</th></tr></thead><tbody><tr v-for="rule in rules" :key="rule.id"><td>{{ rule.id }}</td><td>{{ rule.subject || '全部' }} / {{ rule.category || '全部' }} / {{ rule.need_type || '全部' }}</td><td>{{ (rule.tool_ids || []).join(', ') }}</td><td>{{ rule.priority }}</td><td>{{ rule.is_active ? '启用' : '停用' }}</td><td><button type="button" @click="editRule(rule)">编辑</button><button type="button" @click="removeRule(rule)">删除</button></td></tr></tbody></table></div></template>
      <template v-else><div class="panel-title"><h2>审计日志</h2><button type="button" @click="downloadAudit">导出 CSV</button></div><div class="table-wrap"><table><thead><tr><th>时间</th><th>操作者</th><th>动作</th><th>资源</th><th>结果</th></tr></thead><tbody><tr v-for="log in logs" :key="log.id"><td>{{ log.created_at ? new Date(log.created_at).toLocaleString('zh-CN') : '-' }}</td><td>{{ log.actor_id || '系统/访客' }}</td><td>{{ log.action }}</td><td>{{ log.resource_type }} #{{ log.resource_id || '-' }}</td><td>{{ log.result }}</td></tr></tbody></table></div></template>
    </section>
    <p v-if="notice" class="notice" role="status">{{ notice }}</p>
  </main>
</template>

<style scoped>
.admin-page{max-width:1240px;margin:auto}.admin-head,.panel-title{display:flex;align-items:end;justify-content:space-between;gap:20px}.admin-head{margin-bottom:30px}.admin-head span{color:var(--gold-300);font-size:.68rem;letter-spacing:.23em}.admin-head h1{margin:10px 0;font:500 clamp(2.4rem,5vw,4.5rem) var(--font-display)}.admin-head p,.panel-title span{color:var(--moon-300)}.admin-head button,.admin-tabs button,.panel-title button,.table-wrap button,.rule-form button{min-height:40px;padding:0 14px;border:1px solid var(--color-border);border-radius:999px;background:transparent;color:var(--moon-50);font:inherit;cursor:pointer}.admin-head button,.panel-title button,.rule-form button[type=submit]{border-color:var(--gold-400);background:var(--gold-400);color:var(--ink-950);font-weight:700}.admin-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}.admin-tabs button[aria-pressed=true]{border-color:var(--jade-400);background:rgb(66 185 154 / 12%)}.admin-panel{padding:clamp(20px,3vw,34px);border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel-dark)}.panel-title{align-items:center;margin-bottom:20px}.panel-title h2{margin:0;font:500 1.6rem var(--font-heading)}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;min-width:720px}th,td{padding:13px 12px;border-top:1px solid var(--color-border);text-align:left;white-space:nowrap}th{color:var(--gold-300);font-size:.76rem;font-weight:600}td{color:var(--moon-200);font-size:.84rem}td select,.rule-form input{min-height:36px;padding:0 9px;border:1px solid var(--color-border);border-radius:8px;background:rgb(255 255 255 / 5%);color:var(--moon-50);font:inherit}td select option{color:#111}.table-wrap button{min-height:32px;padding:0 9px;margin-right:6px;font-size:.75rem}.rule-form{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:24px}.rule-form input{min-width:0}.rule-form label{display:flex;align-items:center;gap:6px;color:var(--moon-200);font-size:.82rem}.rule-form label input{min-height:auto}.rule-form button{min-height:36px;padding:0 10px}.notice{position:fixed;right:24px;bottom:24px;padding:12px 18px;border:1px solid var(--jade-400);border-radius:10px;background:var(--ink-900)}@media(max-width:900px){.rule-form{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.admin-head,.panel-title{align-items:flex-start;flex-direction:column}.rule-form{grid-template-columns:1fr}}
</style>
