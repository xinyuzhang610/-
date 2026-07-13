<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'jade',
    validator: (value) => ['gold', 'jade', 'ghost'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  }
})

const emit = defineEmits(['click'])

function handleClick(event) {
  if (props.disabled || props.loading) return
  emit('click', event)
}
</script>

<template>
  <button
    class="app-button"
    :class="[`app-button--${variant}`, { 'app-button--loading': loading }]"
    :type="type"
    :disabled="disabled || loading"
    :aria-busy="loading ? 'true' : undefined"
    @click="handleClick"
  >
    <span v-if="$slots.leading" class="app-button__icon" aria-hidden="true"><slot name="leading" /></span>
    <span class="app-button__label"><slot /></span>
    <span v-if="loading" class="app-button__progress" role="status">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="8" />
      </svg>
      <span class="app-button__sr-only">处理中</span>
    </span>
    <span v-else-if="$slots.trailing" class="app-button__icon" aria-hidden="true"><slot name="trailing" /></span>
  </button>
</template>

<style scoped>
.app-button {
  position: relative;
  display: inline-flex;
  min-width: 2.75rem;
  min-height: 2.75rem;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: 0.65rem 1.25rem;
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  font-family: var(--font-ui);
  font-size: var(--font-size-base);
  font-weight: 650;
  letter-spacing: 0.04em;
  line-height: 1.2;
  touch-action: manipulation;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out);
}

.app-button--jade {
  background: var(--color-jade);
  color: var(--moon-50);
  box-shadow: var(--shadow-jade);
}

.app-button--gold {
  background: var(--gold-600);
  color: var(--moon-50);
  box-shadow: 0 0.75rem 1.75rem rgb(157 108 29 / 20%);
}

.app-button--ghost {
  border-color: var(--color-border);
  background: var(--material-paper);
  color: var(--color-jade);
}

.app-button:hover:not(:disabled) {
  transform: translateY(-1px);
  filter: brightness(1.05);
}

.app-button:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

.app-button:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 3px;
}

.app-button:disabled {
  cursor: not-allowed;
  opacity: 0.48;
  box-shadow: none;
}

.app-button__icon {
  display: inline-grid;
  width: 1.25rem;
  place-items: center;
}

.app-button__progress {
  display: inline-grid;
  width: 1.25rem;
  height: 1.25rem;
  place-items: center;
}

.app-button__progress svg {
  width: 100%;
  animation: app-button-spin 0.8s linear infinite;
}

.app-button__progress circle {
  fill: none;
  stroke: currentColor;
  stroke-dasharray: 32 18;
  stroke-linecap: round;
  stroke-width: 2.5;
}

.app-button__sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  white-space: nowrap;
}

@keyframes app-button-spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .app-button__progress svg { animation: none; }
  .app-button:hover:not(:disabled),
  .app-button:active:not(:disabled) { transform: none; }
}
</style>
