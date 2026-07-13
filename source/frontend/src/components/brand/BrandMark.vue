<script setup>
defineProps({
  compact: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <span
    class="brand-mark"
    :class="{ 'brand-mark--compact': compact }"
    role="img"
    aria-label="智教通，智慧教育平台"
  >
    <svg class="brand-mark__seal" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
      <path class="brand-mark__seal-field" d="M13 6h38a7 7 0 0 1 7 7v38a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7V13a7 7 0 0 1 7-7Z" />
      <path class="brand-mark__circuit" d="M19 19h8v8h10v-8h8M19 45h8v-8h10v8h8M16 32h32" />
      <circle class="brand-mark__node" cx="16" cy="32" r="2.5" />
      <circle class="brand-mark__node" cx="48" cy="32" r="2.5" />
      <path class="brand-mark__spark" d="m32 13 3.2 7.1L32 25l-3.2-4.9L32 13Z" />
    </svg>
    <span class="brand-mark__copy">
      <span class="brand-mark__name">智教通</span>
      <span v-if="!compact" class="brand-mark__descriptor">知启万象 · 教联未来</span>
    </span>
  </span>
</template>

<style scoped>
.brand-mark {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--color-ink);
}

.brand-mark__seal {
  width: 3rem;
  flex: 0 0 3rem;
  filter: drop-shadow(0 0.25rem 0.5rem rgb(23 107 90 / 16%));
}

.brand-mark__seal-field {
  fill: var(--color-jade);
  stroke: var(--gold-400);
  stroke-width: 1.5;
}

.brand-mark__circuit {
  fill: none;
  stroke: var(--moon-50);
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3;
}

.brand-mark__node,
.brand-mark__spark {
  fill: var(--gold-200);
}

.brand-mark__copy {
  display: grid;
  gap: 0.05rem;
}

.brand-mark__name {
  font-family: var(--font-title);
  font-size: var(--font-size-xl);
  font-weight: 700;
  letter-spacing: 0.16em;
  line-height: var(--line-height-tight);
  white-space: nowrap;
}

.brand-mark__descriptor {
  color: var(--color-ink-soft);
  font-size: var(--font-size-xs);
  letter-spacing: 0.22em;
  white-space: nowrap;
}

.brand-mark--compact .brand-mark__seal {
  width: 2.25rem;
  flex-basis: 2.25rem;
}

.brand-mark--compact .brand-mark__name {
  font-size: var(--font-size-lg);
}

@media (max-width: 26rem) {
  .brand-mark:not(.brand-mark--compact) { gap: var(--space-xs); }
  .brand-mark:not(.brand-mark--compact) .brand-mark__seal {
    width: 2.5rem;
    flex-basis: 2.5rem;
  }
  .brand-mark:not(.brand-mark--compact) .brand-mark__name { font-size: var(--font-size-lg); }
  .brand-mark:not(.brand-mark--compact) .brand-mark__descriptor { display: none; }
}
</style>
