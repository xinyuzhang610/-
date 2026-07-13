<template>
  <div class="teacher-guidance">
    <header class="page-hero"><span>NEED DISCOVERY</span><h1>把教学难题，变成清晰的工具路径</h1><p>三步完成需求定位。推荐来自规则与真实工具库，不把简单匹配包装成 AI。</p></header>
    <div class="guidance-map">
      <GuidanceStep :step="1" title="选择学科领域" :status="stepStatus(1)"><div class="choice-grid"><button v-for="item in categories" :key="item.value" :aria-pressed="category===item.value" @click="chooseCategory(item.value)"><strong>{{ item.label }}</strong><small>{{ item.desc }}</small></button></div></GuidanceStep>
      <GuidanceStep :step="2" title="明确教学目标" :status="stepStatus(2)"><div class="choice-grid goals"><button v-for="item in goals" :key="item.value" :disabled="!category" :aria-pressed="goal===item.value" @click="chooseGoal(item.value)"><strong>{{ item.label }}</strong><small>{{ item.desc }}</small></button></div></GuidanceStep>
      <GuidanceStep :step="3" title="获得工具推荐" :status="stepStatus(3)">
        <StatusState v-if="loading" type="loading" title="正在连接工具知识库" description="根据你的学科和目标筛选现有工具。" />
        <StatusState v-else-if="errorMessage" type="error" title="推荐暂时不可用" :description="errorMessage" @retry="loadRecommendations" />
        <StatusState v-else-if="goal && !tools.length" type="empty" title="暂未找到匹配工具" description="可以更换教学目标，或前往工具广场继续探索。" />
        <div v-else-if="tools.length" class="recommendations"><article v-for="tool in tools" :key="tool.id"><span>{{ tool.subject || category }}</span><h3>{{ tool.name }}</h3><p>{{ tool.description || '基于当前教学目标匹配的课堂工具。' }}</p><RouterLink :to="`/tool/${tool.id}`">立即体验</RouterLink></article></div>
        <p v-else class="waiting-copy">完成前两步后，匹配结果将在这里展开。</p>
      </GuidanceStep>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import GuidanceStep from '../../components/teacher/GuidanceStep.vue'
import StatusState from '../../components/ui/StatusState.vue'
import { getRecommendation } from '../../api/recommend'
const categories=[{value:'文科',label:'人文与表达',desc:'语文 / 英语 / 历史 / 政治 / 地理'},{value:'理科',label:'科学与推演',desc:'数学 / 物理 / 化学 / 生物 / 信息技术'}]
const goals=[{value:'课前备课',label:'课前备课',desc:'组织资料与课堂结构'},{value:'课堂教学',label:'课堂互动',desc:'提问、演示与实时参与'},{value:'课后辅导',label:'课后辅导',desc:'答疑与个性化支持'},{value:'兴趣激发',label:'兴趣激发',desc:'让知识变得可探索'}]
const category=ref(''),goal=ref(''),tools=ref([]),loading=ref(false),errorMessage=ref('')
function stepStatus(n){if(n===1)return category.value?'complete':'active';if(n===2)return !category.value?'pending':goal.value?'complete':'active';return goal.value?'active':'pending'}
function chooseCategory(value){category.value=value;goal.value='';tools.value=[];errorMessage.value=''}
function chooseGoal(value){goal.value=value;loadRecommendations()}
async function loadRecommendations(){if(!category.value||!goal.value)return;loading.value=true;errorMessage.value='';try{const {data}=await getRecommendation({step:3,category:category.value,need_type:goal.value});tools.value=data.tools||[]}catch(e){errorMessage.value=e.response?.data?.detail||'无法连接推荐服务，请确认后端已启动。'}finally{loading.value=false}}
</script>
<style scoped>
.teacher-guidance{max-width:1120px;margin:auto}.page-hero{max-width:800px;margin-bottom:40px}.page-hero>span{color:var(--gold-300);font-size:.68rem;letter-spacing:.24em}.page-hero h1{margin:12px 0;font-family:var(--font-display);font-size:clamp(2.2rem,5vw,5rem);font-weight:500;line-height:1.08}.page-hero p{max-width:650px;color:var(--moon-300);line-height:1.8}.guidance-map{position:relative}.choice-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.choice-grid.goals{grid-template-columns:repeat(4,minmax(0,1fr))}.choice-grid button{min-height:96px;padding:16px;border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--material-panel-dark);color:var(--moon-50);text-align:left;cursor:pointer}.choice-grid button[aria-pressed="true"]{border-color:var(--jade-400);box-shadow:inset 0 0 30px var(--effect-jade-soft)}.choice-grid button:disabled{opacity:.35;cursor:not-allowed}.choice-grid strong,.choice-grid small{display:block}.choice-grid small{margin-top:7px;color:var(--moon-300);line-height:1.5}.recommendations{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.recommendations article{padding:20px;border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--material-panel-dark)}.recommendations article>span{color:var(--gold-300);font-size:.7rem}.recommendations h3{margin:8px 0;font-family:var(--font-display);font-size:1.35rem}.recommendations p,.waiting-copy{color:var(--moon-300);line-height:1.65}.recommendations a{display:inline-block;margin-top:12px;color:var(--jade-400)}@media(max-width:800px){.choice-grid.goals,.recommendations{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.choice-grid,.choice-grid.goals,.recommendations{grid-template-columns:1fr}}
</style>
