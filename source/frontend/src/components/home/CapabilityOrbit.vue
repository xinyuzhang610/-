<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import RevealSection from '../motion/RevealSection.vue'
import KnowledgeCore from '../brand/KnowledgeCore.vue'

const capabilities = [
  { name: '需求发现', copy: '说出教学情境，梳理真正要解决的问题。', to: '/feature/discover' },
  { name: '智能推荐', copy: '让适配的资源与工具主动抵达。', to: '/feature/resource' },
  { name: 'AI问答', copy: '在追问中澄清概念、打开思路。', to: '/student/chat' },
  { name: '工具广场', copy: '探索可直接使用的学习与教学工具。', to: '/student/plaza' },
  { name: '学习分析', copy: '把过程沉淀为可回看的成长线索。', to: '/feature/analysis' }
]

const stage = ref(null)
const items = ref([])
let raf
const angles = capabilities.map((_, i) => (i / 5) * Math.PI * 2 - Math.PI / 2)

function animate() {
  if (!stage.value) { raf = requestAnimationFrame(animate); return }
  const w = stage.value.offsetWidth
  const h = stage.value.offsetHeight
  const cx = w * .5, rx = w * .38, ry = h * .34
  const cy = h * .5
  const els = stage.value.querySelectorAll('.orbit__item')
  els.forEach((el, i) => {
    angles[i] += .0015
    const x = cx + Math.cos(angles[i]) * rx - el.offsetWidth / 2
    const y = cy + Math.sin(angles[i]) * ry - el.offsetHeight / 2
    el.style.left = `${x}px`
    el.style.top = `${y}px`
  })
  raf = requestAnimationFrame(animate)
}

onMounted(() => { raf = requestAnimationFrame(animate) })
onBeforeUnmount(() => cancelAnimationFrame(raf))
</script>

<template>
  <RevealSection class="orbit" data-narrative-section data-testid="capability-section">
    <div class="page-container">
      <header class="orbit__heading"><p>02 / 汇聚能力</p><h2>五种能力，围绕同一个知识核心生长</h2></header>
      <div ref="stage" class="orbit__stage">
        <KnowledgeCore class="orbit__core" />
        <RouterLink v-for="(item, index) in capabilities" :key="item.name" :to="item.to" :ref="el => items[index] = el" class="orbit__item">
          <span><strong>{{ item.name }}</strong><small>{{ item.copy }}</small></span>
        </RouterLink>
      </div>
    </div>
  </RevealSection>
</template>

<style scoped>
.orbit { min-height: 100svh; display: flex; align-items: center; padding: clamp(5rem, 10vw, 9rem) 0; overflow: hidden; background: #f5f0e8; color: var(--color-ink); }
.orbit__heading { position: relative; z-index: 2; max-width: 50rem; }
.orbit__heading p { font-family: 'Ma Shan Zheng', cursive; font-size: 2.2rem; letter-spacing: .05em; transform: translateY(-3rem); background: linear-gradient(135deg, var(--gold-200) 0%, var(--gold-400) 40%, var(--gold-600) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2 { margin-top: 1rem; font-family: var(--font-title); font-size: clamp(2.35rem, 4vw, 4.35rem); font-weight: 500; line-height: 1.12; letter-spacing: -.035em; transition: transform .3s var(--ease-out); cursor: default; }
h2:hover { transform: scale(1.04); }
.orbit__stage { position: relative; height: 70vh; min-height: 32rem; margin-top: -1rem; }
.orbit__stage::before { content: ''; position: absolute; inset: 8% 14%; border-radius: 50%; border: 10px solid rgb(200 230 245 / 16%); box-shadow: 0 0 8px rgb(190 225 245 / 18%), 0 0 18px rgb(210 235 250 / 10%), 0 0 36px rgb(225 240 255 / 6%), 0 0 60px rgb(235 245 255 / 3%), inset 0 0 6px rgb(170 215 240 / 16%), inset 0 0 16px rgb(200 230 245 / 7%), inset 0 0 32px rgb(225 240 255 / 3%); transform: rotate(-6deg); }
.orbit__core { position: absolute; top: 50%; left: 50%; width: min(55vw, 42rem); height: min(55vw, 42rem); transform: translate(-50%, -50%); }
.orbit__item { position: absolute; z-index: 2; display: flex; flex-direction: column; align-items: center; gap: .5rem; width: 9rem; text-align: center; color: var(--color-ink); text-decoration: none; transition: filter .3s; }
.orbit__item::before { content: ''; display: block; width: 2.2rem; height: 2.2rem; border-radius: 50%; background: radial-gradient(circle at 35% 35%, rgb(255 255 255 / 50%), var(--c) 60%, transparent 100%); box-shadow: 0 0 14px var(--c), 0 0 35px var(--c); transition: transform .4s var(--ease-out), box-shadow .4s; }
.orbit__item:nth-of-type(1) { --c: #e4c477; } .orbit__item:nth-of-type(2) { --c: #42b99a; } .orbit__item:nth-of-type(3) { --c: #7ad4e8; } .orbit__item:nth-of-type(4) { --c: #ce93d8; } .orbit__item:nth-of-type(5) { --c: #ff8a65; }
.orbit__item svg { display: none; }
.orbit__item strong { display: block; font-size: 1.05rem; font-weight: 700; margin-bottom: .15rem; }
.orbit__item small { display: block; color: var(--color-ink-soft); line-height: 1.45; font-size: .8rem; }
.orbit__item:hover { filter: brightness(1.3); z-index: 5; }
.orbit__item:hover::before { transform: scale(1.4); box-shadow: 0 0 30px var(--c), 0 0 65px var(--c), 0 0 100px var(--c); }
@media (max-width: 640px) { .orbit__stage { display: grid; height: auto; min-height: 0; gap: .75rem; margin-top: 2rem; } .orbit__stage::before,.orbit__core,.starfield { display: none; } .orbit__item { position: static !important; width: 100%; min-height: 5.5rem; flex-direction: row; text-align: left; border: 1px solid rgb(169 221 206 / 25%); border-radius: var(--radius-md); } .orbit__item::before { width: 2rem; height: 2rem; } }
@media (prefers-reduced-motion: reduce) { .orbit__item { transform: none; } }
</style>
