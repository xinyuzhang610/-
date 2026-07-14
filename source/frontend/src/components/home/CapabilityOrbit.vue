<script setup>
import RevealSection from '../motion/RevealSection.vue'
import KnowledgeCore from '../brand/KnowledgeCore.vue'

const capabilities = [
  { name: '需求发现', copy: '说出教学情境，梳理真正要解决的问题。', to: '/feature/discover', icon: 'M4 12h16M12 4v16' },
  { name: '智能推荐', copy: '让适配的资源与工具主动抵达。', to: '/feature/resource', icon: 'm5 12 4 4L19 6' },
  { name: 'AI问答', copy: '在追问中澄清概念、打开思路。', to: '/student/chat', icon: 'M5 5h14v10H9l-4 4V5Z' },
  { name: '工具广场', copy: '探索可直接使用的学习与教学工具。', to: '/student/plaza', icon: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z' },
  { name: '学习分析', copy: '把过程沉淀为可回看的成长线索。', to: '/feature/analysis', icon: 'M5 19V9m7 10V5m7 14v-7' }
]
</script>

<template>
  <RevealSection class="orbit" data-narrative-section data-testid="capability-section">
    <div class="page-container">
      <header class="orbit__heading"><p>02 / 汇聚能力</p><h2>五种能力，围绕同一个知识核心生长</h2></header>
      <div class="orbit__stage">
        <KnowledgeCore class="orbit__core" />
        <RouterLink v-for="(item, index) in capabilities" :key="item.name" :to="item.to" class="orbit__item" :style="{ '--index': index }">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path :d="item.icon" /></svg>
          <span><strong>{{ item.name }}</strong><small>{{ item.copy }}</small></span>
        </RouterLink>
      </div>
    </div>
  </RevealSection>
</template>

<style scoped>
.orbit { padding: clamp(5rem, 10vw, 9rem) 0; overflow: hidden; background: var(--ink-950); color: var(--moon-50); }
.orbit__heading { position: relative; z-index: 2; max-width: 50rem; }
.orbit__heading p { color: var(--gold-200); font-size: .75rem; letter-spacing: .24em; }
h2 { margin-top: 1rem; font-family: var(--font-title); font-size: clamp(2.4rem, 5vw, 5rem); font-weight: 500; line-height: 1.1; }
.orbit__stage { position: relative; height: min(72vw, 48rem); min-height: 38rem; margin-top: -1rem; }
.orbit__stage::before { content: ''; position: absolute; inset: 9% 15%; border: 1px solid rgb(169 221 206 / 22%); border-radius: 50%; transform: rotate(-8deg); }
.orbit__core { position: absolute; top: 50%; left: 50%; width: min(40vw, 29rem); transform: translate(-50%, -50%); }
.orbit__item { position: absolute; z-index: 2; display: flex; width: 14rem; min-height: 6rem; align-items: flex-start; gap: .9rem; padding: 1rem; border-left: 1px solid var(--gold-400); color: var(--moon-50); text-decoration: none; }
.orbit__item:nth-of-type(1) { top: 8%; left: 5%; } .orbit__item:nth-of-type(2) { top: 12%; right: 3%; } .orbit__item:nth-of-type(3) { top: 48%; right: 0; } .orbit__item:nth-of-type(4) { bottom: 4%; right: 20%; } .orbit__item:nth-of-type(5) { bottom: 10%; left: 5%; }
.orbit__item svg { width: 1.5rem; flex: 0 0 1.5rem; fill: none; stroke: var(--jade-200); stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.6; }
.orbit__item strong,.orbit__item small { display: block; } .orbit__item strong { font-size: 1.1rem; } .orbit__item small { margin-top: .4rem; color: rgb(248 250 245 / 62%); line-height: 1.5; }
.orbit__item:hover { background: rgb(169 221 206 / 8%); color: var(--gold-200); }
@media (max-width: 640px) { .orbit__stage { display: grid; height: auto; min-height: 0; gap: .75rem; margin-top: 3rem; } .orbit__stage::before,.orbit__core { display: none; } .orbit__item { position: static; width: 100%; min-height: 5.5rem; border: 1px solid rgb(169 221 206 / 25%); border-radius: var(--radius-md); } }
@media (prefers-reduced-motion: reduce) { .orbit__item { transform: none; } }
</style>
