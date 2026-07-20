<script setup>
const props = defineProps({
  step: { type: Number, required: true },
  status: { type: String, default: 'pending' } // pending | active | complete
})
</script>

<template>
  <div class="step-badge" :class="`is-${status}`" aria-hidden="true">
    <svg class="badge-bg" viewBox="0 0 80 80">
      <!-- 鼠尾草绿做旧底 -->
      <circle cx="40" cy="40" r="36" fill="#8a9a8c" opacity="0.18" />
      <circle cx="40" cy="40" r="32" fill="none" stroke="#d4c8a5" stroke-width="1.5" stroke-dasharray="4 3" />
      <!-- 迷你卷草边角 -->
      <path d="M14 20c4-4 8-2 10 2s-2 8-6 6" fill="none" stroke="#b8a16e" stroke-width="1.2" />
      <path d="M66 60c-4 4-8 2-10-2s2-8 6-6" fill="none" stroke="#b8a16e" stroke-width="1.2" />
      <!-- 燕子剪影 -->
      <path d="M56 22c-4 2-8 6-8 10 0-4-4-8-8-10 4 2 6 4 8 6 2-2 4-4 8-6z" fill="#8b6f47" opacity="0.7" />
    </svg>
    <span class="step-number">{{ status === 'complete' ? '✓' : step }}</span>
  </div>
</template>

<style scoped>
.step-badge {
  position: relative;
  width: 64px;
  height: 64px;
  flex: 0 0 64px;
  display: grid;
  place-items: center;
}

.badge-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-6deg);
}

.step-number {
  position: relative;
  z-index: 1;
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 500;
  color: #6b5d3e;
  line-height: 1;
}

.step-badge.is-active .badge-bg {
  transform: rotate(0deg) scale(1.06);
}

.step-badge.is-active .step-number {
  color: #8b6f47;
  font-weight: 700;
}

.step-badge.is-complete circle:first-child {
  fill: #b8a16e;
  opacity: 0.22;
}

.step-badge.is-complete circle:nth-child(2) {
  stroke: #b8a16e;
}

.step-badge.is-complete .step-number {
  color: #8b6f47;
}
</style>
