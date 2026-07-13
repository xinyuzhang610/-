<template>
  <div class="tools-page"><header><div><span>TOOL CONSTELLATION</span><h1>我的工具</h1><p>管理预设工具、自己的课堂工具，以及外部智能体平台入口。</p></div><a v-if="platformUrl" class="platform-link" :href="platformUrl" target="_blank" rel="noopener">前往师大智能体平台 ↗</a><span v-else class="platform-link" aria-disabled="true">平台地址待配置</span></header>
    <StatusState v-if="loading" type="loading" title="正在读取工具库" />
    <StatusState v-else-if="errorMessage" type="error" title="工具库连接失败" :description="errorMessage" @retry="loadTools" />
    <StatusState v-else-if="!tools.length" type="empty" title="工具库还是空的" description="后端启动并写入预设工具后，它们会显示在这里。" />
    <div v-else class="tool-grid"><article v-for="tool in tools" :key="tool.id"><div class="tool-top"><span class="type-chip">{{ toolType(tool) }}</span><span>{{ tool.category || '通用' }}</span></div><h2>{{ tool.name }}</h2><p>{{ tool.description || '面向真实课堂场景的智能教学工具。' }}</p><dl><div><dt>学科</dt><dd>{{ tool.subject || '通用' }}</dd></div><div><dt>使用</dt><dd>{{ tool.usage_count || 0 }} 次</dd></div></dl><div class="actions"><RouterLink :to="`/tool/${tool.id}`">体验</RouterLink><button @click="share(tool)">分享</button><button v-if="!tool.is_preset" class="danger" @click="remove(tool)">删除</button></div></article></div>
    <p v-if="notice" class="notice" role="status">{{ notice }}</p>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import StatusState from '../../components/ui/StatusState.vue'
import { deleteTool, getPresetTools, getShareLink } from '../../api/tools'
const tools=ref([]),loading=ref(true),errorMessage=ref(''),notice=ref('')
const platformUrl=import.meta.env.VITE_AGENT_PLATFORM_URL||''
function toolType(t){return t.is_preset?'预设工具':t.external_url?'外部智能体':'我的工具'}
async function loadTools(){loading.value=true;errorMessage.value='';try{const {data}=await getPresetTools();tools.value=data.items||[]}catch(e){errorMessage.value=e.response?.data?.detail||'无法连接工具服务，请确认后端已启动。'}finally{loading.value=false}}
async function share(tool){notice.value='';try{const {data}=await getShareLink(tool.id);await navigator.clipboard?.writeText(data.share_url);notice.value='分享链接已复制。'}catch{notice.value='暂时无法生成分享链接。'}}
async function remove(tool){if(!window.confirm(`确定删除“${tool.name}”吗？`))return;try{await deleteTool(tool.id);tools.value=tools.value.filter(t=>t.id!==tool.id);notice.value='工具已删除。'}catch{notice.value='删除失败，请稍后重试。'}}
onMounted(loadTools)
</script>
<style scoped>
.tools-page{max-width:1180px;margin:auto}.tools-page>header{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:34px}.tools-page header span{color:var(--gold-300);font-size:.68rem;letter-spacing:.23em}.tools-page h1{margin:8px 0;font-family:var(--font-display);font-size:clamp(2.4rem,5vw,4.7rem);font-weight:500}.tools-page header p{color:var(--moon-300)}.platform-link{min-height:44px;padding:12px 18px;border:1px solid var(--gold-400);border-radius:var(--radius-full);color:var(--gold-300);text-decoration:none}.tool-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.tool-grid article{padding:24px;border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel-dark)}.tool-top{display:flex;justify-content:space-between;color:var(--moon-300);font-size:.72rem}.type-chip{color:var(--jade-400)!important}.tool-grid h2{margin:16px 0 8px;font-family:var(--font-display);font-size:1.7rem}.tool-grid p{min-height:3.2em;color:var(--moon-300);line-height:1.6}.tool-grid dl{display:flex;gap:24px;padding:16px 0;border-block:1px solid var(--color-border)}.tool-grid dl div{display:flex;gap:7px}.tool-grid dt{color:var(--moon-300)}.tool-grid dd{margin:0}.actions{display:flex;gap:10px;margin-top:16px}.actions a,.actions button{display:grid;place-items:center;min-height:44px;padding:0 15px;border:1px solid var(--color-border);border-radius:var(--radius-full);background:transparent;color:var(--moon-100);font:inherit;text-decoration:none;cursor:pointer}.actions .danger{color:#ffb7ad}.notice{position:fixed;right:24px;bottom:24px;padding:12px 18px;border:1px solid var(--jade-400);border-radius:var(--radius-md);background:var(--ink-900)}@media(max-width:760px){.tools-page>header{align-items:flex-start;flex-direction:column}.tool-grid{grid-template-columns:1fr}}
</style>
