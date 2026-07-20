<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' }, // primary | secondary
  disabled: { type: Boolean, default: false },
  asChild: { type: Boolean, default: false }
})
const emit = defineEmits(['click'])
</script>

<template>
  <component
    :is="asChild ? 'span' : 'button'"
    class="vintage-button"
    :class="`is-${variant}`"
    :disabled="!asChild && disabled"
    :type="asChild ? undefined : 'button'"
    @click="emit('click', $event)"
  >
    <span class="btn-border">
      <span class="btn-inner">
        <slot />
      </span>
    </span>
  </component>
</template>

<style scoped>
.vintage-button {
  display: inline-flex;
  padding: 0;
  border: 0;
  background: transparent;
  font: inherit;
  cursor: pointer;
  color: inherit;
}

.vintage-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-border {
  display: block;
  padding: 2px;
  border-radius: 999px;
  background: linear-gradient(135deg, #b8a16e, #8b6f47);
}

.btn-inner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 1.5rem;
  border-radius: 999px;
  background: #faf8f2;
  color: #5c4f34;
  font-family: var(--font-display);
  font-size: 0.9rem;
  letter-spacing: 0.04em;
  transition: transform 0.2s ease, background 0.2s ease;
}

.vintage-button.is-primary .btn-inner {
  background: linear-gradient(180deg, #faf8f2 0%, #f2efe6 100%);
}

.vintage-button.is-secondary .btn-border {
  background: linear-gradient(135deg, #8a9a8c, #6e7d70);
}

@media (hover: hover) {
  .vintage-button:not(:disabled):hover .btn-inner {
    transform: translateY(-2px);
    background: #ffffff;
  }
}

.vintage-button:disabled .btn-inner {
  transform: none;
}
</style>
