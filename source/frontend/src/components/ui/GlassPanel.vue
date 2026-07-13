<script setup>
defineProps({
  tag: {
    type: String,
    default: 'div'
  }
})
</script>

<template>
  <component :is="tag" class="glass-panel">
    <slot />
  </component>
</template>

<style scoped>
.glass-panel {
  position: relative;
  overflow: hidden;
  border: var(--material-border);
  border-radius: var(--radius-xl);
  background: var(--material-panel);
  box-shadow: var(--shadow-md);
  backdrop-filter: var(--material-blur);
}

.glass-panel::before {
  position: absolute;
  inset: 0.4rem;
  border: 1px solid var(--effect-panel-inlay);
  border-radius: calc(var(--radius-xl) - 0.4rem);
  content: '';
  pointer-events: none;
}

@supports not (backdrop-filter: blur(1px)) {
  .glass-panel { background: var(--material-paper); }
}
</style>
