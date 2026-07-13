<script setup>
import RevealSection from '../motion/RevealSection.vue'
import BrandMark from '../brand/BrandMark.vue'
</script>

<template>
  <RevealSection class="call" data-narrative-section data-testid="final-section">
    <div class="page-container call__inner">
      <BrandMark />
      <p class="call__kicker">知识不应停在答案里</p>
      <h2>从今天的问题出发，<br>长成明天的学习路径</h2>
      <p class="call__promise">教师更从容地组织教学，学生更主动地理解世界。每一次真实提问，都值得被看见、被连接、被继续。</p>
      <div class="call__actions">
        <RouterLink to="/login?role=teacher">以教师身份开始 <span aria-hidden="true">→</span></RouterLink>
        <RouterLink to="/student/guidance">以学生身份探索 <span aria-hidden="true">→</span></RouterLink>
      </div>
    </div>
  </RevealSection>
</template>

<style scoped>
.call { position: relative; padding: clamp(6rem, 13vw, 12rem) 0; overflow: hidden; background: var(--ink-950); color: var(--moon-50); text-align: center; }
.call::before { content: ''; position: absolute; inset: 10% 20%; border: 1px solid rgb(213 166 79 / 18%); border-radius: 50%; box-shadow: 0 0 8rem rgb(66 185 154 / 16%); }
.call__inner { position: relative; display: flex; flex-direction: column; align-items: center; }
.call :deep(.brand-mark) { color: var(--moon-50); }
.call__kicker { margin-top: 3rem; color: var(--gold-200); font-size: .75rem; letter-spacing: .28em; }
h2 { margin-top: 1.2rem; font-family: var(--font-title); font-size: clamp(2.7rem, 6vw, 6rem); font-weight: 500; line-height: 1.08; }
.call__promise { max-width: 42rem; margin-top: 2rem; color: rgb(248 250 245 / 68%); }
.call__actions { display: flex; flex-wrap: wrap; justify-content: center; gap: .75rem; margin-top: 2.5rem; }
.call__actions a { display: inline-flex; min-height: 3rem; align-items: center; gap: 1rem; padding: .7rem 1.2rem; border: 1px solid var(--gold-400); border-radius: 999px; color: var(--moon-50); text-decoration: none; }.call__actions a:last-child { border-color: var(--jade-200); }
</style>
