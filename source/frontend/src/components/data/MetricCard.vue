<template>
  <article class="metric-card" :data-tone="tone" :aria-label="`${label}：${value}`">
    <span class="metric-mark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 17 9 12l3 3 8-9M16 6h4v4"/></svg></span>
    <div><span class="metric-label">{{ label }}</span><strong class="metric-value">{{ value }}</strong><small v-if="trend">{{ trend }}</small></div>
  </article>
</template>
<script setup>defineProps({ label:{type:String,required:true}, value:{type:[String,Number],required:true}, trend:{type:String,default:''}, tone:{type:String,default:'jade'} })</script>
<style scoped>
.metric-card {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 136px;
  padding: 22px;
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
  box-shadow: 0 4px 18px rgba(107, 93, 62, 0.05);
  position: relative;
}

.metric-card::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(139, 111, 71, 0.15);
  pointer-events: none;
  border-radius: 1px;
}

.metric-mark {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border: 1px solid rgba(138, 154, 140, 0.5);
  border-radius: 50%;
  color: #8a9a8c;
  background: rgba(138, 154, 140, 0.08);
  flex-shrink: 0;
}

.metric-mark svg {
  width: 23px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
}

.metric-label, .metric-value, .metric-card small { display: block; }

.metric-label {
  color: #6b5d3e;
  font-size: 0.78rem;
  font-family: var(--font-display);
  letter-spacing: 0.04em;
}

.metric-value {
  margin: 5px 0;
  color: #3d3526;
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 500;
}

.metric-card small {
  color: #8b6f47;
  font-size: 0.72rem;
  letter-spacing: 0.05em;
}

.metric-card[data-tone="gold"] .metric-mark {
  border-color: rgba(184, 161, 110, 0.5);
  color: #b8a16e;
  background: rgba(184, 161, 110, 0.08);
}
</style>
