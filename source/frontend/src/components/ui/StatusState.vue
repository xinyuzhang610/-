<script setup>
import { computed } from 'vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  type: {
    type: String,
    default: 'empty',
    validator: (value) => ['loading', 'empty', 'error'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  retryLabel: {
    type: String,
    default: '重新尝试'
  }
})

defineEmits(['retry'])

const role = computed(() => props.type === 'error' ? 'alert' : 'status')
const live = computed(() => props.type === 'error' ? 'assertive' : 'polite')
</script>

<template>
  <section
    class="status-state"
    :class="`status-state--${type}`"
    :role="role"
    :aria-live="live"
    :aria-busy="type === 'loading' ? 'true' : undefined"
  >
    <svg class="status-state__icon" viewBox="0 0 64 64" aria-hidden="true">
      <template v-if="type === 'loading'">
        <circle class="status-state__orbit" cx="32" cy="32" r="22" />
        <circle class="status-state__accent" cx="32" cy="10" r="4" />
        <path d="M25 32h14M32 25v14" />
      </template>
      <template v-else-if="type === 'error'">
        <path d="M32 8 56 52H8L32 8Z" />
        <path d="M32 23v14M32 45h.01" />
      </template>
      <template v-else>
        <path d="M10 45c8-12 14-18 22-18s14 6 22 18" />
        <path d="M17 45V19c9 0 15 4 15 10 0-6 6-10 15-10v26" />
        <path d="M24 37h16" />
      </template>
    </svg>
    <h3 class="status-state__title">{{ title }}</h3>
    <p v-if="description" class="status-state__description">{{ description }}</p>
    <AppButton v-if="type === 'error'" variant="ghost" @click="$emit('retry')">
      {{ retryLabel }}
    </AppButton>
  </section>
</template>

<style scoped>
.status-state {
  display: grid;
  min-height: 14rem;
  place-items: center;
  align-content: center;
  gap: var(--space-sm);
  padding: var(--space-xl);
  color: var(--color-ink);
  text-align: center;
}

.status-state__icon {
  width: 4rem;
  margin-bottom: var(--space-sm);
  color: var(--color-jade);
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2.5;
}

.status-state--error .status-state__icon { color: var(--color-danger); }
.status-state--loading .status-state__icon { color: var(--color-gold); }
.status-state__accent { fill: currentColor; stroke: none; }
.status-state__orbit { animation: status-orbit 1.6s var(--ease-in-out) infinite; stroke-dasharray: 48 90; transform-origin: center; }

.status-state__title {
  font-family: var(--font-heading);
  font-size: var(--font-size-lg);
}

.status-state__description {
  max-width: 36rem;
  margin-bottom: var(--space-md);
  color: var(--color-ink-soft);
  line-height: var(--line-height-body);
}

@keyframes status-orbit { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .status-state__orbit { animation: none; }
}
</style>
