<script setup>
import { useReveal } from '../../composables/useReveal'

defineProps({
  tag: {
    type: String,
    default: 'section'
  }
})

const { target, visible } = useReveal()
</script>

<template>
  <component
    :is="tag"
    ref="target"
    class="reveal-section"
    :class="{ 'is-visible': visible }"
    :data-visible="String(visible)"
  >
    <slot />
  </component>
</template>

<style scoped>
.reveal-section {
  opacity: 0;
  transform: translateY(1.25rem);
  transition:
    opacity var(--duration-reveal) var(--ease-reveal),
    transform var(--duration-reveal) var(--ease-reveal);
}

.reveal-section.is-visible {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .reveal-section { opacity: 1; transform: none; }
}
</style>
