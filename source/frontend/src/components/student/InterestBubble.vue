<script setup>
defineProps({ label: { type: String, required: true }, selected: Boolean, index: { type: Number, default: 0 } })
defineEmits(['select'])
</script>

<template>
  <button class="interest-bubble" type="button" :aria-pressed="selected" :style="{ '--i': index }" @click="$emit('select')">
    <svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="25"/><path d="M18 34c8-14 20-14 28 0M24 25h.01M40 25h.01"/></svg>
    <span>{{ label }}</span>
  </button>
</template>

<style scoped>
.interest-bubble{position:relative;display:grid;min-width:108px;min-height:108px;place-items:center;align-content:center;gap:8px;padding:14px;border:1px solid rgb(213 166 79 / 45%);border-radius:50%;background:radial-gradient(circle at 35% 28%,rgb(248 250 245 / 22%),rgb(23 107 90 / 16%) 38%,rgb(16 25 22 / 84%));color:var(--moon-50);font:600 .88rem var(--font-ui);box-shadow:inset 0 0 24px rgb(66 185 154 / 12%),0 14px 40px rgb(0 0 0 / 18%);cursor:pointer;animation:drift 5s ease-in-out infinite;animation-delay:calc(var(--i) * -600ms);transition:transform var(--duration-normal),border-color var(--duration-fast),box-shadow var(--duration-normal)}
.interest-bubble svg{width:30px;fill:none;stroke:var(--gold-300);stroke-width:1.7;stroke-linecap:round}.interest-bubble:hover{transform:translateY(-7px) scale(1.03)}.interest-bubble[aria-pressed="true"]{border-color:var(--jade-400);box-shadow:0 0 0 3px rgb(66 185 154 / 22%),0 16px 46px rgb(66 185 154 / 22%)}
@keyframes drift{50%{translate:0 -8px}}@media(prefers-reduced-motion:reduce){.interest-bubble{animation:none}.interest-bubble:hover{transform:none}}
</style>
