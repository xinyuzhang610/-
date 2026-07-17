<script setup>
import RevealSection from '../motion/RevealSection.vue'
import { generatedAssets } from '../../assets/generated/asset-manifest'
</script>

<template>
  <RevealSection class="showcase" data-narrative-section data-testid="showcase-section">
    <img class="showcase__universe" :src="generatedAssets.knowledgeUniverse.src" alt="" :width="generatedAssets.knowledgeUniverse.width" :height="generatedAssets.knowledgeUniverse.height" loading="lazy">
    <div class="page-container showcase__inner">
      <header><p>04 / 产品实景</p><h2><span>不是想象中的功能，</span><strong>是正在发生的学习界面</strong></h2></header>
      <div class="showcase__previews">
        <article class="preview preview--guidance">
          <div class="preview__bar"><span>需求引导</span><i></i><i></i></div>
          <div class="guidance"><span class="guidance__question">这节课，你想解决什么？</span><button type="button">激发写作灵感</button><button type="button">讲清公式推导</button><div class="guidance__answer">正在为你的教学情境组织建议…</div></div>
          <footer>来自教师端 · 需求发现与工具推荐</footer>
        </article>
        <article class="preview preview--analytics">
          <div class="preview__bar"><span>数据看板</span><i></i><i></i></div>
          <div class="analytics"><div class="analytics__metric"><b>学习轨迹</b><small>最近 7 日使用趋势</small></div><svg viewBox="0 0 420 160" role="img" aria-label="学习活动趋势示意"><path class="grid" d="M10 35h400M10 80h400M10 125h400"/><path class="line" d="m10 130 64-24 64 8 64-50 64 19 64-56 64 22"/><g><circle cx="74" cy="106" r="5"/><circle cx="202" cy="64" r="5"/><circle cx="330" cy="27" r="5"/></g></svg><div class="analytics__tags"><span>工具使用</span><span>学习记录</span><span>热门工具</span></div></div>
          <footer>来自数据看板 · 使用趋势与学习记录</footer>
        </article>
      </div>
    </div>
  </RevealSection>
</template>

<style scoped>
.showcase { position: relative; display: flex; align-items: center; overflow: hidden; padding: clamp(0rem, 4vw, 3rem) 0; background: var(--moon-100); }
.showcase__universe { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .08; mix-blend-mode: multiply; }
.showcase__inner { position: relative; }
header p { font-family: 'Ma Shan Zheng', cursive; font-size: 2.2rem; letter-spacing: .05em; background: linear-gradient(135deg, #3a5a3a 0%, #1a3a24 35%, #2a5a38 65%, #4a6840 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2 { max-width: 14em; margin-top: 1rem; font-family: var(--font-title); font-size: clamp(2.35rem, 4vw, 4.35rem); font-weight: 500; line-height: 1.12; letter-spacing: -.035em; }
h2 span, h2 strong { display: block; }
h2 span { color: #777; font-size: .72em; font-weight: 400; letter-spacing: -.015em; }
h2 strong { margin-top: .28em; color: var(--color-ink); font-weight: 500; }
@media (hover: hover) { h2 { transition: transform .3s var(--ease-out); cursor: default; } h2:hover { transform: scale(1.03); } }
.showcase__previews { display: grid; grid-template-columns: 1.08fr .92fr; gap: clamp(1rem, 3vw, 2.5rem); align-items: end; margin-top: 2rem; }
.preview { overflow: hidden; border: 1px solid var(--color-border); border-radius: 1.2rem; background: rgb(248 250 245 / 92%); box-shadow: var(--shadow-lg); }
.preview--guidance { transform: translateY(-1rem); }
.preview--analytics { transform: translateY(-1rem); }
.preview__bar { display: flex; min-height: 3rem; align-items: center; gap: .4rem; padding: .7rem 1rem; border-bottom: 1px solid var(--color-border); }
.preview__bar span { margin-right: auto; font-weight: 700; }.preview__bar i { width: .55rem; height: .55rem; border-radius: 50%; background: var(--gold-400); }.preview__bar i:last-child { background: var(--jade-400); }
.preview footer { padding: .8rem 1rem; border-top: 1px solid var(--color-border); color: var(--color-ink-soft); font-size: .75rem; }
.guidance { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; min-height: 20rem; padding: clamp(1.5rem, 4vw, 3rem); }
.guidance__question,.guidance__answer { grid-column: 1 / -1; }.guidance__question { font-family: var(--font-title); font-size: 1.7rem; }.guidance button { min-height: 3rem; padding: .6rem; border: 1px solid var(--jade-200); border-radius: .6rem; background: transparent; }.guidance__answer { align-self: end; padding: 1rem; border-left: 3px solid var(--gold-400); background: var(--moon-100); color: var(--color-ink-soft); }
.analytics { min-height: 18rem; padding: 2rem; }.analytics__metric b,.analytics__metric small { display: block; }.analytics__metric small { color: var(--color-ink-soft); }.analytics svg { margin: 1.5rem 0; }.grid { fill: none; stroke: var(--color-border); }.line { fill: none; stroke: var(--jade-700); stroke-width: 4; }.analytics circle { fill: var(--gold-400); }.analytics__tags { display: flex; flex-wrap: wrap; gap: .5rem; }.analytics__tags span { padding: .3rem .65rem; border-radius: 99px; background: var(--moon-200); font-size: .75rem; }
@media (max-width: 900px) { .showcase__previews { grid-template-columns: 1fr; } .preview--guidance, .preview--analytics { transform: none; } }
@media (max-width: 520px) { .guidance { grid-template-columns: 1fr; }.guidance button { grid-column: 1; } }
@media (prefers-reduced-motion: reduce) { .preview--guidance, .preview--analytics { transform: none; } }
</style>
