<script setup>
defineProps({ label: { type: String, required: true }, selected: Boolean, index: { type: Number, default: 0 } })
defineEmits(['select'])
</script>

<template>
  <button class="interest-bubble" type="button" :aria-pressed="selected" :style="{ '--i': index }" @click="$emit('select')">
    <svg class="bubble-svg" viewBox="0 0 64 64" aria-hidden="true">
      <circle cx="32" cy="32" r="26" fill="none" />
      <circle cx="32" cy="32" r="22" fill="none" stroke-dasharray="3 2" opacity="0.4" />
      <path d="M18 36c8-14 20-14 28 0" fill="none" />
      <circle cx="23" cy="26" r="1.5" fill="currentColor" opacity="0.6" />
      <circle cx="41" cy="26" r="1.5" fill="currentColor" opacity="0.6" />
    </svg>
    <span>{{ label }}</span>
  </button>
</template>

<style scoped>
.interest-bubble {
  position: relative;
  display: grid;
  min-width: 116px;
  min-height: 116px;
  place-items: center;
  align-content: center;
  gap: 6px;
  padding: 16px;
  border: 1.5px solid rgba(184, 161, 110, 0.45);
  border-radius: 50%;
  background:
    radial-gradient(circle at 38% 25%, rgba(255, 252, 247, 0.95), transparent 45%),
    radial-gradient(circle at 60% 70%, rgba(138, 154, 140, 0.08), transparent 40%),
    linear-gradient(160deg, #faf7f0, #f0ebe0 60%, #e6dfcf);
  color: #4a4333;
  font: 600 0.88rem var(--font-display);
  box-shadow:
    0 6px 24px rgba(107, 93, 62, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -2px 4px rgba(107, 93, 62, 0.04);
  cursor: pointer;
  animation: drift 5s ease-in-out infinite;
  animation-delay: calc(var(--i, 0) * -600ms);
  transition: transform 0.3s ease, border-color 0.25s ease, box-shadow 0.3s ease;
}

/* 内圈虚线 */
.interest-bubble::before {
  content: '';
  position: absolute;
  top: 8px; left: 8px; right: 8px; bottom: 8px;
  border: 1px dashed rgba(139, 111, 71, 0.2);
  border-radius: 50%;
  pointer-events: none;
  transition: border-color 0.25s ease;
}

/* 底部卷边 */
.interest-bubble::after {
  content: '';
  position: absolute;
  bottom: 4px;
  right: 12px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 14px 14px;
  border-color: transparent transparent rgba(210, 198, 168, 0.55) transparent;
  pointer-events: none;
}

.bubble-svg {
  width: 32px;
  fill: none;
  stroke: #8b6f47;
  stroke-width: 1.5;
  stroke-linecap: round;
  transition: stroke 0.25s ease;
}

.interest-bubble:hover {
  transform: translateY(-8px) scale(1.04);
  border-color: rgba(184, 161, 110, 0.7);
  box-shadow:
    0 14px 36px rgba(107, 93, 62, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.interest-bubble:hover .bubble-svg {
  stroke: #5c4f34;
}

.interest-bubble[aria-pressed="true"] {
  border-color: #8a9a8c;
  background:
    radial-gradient(circle at 38% 25%, rgba(255, 252, 247, 1), transparent 45%),
    radial-gradient(circle at 60% 70%, rgba(138, 154, 140, 0.15), transparent 40%),
    linear-gradient(160deg, #faf8f2, #ece6d7 60%, #e2dac8);
  box-shadow:
    0 0 0 3px rgba(138, 154, 140, 0.18),
    0 12px 34px rgba(107, 93, 62, 0.13),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.interest-bubble[aria-pressed="true"] .bubble-svg {
  stroke: #6e7d70;
}

@keyframes drift {
  50% { translate: 0 -8px; }
}

@media (prefers-reduced-motion: reduce) {
  .interest-bubble { animation: none; }
  .interest-bubble:hover { transform: none; }
}
</style>
