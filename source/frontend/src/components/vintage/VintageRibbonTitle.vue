<script setup>
const props = defineProps({
  label: { type: String, required: true }
})
</script>

<template>
  <div class="ribbon-title">
    <span class="ribbon-tail ribbon-tail-left" aria-hidden="true"></span>
    <span class="ribbon-body">{{ label }}</span>
    <span class="ribbon-tail ribbon-tail-right" aria-hidden="true"></span>
  </div>
</template>

<style scoped>
.ribbon-title {
  display: inline-flex;
  align-items: center;
  gap: 0;
  font-family: var(--font-display);
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  color: #4a4333;
  text-transform: uppercase;
}

.ribbon-body {
  position: relative;
  padding: 0.45rem 1rem;
  background: linear-gradient(180deg, #c5d1d4 0%, #b2c1c5 100%);
  border-top: 1px solid rgba(255,255,255,0.35);
  border-bottom: 1px solid rgba(107, 93, 62, 0.12);
  box-shadow: 0 2px 6px rgba(107, 93, 62, 0.08);
  white-space: nowrap;
}

.ribbon-tail {
  display: block;
  width: 0;
  height: 0;
  border-style: solid;
}

.ribbon-tail-left {
  border-width: 0 0 1.6rem 0.7rem;
  border-color: transparent transparent #9eb0b5 transparent;
}

.ribbon-tail-right {
  border-width: 1.6rem 0 0 0.7rem;
  border-color: transparent transparent transparent #9eb0b5;
}
</style>
