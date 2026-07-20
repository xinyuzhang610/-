<script setup>
defineProps({ tool: { type: Object, required: true }, hot: Boolean })
</script>

<template>
  <RouterLink class="tool-card" :to="`/tool/${tool.id}`" :aria-label="`使用工具：${tool.name}`">
    <span class="tool-card__glyph" aria-hidden="true">
      <svg viewBox="0 0 32 32"><path d="M16 3 27 9v14l-11 6L5 23V9l11-6Z"/><path d="m5 9 11 7 11-7M16 16v13"/></svg>
    </span>
    <span v-if="hot" class="tool-card__hot">热门</span>
    <span class="tool-card__category">{{ tool.category || '通用' }}</span>
    <h3>{{ tool.name }}</h3>
    <p>{{ tool.description || '等待工具创建者补充说明。' }}</p>
    <span class="tool-card__meta">使用 {{ tool.usage_count || 0 }} 次 <b>进入工具 →</b></span>
  </RouterLink>
</template>

<style scoped>
.tool-card {
  position: relative;
  display: flex;
  min-height: 240px;
  flex-direction: column;
  gap: 12px;
  padding: 24px;
  border: 1px solid rgba(196, 180, 154, 0.4);
  border-radius: 2px;
  background: linear-gradient(155deg, rgba(250, 248, 242, 0.85), rgba(237, 230, 216, 0.7));
  color: #4a4333;
  text-decoration: none;
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.06);
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

/* 虚线内边框 */
.tool-card::before {
  content: '';
  position: absolute;
  inset: 5px;
  border: 1px dashed rgba(139, 111, 71, 0.2);
  border-radius: 1px;
  pointer-events: none;
  transition: border-color 0.3s ease;
}

/* 底部卷边 */
.tool-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 24px 24px;
  border-color: transparent transparent rgba(210, 198, 168, 0.5) transparent;
  pointer-events: none;
  z-index: 2;
  transition: border-width 0.25s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
  border-color: rgba(184, 161, 110, 0.6);
  box-shadow: 0 16px 40px rgba(107, 93, 62, 0.12);
}

.tool-card:hover::after {
  border-width: 0 0 30px 30px;
}

.tool-card:hover::before {
  border-color: rgba(139, 111, 71, 0.3);
}

.tool-card__glyph {
  display: grid;
  width: 46px;
  height: 46px;
  place-items: center;
  border: 1px solid rgba(138, 154, 140, 0.5);
  border-radius: 2px;
  color: #8a9a8c;
  background: rgba(138, 154, 140, 0.06);
}

.tool-card__glyph svg {
  width: 25px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.4;
}

.tool-card__hot {
  position: absolute;
  right: 16px;
  top: 16px;
  padding: 3px 10px;
  border: 1px solid rgba(184, 161, 110, 0.5);
  border-radius: 2px;
  background: rgba(184, 161, 110, 0.15);
  color: #8b6f47;
  font-size: 0.68rem;
  font-family: var(--font-display);
  letter-spacing: 0.08em;
}

.tool-card__category {
  color: #8b6f47;
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  font-family: var(--font-display);
  text-transform: uppercase;
}

.tool-card h3 {
  font: 600 1.2rem var(--font-display);
  color: #3d3526;
  margin: 0;
}

.tool-card p {
  flex: 1;
  color: #6b5d3e;
  line-height: 1.7;
  font-size: 0.88rem;
  margin: 0;
}

.tool-card__meta {
  display: flex;
  justify-content: space-between;
  color: #8b7e60;
  font-size: 0.78rem;
  padding-top: 8px;
  border-top: 1px solid rgba(196, 180, 154, 0.25);
}

.tool-card__meta b {
  color: #8b6f47;
  font-family: var(--font-display);
}
</style>
