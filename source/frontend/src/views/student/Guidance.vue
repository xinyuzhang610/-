<script setup>
import { computed, ref } from 'vue'
import InterestBubble from '../../components/student/InterestBubble.vue'

const layers = [
  { title: '此刻，哪一种阻力最明显？', note: '先辨认学习阻力', options: ['读不懂题', '找不到思路', '难以专注'] },
  { title: '它出现在哪片知识星域？', note: '再定位学科领域', options: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治', '信息技术'] },
  { title: '你希望怎样突破？', note: '最后选择学习方式', options: ['概念辨析', '分步推导', '案例启发', '练习巩固'] }
]
const selections = ref(['', '', ''])
const current = ref(0)
const choose = (value) => {
  selections.value[current.value] = value
}
const progress = computed(() => `第 ${current.value + 1} 层，共 3 层`)
const recommendationQuery = computed(() => ({ difficulty: selections.value[0], subject: selections.value[1], approach: selections.value[2] }))
</script>

<template>
  <main class="guidance-page">
    <div class="starfield" aria-hidden="true" />
    <header>
      <p class="eyebrow">STUDENT · KNOWLEDGE ORBIT</p>
      <h1>找到属于你的知识入口</h1>
      <p>用三次选择，把模糊的困惑变成一条可以行动的学习路径。</p>
    </header>

    <ol class="layer-map" aria-label="兴趣引导三层路径">
      <li v-for="(layer, index) in layers" :key="layer.title" data-interest-layer :class="{ active: current === index, done: selections[index] }">
        <button type="button" :aria-label="`前往第 ${index + 1} 层：${layer.note}`" :disabled="index > 0 && !selections[index - 1]" @click="current = index">
          <span>0{{ index + 1 }}</span>{{ layer.note }}
        </button>
      </li>
    </ol>

    <section class="orbit-panel" :aria-labelledby="`layer-title-${current}`">
      <div class="progress-row"><span role="status" aria-live="polite">{{ progress }}</span><span>{{ selections.filter(Boolean).length * 33 + (selections[2] ? 1 : 0) }}%</span></div>
      <div class="progress-track"><i :style="{ width: `${selections.filter(Boolean).length * 33 + (selections[2] ? 1 : 0)}%` }" /></div>
      <p class="layer-kicker">LAYER 0{{ current + 1 }}</p>
      <h2 :id="`layer-title-${current}`">{{ layers[current].title }}</h2>
      <div class="bubble-grid">
        <InterestBubble v-for="(option, index) in layers[current].options" :key="option" :label="option" :index="index" :selected="selections[current] === option" @select="choose(option)" />
      </div>
      <button v-if="current < 2" class="next-layer" type="button" :disabled="!selections[current]" @click="current += 1">进入下一层 →</button>
    </section>

    <aside class="selection-trail" aria-label="已选择的学习线索">
      <div v-for="(layer, index) in layers" :key="layer.note"><span>{{ layer.note }}</span><strong>{{ selections[index] || '待选择' }}</strong></div>
      <RouterLink v-if="selections.every(Boolean)" :to="{ path: '/student/plaza', query: recommendationQuery }">带着线索探索工具广场 →</RouterLink>
    </aside>
  </main>
</template>

<style scoped>
.guidance-page{position:relative;min-height:100%;overflow:hidden;padding:clamp(28px,5vw,72px);background:radial-gradient(circle at 70% 22%,rgb(23 107 90 / 28%),transparent 32%),linear-gradient(145deg,#0c1512,#15241f 58%,#111b18);color:var(--moon-50)}.starfield{position:absolute;inset:0;opacity:.22;background-image:radial-gradient(circle,var(--gold-300) 1px,transparent 1px);background-size:47px 47px;mask-image:linear-gradient(to bottom,#000,transparent 80%)}header,.layer-map,.orbit-panel,.selection-trail{position:relative;z-index:1}header{max-width:800px}.eyebrow,.layer-kicker{color:var(--gold-300);font-size:.72rem;letter-spacing:.22em}h1{max-width:720px;margin:12px 0;font:500 clamp(2.2rem,5vw,4.7rem)/1.08 var(--font-display)}header>p:last-child{max-width:620px;color:var(--moon-300);line-height:1.8}.layer-map{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:760px;margin:40px 0 26px;list-style:none}.layer-map button{width:100%;min-height:58px;padding:10px;border:1px solid rgb(203 211 201 / 18%);border-radius:14px;background:rgb(255 255 255 / 4%);color:var(--ink-300);text-align:left;cursor:pointer}.layer-map button span{display:block;color:var(--gold-300);font-size:.7rem}.layer-map .active button,.layer-map .done button{border-color:var(--jade-400);color:var(--moon-50)}.orbit-panel{max-width:960px;padding:clamp(24px,4vw,48px);border:1px solid rgb(213 166 79 / 25%);border-radius:32px;background:rgb(5 14 11 / 58%);box-shadow:0 30px 90px rgb(0 0 0 / 28%);backdrop-filter:blur(18px)}.progress-row{display:flex;justify-content:space-between;color:var(--moon-300);font-size:.78rem}.progress-track{height:2px;margin:10px 0 36px;background:rgb(255 255 255 / 10%)}.progress-track i{display:block;height:100%;background:linear-gradient(90deg,var(--jade-400),var(--gold-400));transition:width .4s}.orbit-panel h2{margin:8px 0 32px;font:500 clamp(1.6rem,3vw,2.5rem) var(--font-heading)}.bubble-grid{display:flex;flex-wrap:wrap;gap:clamp(14px,3vw,30px)}.selection-trail{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:960px;margin-top:20px}.selection-trail div{padding:15px;border-bottom:1px solid rgb(255 255 255 / 14%)}.selection-trail span,.selection-trail strong{display:block}.selection-trail span{color:var(--ink-300);font-size:.72rem}.selection-trail strong{margin-top:5px}.selection-trail a{grid-column:1/-1;justify-self:end;color:var(--gold-300)}
@media(max-width:700px){.guidance-page{padding:24px 18px}.layer-map{grid-template-columns:1fr}.bubble-grid{justify-content:center}.selection-trail{grid-template-columns:1fr}.selection-trail a{justify-self:start}}@media(prefers-reduced-motion:reduce){.progress-track i{transition:none}}
.next-layer{display:block;min-height:46px;margin:32px 0 0 auto;padding:0 22px;border:0;border-radius:12px;background:var(--gold-400);color:var(--ink-950);font-weight:700;cursor:pointer}.next-layer:disabled{opacity:.4;cursor:not-allowed}
</style>
