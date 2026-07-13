<script setup>
defineProps({ tool: { type: Object, required: true }, hot: Boolean })
</script>

<template>
  <RouterLink class="tool-card" :to="`/tool/${tool.id}`" :aria-label="`使用工具：${tool.name}`">
    <span class="tool-card__glyph" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M16 3 27 9v14l-11 6L5 23V9l11-6Z"/><path d="m5 9 11 7 11-7M16 16v13"/></svg></span>
    <span v-if="hot" class="tool-card__hot">热门</span>
    <span class="tool-card__category">{{ tool.category || '通用' }}</span>
    <h3>{{ tool.name }}</h3>
    <p>{{ tool.description || '等待工具创建者补充说明。' }}</p>
    <span class="tool-card__meta">使用 {{ tool.usage_count || 0 }} 次 <b>进入工具 →</b></span>
  </RouterLink>
</template>

<style scoped>
.tool-card{position:relative;display:flex;min-height:240px;flex-direction:column;gap:12px;padding:24px;border:1px solid rgb(203 211 201 / 18%);border-radius:var(--radius-xl);background:linear-gradient(145deg,rgb(255 255 255 / 7%),rgb(66 185 154 / 4%));color:var(--moon-50);text-decoration:none;box-shadow:inset 0 0 34px rgb(66 185 154 / 5%);transition:transform var(--duration-normal),border-color var(--duration-normal),box-shadow var(--duration-normal)}.tool-card:hover{transform:translateY(-6px);border-color:rgb(213 166 79 / 55%);box-shadow:0 22px 48px rgb(0 0 0 / 20%)}.tool-card__glyph{display:grid;width:46px;height:46px;place-items:center;border:1px solid var(--jade-400);border-radius:14px;color:var(--jade-400)}.tool-card__glyph svg{width:25px;fill:none;stroke:currentColor;stroke-width:1.4}.tool-card__hot{position:absolute;right:18px;top:18px;padding:4px 9px;border-radius:99px;background:var(--gold-400);color:var(--ink-950);font-size:.7rem}.tool-card__category{color:var(--gold-300);font-size:.72rem;letter-spacing:.16em}.tool-card h3{font:600 1.2rem var(--font-heading)}.tool-card p{flex:1;color:var(--moon-300);line-height:1.7}.tool-card__meta{display:flex;justify-content:space-between;color:var(--ink-300);font-size:.78rem}.tool-card__meta b{color:var(--jade-200)}
</style>
