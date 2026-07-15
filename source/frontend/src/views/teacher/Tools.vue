<template>
  <main class="tools-page">
    <header class="page-head">
      <div>
        <span>TOOL CONSTELLATION</span>
        <h1>我的工具</h1>
        <p>把课堂意图变成可复用、可分享、可追踪的智能工具。</p>
      </div>
      <a v-if="platformUrl" class="platform-link" :href="platformUrl" target="_blank" rel="noopener">打开外部智能体平台</a>
    </header>

    <StatusState v-if="loading" type="loading" title="正在读取工具库" />
    <StatusState v-else-if="errorMessage" type="error" title="工具库连接失败" :description="errorMessage" @retry="loadTools" />
    <template v-else>
      <section class="studio" aria-labelledby="studio-title">
        <div class="studio__head"><div><span>CREATE / EDIT</span><h2 id="studio-title">{{ editingId ? '编辑工具' : '新建课堂工具' }}</h2></div><button v-if="editingId" class="text-button" type="button" @click="resetForm">取消编辑</button></div>
        <div class="template-row"><span>从模板开始</span><button v-for="template in templates" :key="template.id" type="button" @click="copyTemplate(template)">{{ template.name }}</button></div>
        <form @submit.prevent="saveTool">
          <label>工具名称<input v-model.trim="form.name" required maxlength="100" placeholder="例如：议论文结构教练"></label>
          <label>所属学科<input v-model.trim="form.subject" placeholder="例如：语文"></label>
          <label>分类<select v-model="form.category"><option value="文科">文科</option><option value="理科">理科</option><option value="通用">通用</option></select></label>
          <label>外部智能体平台地址<input v-model.trim="form.externalUrl" type="url" placeholder="https://..."></label>
          <label class="wide">工具说明<textarea v-model.trim="form.description" rows="2" placeholder="告诉学生，它可以协助完成什么。"></textarea></label>
          <label class="wide">系统提示词<textarea v-model.trim="form.prompt_template" required rows="5" placeholder="定义这个工具的角色、目标和输出方式。"></textarea></label>
          <div class="form-actions"><label class="check"><input v-model="form.is_public" type="checkbox">允许公开分享</label><button class="primary" type="submit" :disabled="saving">{{ saving ? '保存中…' : editingId ? '保存修改' : '创建工具' }}</button></div>
        </form>
      </section>

      <section class="collection" aria-labelledby="mine-title">
        <div class="section-head"><div><span>OWNED TOOLS</span><h2 id="mine-title">我创建的工具</h2></div><p>{{ myTools.length }} 个工具</p></div>
        <StatusState v-if="!myTools.length" type="empty" title="还没有自己的工具" description="从上方模板复制，或从一段清晰的课堂提示词开始。" />
        <div v-else class="tool-grid">
          <article v-for="tool in myTools" :key="tool.id" class="tool-card">
            <div class="tool-card__meta"><span>{{ tool.category }}</span><span>{{ tool.is_public ? '可分享' : '已撤销公开' }}</span></div>
            <h3>{{ tool.name }}</h3><p>{{ tool.description || '尚未添加工具说明。' }}</p>
            <div class="metrics"><span>{{ tool.subject || '通用学科' }}</span><span>{{ tool.usage_count || 0 }} 次使用</span></div>
            <div class="actions"><RouterLink :to="`/tool/${tool.id}`">体验</RouterLink><button type="button" @click="editTool(tool)">编辑</button><button type="button" @click="share(tool)">分享</button><button v-if="tool.is_public" type="button" @click="revoke(tool)">撤销公开</button><button class="danger" type="button" @click="remove(tool)">删除</button></div>
          </article>
        </div>
      </section>

      <section class="collection presets" aria-labelledby="presets-title">
        <div class="section-head"><div><span>PRESET LIBRARY</span><h2 id="presets-title">预设工具</h2></div><p>可复制为你的课堂版本</p></div>
        <div class="tool-grid">
          <article v-for="tool in presets" :key="tool.id" class="tool-card tool-card--quiet"><div class="tool-card__meta"><span>{{ tool.category }}</span><span>预设</span></div><h3>{{ tool.name }}</h3><p>{{ tool.description || '面向真实课堂场景的智能工具。' }}</p><div class="actions"><button type="button" @click="copyTemplate(tool)">复制为新工具</button><RouterLink :to="`/tool/${tool.id}`">体验</RouterLink></div></article>
        </div>
      </section>
    </template>

    <div v-if="shareInfo" class="share-modal" role="dialog" aria-modal="true" aria-labelledby="share-title" @click.self="shareInfo = null"><section><button class="close" type="button" aria-label="关闭" @click="shareInfo = null">×</button><span>SHARE LINK</span><h2 id="share-title">邀请学生使用</h2><img :src="qrImage" alt="工具分享二维码"><input :value="shareInfo.share_url" readonly @focus="$event.target.select()"><button class="primary" type="button" @click="copyShare">复制分享链接</button></section></div>
    <p v-if="notice" class="notice" role="status">{{ notice }}</p>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import QRCode from 'qrcode'
import StatusState from '../../components/ui/StatusState.vue'
import { createTool, deleteTool, getMyTools, getPresetTools, getShareLink, getTemplates, revokeShare, updateTool } from '../../api/tools'
import { useDemoMode } from '../../composables/useDemoMode'

const presets = ref([]), myTools = ref([]), templates = ref([]), loading = ref(true), saving = ref(false), errorMessage = ref(''), notice = ref(''), editingId = ref(null), shareInfo = ref(null)
const platformUrl = import.meta.env.VITE_AGENT_PLATFORM_URL || ''
const { enabled: demoEnabled, getDemoData } = useDemoMode()
const emptyForm = () => ({ name: '', description: '', category: '通用', subject: '', prompt_template: '', externalUrl: '', is_public: true })
const form = reactive(emptyForm())
const qrImage = ref('')
watch(shareInfo, async (share) => { qrImage.value = share ? await QRCode.toDataURL(share.share_url, { width: 220, margin: 1 }) : '' })

function resetForm() { Object.assign(form, emptyForm()); editingId.value = null }
function normalizeTool(tool) { return { ...tool, externalUrl: tool.interface_config?.external_url || '' } }
async function loadTools() {
  loading.value = true; errorMessage.value = ''
  try {
    if (demoEnabled.value) { presets.value = getDemoData('tools').items; myTools.value = []; templates.value = []; return }
    const [presetResponse, mineResponse, templateResponse] = await Promise.all([getPresetTools(), getMyTools(), getTemplates()])
    presets.value = presetResponse.data.items || []
    myTools.value = (mineResponse.data.items || []).map(normalizeTool)
    templates.value = templateResponse.data || []
  } catch (error) { errorMessage.value = error.response?.data?.detail || '无法连接工具服务，请确认已使用教师账号登录。' }
  finally { loading.value = false }
}
function copyTemplate(template) {
  Object.assign(form, { name: `${template.name}（副本）`, description: template.description || '', category: template.category || '通用', subject: template.subject || '', prompt_template: template.prompt_template || '', externalUrl: template.default_config?.external_url || template.interface_config?.external_url || '', is_public: true })
  editingId.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
function editTool(tool) { Object.assign(form, normalizeTool(tool)); editingId.value = tool.id; window.scrollTo({ top: 0, behavior: 'smooth' }) }
function payload() { return { name: form.name, description: form.description || null, category: form.category, subject: form.subject || null, prompt_template: form.prompt_template, interface_config: form.externalUrl ? { external_url: form.externalUrl } : null, is_public: form.is_public } }
async function saveTool() {
  saving.value = true; notice.value = ''
  try {
    if (editingId.value) await updateTool(editingId.value, payload()); else await createTool(payload())
    notice.value = editingId.value ? '工具已更新。' : '工具已创建。'
    resetForm(); await loadTools()
  } catch (error) { notice.value = error.response?.data?.detail || '保存失败，请检查必填信息后重试。' }
  finally { saving.value = false }
}
async function share(tool) { try { shareInfo.value = (await getShareLink(tool.id)).data } catch (error) { notice.value = error.response?.data?.detail || '暂时无法生成分享链接。' } }
async function copyShare() { try { await navigator.clipboard.writeText(shareInfo.value.share_url); notice.value = '分享链接已复制。' } catch { notice.value = '复制失败，请手动复制链接。' } }
async function revoke(tool) { if (!window.confirm(`确认撤销“${tool.name}”的公开分享吗？`)) return; try { await revokeShare(tool.id); notice.value = '公开分享已撤销。'; await loadTools() } catch (error) { notice.value = error.response?.data?.detail || '撤销失败。' } }
async function remove(tool) { if (!window.confirm(`确认删除“${tool.name}”吗？`)) return; try { await deleteTool(tool.id); notice.value = '工具已删除。'; await loadTools() } catch (error) { notice.value = error.response?.data?.detail || '删除失败。' } }
onMounted(loadTools)
</script>

<style scoped>
.tools-page{max-width:1180px;margin:auto;padding:clamp(24px,4vw,52px) 0 80px}.page-head,.section-head,.studio__head{display:flex;justify-content:space-between;gap:24px}.page-head{align-items:end;margin-bottom:34px}.page-head span,.section-head span,.studio__head span{color:var(--gold-300);font-size:.68rem;letter-spacing:.23em}.page-head h1{margin:8px 0;font:500 clamp(2.4rem,5vw,4.7rem) var(--font-display)}.page-head p{color:var(--moon-300)}.platform-link,.primary{min-height:44px;padding:12px 18px;border:1px solid var(--gold-400);border-radius:var(--radius-full);background:var(--gold-400);color:var(--ink-950);font:inherit;font-weight:700;text-decoration:none;cursor:pointer}.studio,.collection{padding:clamp(20px,3vw,34px);border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel-dark)}.studio{margin-bottom:30px}.studio h2,.section-head h2{margin:7px 0;font:500 1.75rem var(--font-heading)}.text-button{border:0;background:transparent;color:var(--gold-300);font:inherit;cursor:pointer}.template-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:23px 0}.template-row span{color:var(--moon-300);font-size:.82rem}.template-row button,.actions button,.actions a{min-height:38px;padding:0 11px;border:1px solid var(--color-border);border-radius:var(--radius-full);background:transparent;color:var(--moon-100);font:inherit;text-decoration:none;cursor:pointer}.studio form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.studio label{display:grid;gap:7px;color:var(--moon-300);font-size:.8rem}.studio input,.studio select,.studio textarea,.share-modal input{width:100%;border:1px solid var(--color-border);border-radius:10px;background:rgb(255 255 255 / 4%);color:var(--moon-50);font:inherit}.studio input,.studio select{min-height:44px;padding:0 12px}.studio textarea{padding:11px 12px;resize:vertical}.wide{grid-column:1/-1}.form-actions{display:flex;grid-column:1/-1;align-items:center;justify-content:space-between;gap:16px}.check{display:flex!important;grid-auto-flow:column;justify-content:start;align-items:center}.check input{width:auto}.collection{margin-top:22px}.section-head{align-items:end;margin-bottom:20px}.section-head p{color:var(--moon-300)}.tool-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.tool-card{padding:22px;border:1px solid rgb(203 211 201 / 14%);border-radius:18px;background:rgb(255 255 255 / 3%)}.tool-card--quiet{background:transparent}.tool-card__meta,.metrics,.actions{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px}.tool-card__meta,.metrics{color:var(--moon-300);font-size:.75rem}.tool-card__meta span:first-child{color:var(--jade-200)}.tool-card h3{margin:15px 0 8px;font:500 1.45rem var(--font-heading)}.tool-card p{min-height:3.2em;color:var(--moon-300);line-height:1.6}.metrics{padding:14px 0;border-block:1px solid rgb(203 211 201 / 12%)}.actions{justify-content:flex-start;margin-top:15px}.actions .danger{color:#ffb7ad}.presets{margin-top:22px}.share-modal{position:fixed;z-index:20;inset:0;display:grid;place-items:center;padding:24px;background:rgb(4 10 8 / 74%);backdrop-filter:blur(12px)}.share-modal section{position:relative;width:min(100%,430px);padding:32px;border:1px solid var(--gold-400);border-radius:24px;background:var(--ink-900);text-align:center}.share-modal h2{margin:10px 0 18px;font:500 2rem var(--font-heading)}.share-modal img{display:block;width:220px;height:220px;margin:0 auto 20px;border-radius:12px;background:#fff}.share-modal input{min-height:44px;margin-bottom:12px;padding:0 11px;color:var(--moon-100)}.close{position:absolute;right:12px;top:8px;border:0;background:transparent;color:var(--moon-100);font-size:2rem;cursor:pointer}.notice{position:fixed;z-index:30;right:24px;bottom:24px;padding:12px 18px;border:1px solid var(--jade-400);border-radius:var(--radius-md);background:var(--ink-900)}@media(max-width:760px){.tools-page{padding-inline:16px}.page-head,.section-head{align-items:flex-start;flex-direction:column}.studio form,.tool-grid{grid-template-columns:1fr}.studio label,.wide,.form-actions{grid-column:auto}.form-actions{align-items:flex-start;flex-direction:column}.page-head{margin-top:12px}}
</style>
