<script setup>
const props = defineProps({
  variant: { type: String, default: 'parchment' } // parchment | sage | blue
})
</script>

<template>
  <div class="vintage-textbox" :class="`is-${variant}`">
    <svg class="corner corner-tl" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M2 10c4-2 10-2 12-8M10 2c-2 4-2 10-8 12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>
    <svg class="corner corner-tr" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M22 10c-4-2-10-2-12-8M14 2c2 4 2 10 8 12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>
    <svg class="corner corner-bl" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M2 14c4 2 10 2 12 8M10 22c-2-4-2-10-8-12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>
    <svg class="corner corner-br" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M22 14c-4 2-10 2-12 8M14 22c2-4 2-10 8-12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>
    <div class="textbox-inner">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.vintage-textbox {
  position: relative;
  padding: 1px;
  border-radius: 2px;
  background:
    radial-gradient(circle at 12% 15%, rgba(139, 111, 71, 0.04), transparent 35%),
    radial-gradient(circle at 88% 85%, rgba(139, 111, 71, 0.04), transparent 35%);
}

.vintage-textbox.is-parchment {
  background-color: #faf8f2;
  border: 1px solid #d8d0b8;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.6), 0 4px 14px rgba(107, 93, 62, 0.08);
}

.vintage-textbox.is-sage {
  background-color: rgba(138, 154, 140, 0.12);
  border: 1px solid rgba(138, 154, 140, 0.35);
}

.vintage-textbox.is-blue {
  background-color: rgba(197, 209, 212, 0.22);
  border: 1px solid rgba(139, 157, 162, 0.35);
}

.textbox-inner {
  position: relative;
  z-index: 1;
  padding: 1.1rem 1.25rem;
}

.corner {
  position: absolute;
  width: 18px;
  height: 18px;
  color: #b8a16e;
  opacity: 0.65;
  z-index: 2;
}

.corner-tl { top: 6px; left: 6px; }
.corner-tr { top: 6px; right: 6px; transform: rotate(90deg); }
.corner-bl { bottom: 6px; left: 6px; transform: rotate(-90deg); }
.corner-br { bottom: 6px; right: 6px; transform: rotate(180deg); }
</style>
