<script setup>
import { ref } from 'vue'
import BrandMark from '../brand/BrandMark.vue'
import InkLandscape from '../brand/InkLandscape.vue'
import KnowledgeCore from '../brand/KnowledgeCore.vue'
import EntryLink from './EntryLink.vue'
import HeroScratchReveal from './HeroScratchReveal.vue'
import { generatedAssets } from '../../assets/generated/asset-manifest'

const animationSkipped = ref(false)
const hasRevealed = ref(false)
const heroArtFailed = ref(false)
const revealUnavailable = ref(false)
</script>

<template>
  <section class="hero" :class="{ 'hero--still': animationSkipped }" data-narrative-section data-testid="hero-section">
    <div class="hero__art" :class="{ 'hero__art--fallback': heroArtFailed }">
      <img
        v-if="!heroArtFailed"
        data-testid="hero-background-image"
        :src="generatedAssets.heroInkLandscape.src"
        :width="generatedAssets.heroInkLandscape.width"
        :height="generatedAssets.heroInkLandscape.height"
        :alt="generatedAssets.heroInkLandscape.alt"
        fetchpriority="high"
        @error="heroArtFailed = true"
      >
      <InkLandscape :parallax="!animationSkipped" class="hero__ink" />
      <KnowledgeCore class="hero__core" />
    </div>
    <HeroScratchReveal
      :skipped="animationSkipped"
      @first-reveal="hasRevealed = true"
      @static-mode="revealUnavailable = true"
    />
    <div class="hero__content page-container">
      <p class="hero__eyebrow">知识觉醒 · 智能教育同行者</p>
      <h1>让每一次提问，<br><em>照亮学习路径</em></h1>
      <p class="hero__lead">从发现需求，到每个学生清晰可见的成长轨迹。智教通让工具、资源与洞察围绕学习发生。</p>
      <div class="hero__actions" aria-label="选择进入方式">
        <EntryLink role="teacher" label="教师入口" to="/login?role=teacher" test-id="teacher-entry" />
        <EntryLink role="student" label="学生入口" to="/student/guidance" test-id="student-entry" />
      </div>
      <p v-if="!hasRevealed && !animationSkipped && !revealUnavailable" class="hero__reveal-hint" aria-hidden="true">
        移动光标，唤醒画卷
      </p>
      <button class="hero__skip" type="button" @click="animationSkipped = true">
        {{ animationSkipped ? '动态已跳过' : '跳过动态' }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.hero { position: relative; min-height: max(46rem, 100svh); overflow: hidden; isolation: isolate; background: var(--ink-950); color: var(--moon-50); }
.hero__art { position: absolute; z-index: 0; inset: 0; min-height: 46rem; }
.hero__art--fallback { background: radial-gradient(circle at 76% 42%, rgb(66 185 154 / 18%), transparent 28%), linear-gradient(135deg, #07110e, #17271f); }
.hero__art::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, rgb(10 20 17 / 94%) 0%, rgb(10 20 17 / 70%) 43%, rgb(10 20 17 / 12%) 76%), linear-gradient(0deg, var(--ink-950), transparent 30%); }
.hero__art > img { width: 100%; height: 100%; object-fit: cover; opacity: .72; }
.hero__ink { position: absolute; inset: auto 0 0; min-height: 36%; opacity: .2; mix-blend-mode: screen; }
.hero__core { position: absolute; z-index: 1; top: 50%; right: clamp(-8rem, 3vw, 4rem); width: min(49vw, 42rem); transform: translateY(-50%); opacity: .75; }
.hero__content { position: relative; z-index: 2; display: flex; min-height: max(46rem, 100svh); flex-direction: column; justify-content: center; align-items: flex-start; padding-block: 8rem 5rem; pointer-events: none; }
.hero__content :is(a, button) { pointer-events: auto; }
.hero__eyebrow { margin-bottom: 1.5rem; color: var(--gold-200); font-size: .78rem; letter-spacing: .28em; }
h1 { max-width: 9.5em; font-family: var(--font-title); font-size: clamp(3rem, 7.5vw, 7rem); font-weight: 600; letter-spacing: -.055em; line-height: .98; text-wrap: balance; }
h1 em { color: var(--jade-200); font-style: normal; }
.hero__lead { max-width: 36rem; margin-top: 2rem; color: rgb(248 250 245 / 80%); font-size: clamp(1rem, 1.5vw, 1.2rem); }
.hero__actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 2rem; }
.hero__reveal-hint { margin-top: 1rem; color: rgb(248 250 245 / 56%); font-size: .72rem; letter-spacing: .18em; }
.hero__skip { min-height: 2.75rem; margin-top: 1rem; padding: .25rem .75rem; background: transparent; color: rgb(248 250 245 / 68%); text-decoration: underline; text-underline-offset: .25rem; }
.hero--still .hero__core { display: none; }
@media (max-width: 700px) { .hero__art::after { background: linear-gradient(0deg, var(--ink-950) 8%, rgb(10 20 17 / 64%) 75%); } .hero__core { top: 28%; right: -6rem; width: 22rem; } .hero__content { justify-content: flex-end; } }
@media (prefers-reduced-motion: reduce) { .hero__core { display: none; } }
</style>
