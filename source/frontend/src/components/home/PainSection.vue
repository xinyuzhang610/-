<script setup>
import RevealSection from '../motion/RevealSection.vue'

const pains = [
  { number: '壹', title: '备课耗时', copy: '资料筛选、教案组织与工具试用反复切换，真正用于教学设计的时间被不断切碎。', signal: '时间被切成碎片' },
  { number: '贰', title: '资源分散', copy: '课件、题库与数字工具散落各处，知识之间缺少可复用、可追踪的连接。', signal: '知识孤岛彼此失联' },
  { number: '叁', title: '学生差异', copy: '同一课堂里的兴趣、基础与节奏各不相同，单一路径难以回应真实差异。', signal: '每个人需要不同光路' }
]
</script>

<template>
  <RevealSection class="pain" data-narrative-section data-testid="pain-section">
    <div class="page-container pain__grid">
      <header class="pain__intro">
        <p class="kicker">01 / 看见阻力</p>
        <h2>问题不是缺少工具，<br>而是知识尚未连成路</h2>
      </header>
      <ol class="pain__signals">
        <li v-for="pain in pains" :key="pain.title">
          <span class="pain__number">{{ pain.number }}</span>
          <div><h3>{{ pain.title }}</h3><p>{{ pain.copy }}</p></div>
          <span class="pain__signal">{{ pain.signal }}</span>
        </li>
      </ol>
    </div>
  </RevealSection>
</template>

<style scoped>
.pain { padding: clamp(5rem, 10vw, 9rem) 0; background: var(--moon-100); }
.pain__grid { display: grid; grid-template-columns: .8fr 1.4fr; gap: clamp(3rem, 8vw, 9rem); }
.pain__intro { position: sticky; top: 5rem; align-self: start; }
.kicker { margin-bottom: 1rem; color: var(--gold-600); font-size: .75rem; letter-spacing: .24em; }
h2 { font-family: var(--font-title); font-size: clamp(2.2rem, 4vw, 4.5rem); font-weight: 500; line-height: 1.18; }
.pain__signals { list-style: none; }
.pain__signals li { display: grid; grid-template-columns: 3.5rem 1fr auto; gap: 1.5rem; align-items: start; padding: 2.5rem 0; border-top: 1px solid var(--color-border); }
.pain__number { color: var(--jade-700); font-family: var(--font-title); font-size: 1.5rem; }
h3 { margin-bottom: .6rem; font-family: var(--font-title); font-size: 1.65rem; }
.pain__signals p { max-width: 34rem; color: var(--color-ink-soft); }
.pain__signal { max-width: 8rem; padding-left: 1rem; border-left: 2px solid var(--gold-400); color: var(--gold-600); font-size: .76rem; letter-spacing: .12em; }
@media (max-width: 900px) { .pain__grid { grid-template-columns: 1fr; } .pain__intro { position: static; } }
@media (max-width: 640px) { .pain__signals li { grid-template-columns: 2.5rem 1fr; } .pain__signal { grid-column: 2; max-width: none; } }
</style>
