<script setup>
import RevealSection from '../motion/RevealSection.vue'
import painBg from '../../assets/generated/3.png'

const pains = [
  { number: '壹', title: '备课耗时', copy: '资料筛选、教案组织与工具试用反复切换，真正用于教学设计的时间被不断切碎。', signal: '时间被切成碎片' },
  { number: '贰', title: '资源分散', copy: '课件、题库与数字工具散落各处，知识之间缺少可复用、可追踪的连接。', signal: '知识孤岛彼此失联' },
  { number: '叁', title: '学生差异', copy: '同一课堂里的兴趣、基础与节奏各不相同，单一路径难以回应真实差异。', signal: '每个人需要不同光路' }
]
</script>

<template>
  <RevealSection class="pain" data-narrative-section data-testid="pain-section">
    <img class="pain__bg" :src="painBg" alt="" />
    <div class="pain__shade" />
    <div class="page-container pain__grid">
      <header class="pain__intro">
        <p class="kicker">01 / 看见阻力</p>
        <h2>
          <span data-testid="pain-heading-line">问题不在工具多少</span>
          <strong data-testid="pain-heading-line">而在知识尚未成路</strong>
        </h2>
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
.pain { position: relative; min-height: 100svh; display: flex; align-items: center; padding: clamp(5rem, 10vw, 9rem) 0; overflow: hidden; background: #0a1a18; color: var(--moon-50); }
.pain__bg { position: absolute; inset: 0; z-index: 0; width: 100%; height: 100%; object-fit: cover; filter: hue-rotate(-15deg) saturate(.8); }
.pain__shade { position: absolute; inset: 0; z-index: 0; background: linear-gradient(90deg, rgb(5 20 15 / 50%) 0%, rgb(5 20 15 / 25%) 50%, rgb(5 20 15 / 0%) 100%), linear-gradient(0deg, rgb(5 20 15 / 30%), transparent 45%); }
.pain__grid { position: relative; z-index: 2; display: grid; grid-template-columns: minmax(18rem, .78fr) minmax(32rem, 1.35fr); gap: clamp(3rem, 7vw, 8rem); }
.pain__intro { position: sticky; top: 5rem; align-self: start; min-width: 0; }
.kicker { margin-bottom: 1rem; font-family: 'Ma Shan Zheng', cursive; font-size: 2.2rem; line-height: .9; letter-spacing: .05em; margin-top: 1rem; transform: translateY(0); background: linear-gradient(135deg, var(--gold-200) 0%, var(--gold-400) 40%, var(--gold-600) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2 { margin-top: 5rem; max-width: 8.6em; font-family: var(--font-title); font-size: clamp(2.35rem, 4vw, 4.35rem); font-weight: 500; line-height: 1.12; letter-spacing: -.035em; }
h2 span,
h2 strong { display: block; }
h2 span { color: var(--moon-300); font-size: .72em; font-weight: 400; letter-spacing: -.015em; text-shadow: 0 0 8px rgb(0 0 0 / 90%), 0 0 20px rgb(0 0 0 / 60%), 0 0 40px rgb(0 0 0 / 35%); transition: transform .3s var(--ease-out); cursor: default; }
h2 strong { margin-top: .28em; color: var(--moon-50); font-weight: 500; text-shadow: 0 1px 6px rgb(0 0 0 / 60%); transition: transform .3s var(--ease-out); cursor: default; }
h2:hover span { transform: scale(1.04); }
h2:hover strong { transform: scale(1.04); }
.pain__signals { list-style: none; }
.pain__signals li { display: grid; grid-template-columns: 3.5rem 1fr auto; gap: 1.5rem; align-items: start; padding: 2rem; margin-bottom: .8rem; border: 1px solid rgb(248 250 245 / 8%); border-radius: var(--radius-xl); background: rgb(255 255 255 / 3%); backdrop-filter: blur(6px); transition: transform .35s var(--ease-out), border-color .3s, box-shadow .3s, background .3s; cursor: default; }
.pain__signals li:hover { transform: translateY(-3px); border-color: var(--gold-400); background: rgb(255 255 255 / 8%); box-shadow: 0 12px 36px rgb(0 0 0 / 35%), 0 0 28px rgb(213 166 79 / 8%); }
.pain__number { font-family: 'Ma Shan Zheng', cursive; font-size: 1.8rem; background: linear-gradient(135deg, var(--gold-200) 0%, var(--gold-400) 40%, var(--gold-600) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; transition: transform .3s var(--ease-out); cursor: default; }
.pain__number:hover { transform: scale(1.15); }
h3 { margin-bottom: .6rem; font-family: 'KaiTi', 'STKaiti', 'AR PL UKai CN', serif; font-size: 2rem; color: var(--moon-50); text-shadow: 0 1px 4px rgb(0 0 0 / 60%); }
.pain__signals p { max-width: 34rem; font-family: 'KaiTi', 'STKaiti', 'AR PL UKai CN', serif; font-size: 1.15rem; color: var(--moon-100); line-height: 1.8; text-shadow: 0 1px 3px rgb(0 0 0 / 50%); }
.pain__signal { max-width: none; padding: .3rem 1rem; border: none; border-radius: .3rem; font-family: 'Ma Shan Zheng', cursive; font-size: 1.35rem; letter-spacing: .06em; background: linear-gradient(135deg, var(--gold-200) 0%, var(--gold-400) 40%, var(--gold-600) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; transition: transform .3s var(--ease-out); cursor: default; display: inline-block; position: relative; }
.pain__signal::before { content: ''; position: absolute; inset: 0; z-index: -1; border-radius: .3rem; background: rgb(10 5 2 / 55%); backdrop-filter: blur(2px); }
.pain__signal:hover { transform: scale(1.12); }
@media (max-width: 1100px) {
  .pain__grid { grid-template-columns: 1fr; }
  .pain__intro { position: static; }
  h2 { max-width: 11em; }
}
@media (max-width: 640px) {
  h2 { font-size: clamp(2.15rem, 11vw, 3.15rem); }
  .pain__signals li { grid-template-columns: 2.5rem 1fr; }
  .pain__signal { grid-column: 2; }
}
</style>
