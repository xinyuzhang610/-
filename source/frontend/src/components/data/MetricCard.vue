<template>
  <article class="metric-card" :data-tone="tone" :aria-label="`${label}：${value}`">
    <span class="metric-mark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 17 9 12l3 3 8-9M16 6h4v4"/></svg></span>
    <div><span class="metric-label">{{ label }}</span><strong class="metric-value">{{ value }}</strong><small v-if="trend">{{ trend }}</small></div>
  </article>
</template>
<script setup>defineProps({ label:{type:String,required:true}, value:{type:[String,Number],required:true}, trend:{type:String,default:''}, tone:{type:String,default:'jade'} })</script>
<style scoped>
.metric-card{display:flex;align-items:center;gap:16px;min-height:136px;padding:22px;border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel-dark);box-shadow:inset 0 0 36px var(--effect-jade-soft)}.metric-mark{display:grid;place-items:center;width:46px;height:46px;border:1px solid var(--jade-400);border-radius:50%;color:var(--jade-400)}.metric-mark svg{width:23px;fill:none;stroke:currentColor;stroke-width:1.6}.metric-label,.metric-value,.metric-card small{display:block}.metric-label{color:var(--moon-300);font-size:.78rem}.metric-value{margin:5px 0;color:var(--moon-50);font-family:var(--font-display);font-size:2.2rem}.metric-card small{color:var(--gold-300)}.metric-card[data-tone="gold"]{box-shadow:inset 0 0 36px var(--effect-gold-soft)}.metric-card[data-tone="gold"] .metric-mark{border-color:var(--gold-400);color:var(--gold-300)}
</style>
