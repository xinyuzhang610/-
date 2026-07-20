<script setup>
import { computed, ref } from 'vue'
import InterestBubble from '../../components/student/InterestBubble.vue'
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageFrame from '../../components/vintage/VintageFrame.vue'
import VintageOrnament from '../../components/vintage/VintageOrnament.vue'
import VintagePostmark from '../../components/vintage/VintagePostmark.vue'

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
  <main class="guidance-page vintage-theme">
    <header class="page-hero">
      <VintageOrnament name="swallow" />
      <VintageRibbonTitle label="STUDENT · KNOWLEDGE ORBIT" />
      <h1>找到属于你的知识入口</h1>
      <p>用三次选择，把模糊的困惑变成一条可以行动的学习路径。</p>
      <VintageDivider />
    </header>

    <ol class="layer-map" aria-label="兴趣引导三层路径">
      <li v-for="(layer, index) in layers" :key="layer.title" :class="{ active: current === index, done: selections[index] }">
        <button type="button" :aria-label="`前往第 ${index + 1} 层：${layer.note}`" :disabled="index > 0 && !selections[index - 1]" @click="current = index">
          <span>0{{ index + 1 }}</span>{{ layer.note }}
        </button>
      </li>
    </ol>

    <VintageFrame tone="gold" class="orbit-frame">
      <section class="orbit-panel" :aria-labelledby="`layer-title-${current}`">
        <div class="orbit-corner orbit-corner--tl"><VintageOrnament name="flourish-tl" /></div>
        <div class="orbit-corner orbit-corner--tr"><VintageOrnament name="flourish-tr" /></div>
        <div class="orbit-corner orbit-corner--bl"><VintageOrnament name="flourish-bl" /></div>
        <div class="orbit-corner orbit-corner--br"><VintageOrnament name="flourish-br" /></div>

        <div class="progress-row"><span role="status" aria-live="polite">{{ progress }}</span><span>{{ selections.filter(Boolean).length * 33 + (selections[2] ? 1 : 0) }}%</span></div>
        <div class="progress-track"><i :style="{ width: `${selections.filter(Boolean).length * 33 + (selections[2] ? 1 : 0)}%` }" /></div>
        <p class="layer-kicker">LAYER 0{{ current + 1 }}</p>
        <h2 :id="`layer-title-${current}`">{{ layers[current].title }}</h2>
        <div class="bubble-grid">
          <InterestBubble v-for="(option, idx) in layers[current].options" :key="option" :label="option" :index="idx" :selected="selections[current] === option" @select="choose(option)" />
        </div>
        <button v-if="current < 2" class="next-layer" type="button" :disabled="!selections[current]" @click="current += 1">
          进入下一层 →
        </button>
      </section>
    </VintageFrame>

    <aside class="selection-trail" aria-label="已选择的学习线索">
      <div v-for="(layer, index) in layers" :key="layer.note" class="trail-item">
        <span class="trail-label">{{ layer.note }}</span>
        <strong>{{ selections[index] || '待选择' }}</strong>
        <VintagePostmark v-if="selections[index]" :text="selections[index].slice(0,4)" />
      </div>
      <RouterLink v-if="selections.every(Boolean)" :to="{ path: '/student/plaza', query: recommendationQuery }" class="trail-cta">
        带着线索探索工具广场 →
      </RouterLink>
    </aside>
  </main>
</template>

<style scoped>
.guidance-page.vintage-theme {
  position: relative;
  min-height: 100%;
  padding: clamp(28px, 5vw, 58px) clamp(20px, 4vw, 48px) 80px;
  background:
    radial-gradient(circle at 70% 22%, rgba(184, 161, 110, 0.08), transparent 32%),
    radial-gradient(circle at 30% 80%, rgba(138, 154, 140, 0.06), transparent 28%),
    #f5f1e8;
  color: #4a4333;
}

.guidance-page.vintage-theme::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.035;
  background-image:
    radial-gradient(circle at 20% 20%, #6b5d3e 1px, transparent 1px),
    radial-gradient(circle at 80% 80%, #6b5d3e 1px, transparent 1px);
  background-size: 80px 80px;
  z-index: 0;
}

/* ---- Hero ---- */
.page-hero {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto 1.5rem;
  text-align: center;
}

.page-hero .vintage-ornament {
  margin-bottom: 0.75rem;
}

.page-hero h1 {
  margin: 0.75rem 0;
  font: 500 clamp(2.2rem, 5vw, 4rem)/1.1 var(--font-display);
  color: #3d3526;
}

.page-hero > p {
  max-width: 580px;
  margin: 0 auto;
  color: #6b5d3e;
  line-height: 1.75;
  font-size: 0.95rem;
}

.page-hero .vintage-divider {
  margin-top: 1.25rem;
}

/* ---- 三层导航 ---- */
.layer-map {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  max-width: 780px;
  margin: 0 auto 2rem;
  list-style: none;
  padding: 0;
}

.layer-map li button {
  width: 100%;
  min-height: 62px;
  padding: 10px 14px;
  border: 1px solid rgba(196, 180, 154, 0.4);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
  color: #8b7e60;
  text-align: left;
  cursor: pointer;
  font: inherit;
  font-family: var(--font-display);
  font-size: 0.88rem;
  transition: all 0.25s ease;
  position: relative;
}

.layer-map li button::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px dashed rgba(139, 111, 71, 0.15);
  border-radius: 1px;
  pointer-events: none;
}

.layer-map li button span {
  display: block;
  color: #b8a16e;
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  margin-bottom: 3px;
}

.layer-map li button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(107, 93, 62, 0.1);
  border-color: rgba(184, 161, 110, 0.5);
}

.layer-map li.active button,
.layer-map li.done button {
  color: #4a4333;
  background: rgba(250, 248, 242, 0.85);
  border-color: rgba(138, 154, 140, 0.5);
}

.layer-map li.done button {
  border-color: rgba(184, 161, 110, 0.5);
}

.layer-map li.done button::after {
  content: '✓';
  position: absolute;
  top: 8px;
  right: 12px;
  font-size: 0.7rem;
  color: #8a9a8c;
}

/* ---- 轨道面板 ---- */
.orbit-frame {
  position: relative;
  z-index: 1;
  max-width: 980px;
  margin: 0 auto;
  overflow: hidden;
}

.orbit-panel {
  position: relative;
  min-height: 320px;
  overflow: hidden;
  padding: 2rem 1.5rem 1.5rem;
  text-align: center;
}

.orbit-corner {
  position: absolute;
  z-index: 2;
}

.orbit-corner--tl { top: 6px; left: 6px; }
.orbit-corner--tr { top: 6px; right: 6px; }
.orbit-corner--bl { bottom: 6px; left: 6px; }
.orbit-corner--br { bottom: 6px; right: 6px; }

.progress-row {
  display: flex;
  justify-content: space-between;
  color: #6b5d3e;
  font-size: 0.78rem;
  font-family: var(--font-display);
}

.progress-track {
  height: 3px;
  margin: 12px 0 32px;
  background: rgba(196, 180, 154, 0.25);
  border-radius: 2px;
}

.progress-track i {
  display: block;
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(90deg, #8a9a8c, #b8a16e);
  transition: width 0.4s ease;
  box-shadow: 0 0 8px rgba(138, 154, 140, 0.25);
}

.layer-kicker {
  color: #8b6f47;
  font-size: 0.68rem;
  letter-spacing: 0.24em;
  font-family: var(--font-display);
}

.orbit-panel h2 {
  margin: 8px 0 36px;
  font: 500 clamp(1.6rem, 3vw, 2.4rem)/1.2 var(--font-display);
  color: #3d3526;
}

.bubble-grid {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(14px, 3vw, 28px);
  justify-content: center;
  margin-top: 0.5rem;
}

.next-layer {
  display: inline-block;
  min-height: 48px;
  margin: 36px auto 0;
  padding: 0 26px;
  border: 1px solid #b8a16e;
  border-radius: 2px;
  background: linear-gradient(135deg, rgba(250, 248, 242, 0.95), rgba(242, 239, 230, 0.85));
  color: #5c4f34;
  font: inherit;
  font-family: var(--font-display);
  font-size: 0.92rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  position: relative;
}

.next-layer::before {
  content: '';
  position: absolute;
  inset: 2px;
  border: 1px dashed rgba(139, 111, 71, 0.18);
  pointer-events: none;
}

.next-layer:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(107, 93, 62, 0.14);
}

.next-layer:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

/* ---- 选择轨迹 ---- */
.selection-trail {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  max-width: 980px;
  margin: 24px auto 0;
}

.trail-item {
  position: relative;
  padding: 18px 16px;
  border: 1px solid rgba(196, 180, 154, 0.3);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.5);
  overflow: hidden;
  min-height: 56px;
}

.trail-item::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px dashed rgba(139, 111, 71, 0.12);
  pointer-events: none;
  border-radius: 1px;
}

.trail-item .vintage-postmark {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 40px;
  height: 40px;
  opacity: 0.55;
}

.trail-label {
  display: block;
  color: #8b7e60;
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  font-family: var(--font-display);
}

.trail-item strong {
  display: block;
  margin-top: 6px;
  color: #4a4333;
  font-family: var(--font-display);
  font-size: 0.95rem;
}

.trail-cta {
  grid-column: 1 / -1;
  justify-self: end;
  color: #8b6f47;
  font-family: var(--font-display);
  font-weight: 600;
  text-decoration: none;
  padding: 10px 22px;
  border: 1px solid rgba(184, 161, 110, 0.45);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
  transition: all 0.25s ease;
}

.trail-cta:hover {
  background: rgba(184, 161, 110, 0.12);
  border-color: rgba(184, 161, 110, 0.65);
  transform: translateY(-1px);
}

@media (max-width: 700px) {
  .guidance-page { padding: 24px 18px 60px; }
  .layer-map { grid-template-columns: 1fr; }
  .bubble-grid { justify-content: center; }
  .selection-trail { grid-template-columns: 1fr; }
  .trail-cta { justify-self: start; }
  .orbit-corner { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  .progress-track i { transition: none; }
  .layer-map li button, .next-layer { transition: none; }
}
</style>
