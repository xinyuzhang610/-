<script setup>
import RevealSection from '../motion/RevealSection.vue'
import JourneySubjectFrame from './JourneySubjectFrame.vue'
import { generatedAssets } from '../../assets/generated/asset-manifest'

const teacherSteps = [
  { label: '登录', to: '/login?role=teacher' },
  { label: '需求引导', to: '/login?role=teacher' },
  { label: '工具管理', to: '/teacher/tools' },
  { label: '数据洞察', to: '/teacher/dashboard' }
]
const studentSteps = [
  { label: '兴趣引导', to: '/student/guidance' },
  { label: '工具广场', to: '/student/plaza' },
  { label: 'AI问答', to: '/student/chat' },
  { label: '学习轨迹', to: '/student/records' }
]
</script>

<template>
  <RevealSection class="journey" data-narrative-section data-testid="journey-section">
    <header class="journey__title page-container"><p>03 / 双向同行</p><h2>同一片知识星图，<br>两条彼此照应的路</h2></header>
    <div class="journey__split">
      <article class="journey__path journey__path--teacher">
        <JourneySubjectFrame :asset="generatedAssets.teacherOrbit" tone="teacher" />
        <div class="journey__content"><span class="journey__role">教师端</span><h3>把教学意图，编排成可执行的课堂</h3><ol><li v-for="step in teacherSteps" :key="step.label"><RouterLink :to="step.to">{{ step.label }}</RouterLink></li></ol></div>
      </article>
      <article class="journey__path journey__path--student">
        <JourneySubjectFrame :asset="generatedAssets.studentOrbit" tone="student" />
        <div class="journey__content"><span class="journey__role">学生端</span><h3>从兴趣出发，让每一次探索留下轨迹</h3><ol><li v-for="step in studentSteps" :key="step.label"><RouterLink :to="step.to">{{ step.label }}</RouterLink></li></ol></div>
      </article>
    </div>
  </RevealSection>
</template>

<style scoped>
.journey { padding-top: clamp(5rem, 10vw, 9rem); background: var(--moon-50); }
.journey__title p { color: var(--gold-600); font-size: .75rem; letter-spacing: .24em; }
h2 { margin: 1rem 0 4rem; font-family: var(--font-title); font-size: clamp(2.5rem, 5vw, 5rem); font-weight: 500; line-height: 1.1; }
.journey__split { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.journey__path { position: relative; min-height: 36rem; aspect-ratio: 1 / 1.06; overflow: hidden; color: var(--moon-50); }
.journey__path::after { content: ''; position: absolute; z-index: 1; inset: 0; background: linear-gradient(0deg, rgb(10 20 17 / 96%) 0%, rgb(10 20 17 / 42%) 42%, transparent 72%); }
.journey__content { position: absolute; z-index: 2; right: 0; bottom: 0; left: 0; padding: clamp(2rem, 4vw, 4rem); }
.journey__role { color: var(--gold-200); font-size: .75rem; letter-spacing: .24em; }
h3 { max-width: 13em; margin: 1rem 0 2rem; font-family: var(--font-title); font-size: clamp(1.8rem, 3vw, 3.2rem); font-weight: 500; line-height: 1.2; }
ol { display: flex; flex-wrap: wrap; gap: .5rem; list-style: none; counter-reset: path; }
li { counter-increment: path; }
li a { display: inline-flex; min-height: 2.75rem; align-items: center; padding: .45rem .8rem; border: 1px solid rgb(248 250 245 / 32%); border-radius: 999px; color: var(--moon-50); text-decoration: none; }
li a::before { content: '0' counter(path); margin-right: .45rem; color: var(--gold-200); font-size: .65rem; }
.journey__path:hover :deep(.journey-subject__subject) { transform: translateY(-.4rem) scale(1.012); }
@media (max-width: 900px) { .journey__split { grid-template-columns: 1fr; } .journey__path { min-height: 34rem; aspect-ratio: auto; } }
@media (prefers-reduced-motion: reduce) { .journey__path:hover :deep(.journey-subject__subject) { transform: none; } }
</style>
