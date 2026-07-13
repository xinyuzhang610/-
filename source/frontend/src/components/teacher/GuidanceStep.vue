<template>
  <section class="guidance-step" :class="`is-${status}`" :aria-labelledby="headingId">
    <div class="step-index" aria-hidden="true">0{{ step }}</div>
    <div class="step-body"><span class="step-status">{{ statusLabel }}</span><h2 :id="headingId">{{ title }}</h2><slot /></div>
  </section>
</template>
<script setup>
import { computed, useId } from 'vue'
const props=defineProps({ step:{type:Number,required:true}, title:{type:String,required:true}, status:{type:String,default:'pending'} })
const headingId=`guidance-${useId()}`
const statusLabel=computed(()=>({active:'正在进行',complete:'已完成',pending:'等待选择'}[props.status]||props.status))
</script>
<style scoped>
.guidance-step{display:grid;grid-template-columns:72px 1fr;gap:20px;padding:22px 0;border-top:1px solid var(--color-border);opacity:.58}.guidance-step.is-active,.guidance-step.is-complete{opacity:1}.step-index{font-family:var(--font-display);font-size:2.3rem;color:var(--gold-400)}.step-status{color:var(--jade-400);font-size:.7rem;letter-spacing:.14em}.step-body h2{margin:5px 0 16px;color:var(--moon-50);font-family:var(--font-display);font-size:clamp(1.5rem,3vw,2.4rem)}@media(max-width:600px){.guidance-step{grid-template-columns:48px 1fr}.step-index{font-size:1.6rem}}
</style>

