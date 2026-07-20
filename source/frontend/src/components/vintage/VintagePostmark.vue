<script setup>
const props = defineProps({
  text: { type: String, default: 'APPROVED' }
})
</script>

<template>
  <div class="vintage-postmark" aria-hidden="true">
    <svg viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3 2" />
      <circle cx="32" cy="32" r="22" fill="none" stroke="currentColor" stroke-width="0.6" />
      <path id="textPath" d="M32 12a20 20 0 1 1 0 40a20 20 0 1 1 0-40" fill="none" />
      <text fill="currentColor" font-size="6.5" font-family="var(--font-display)" letter-spacing="1.5">
        <textPath href="#textPath" startOffset="50%" text-anchor="middle">{{ text }}</textPath>
      </text>
    </svg>
  </div>
</template>

<style scoped>
.vintage-postmark {
  width: 52px;
  height: 52px;
  color: #8b6f47;
  opacity: 0.75;
  transform: rotate(-12deg);
}

.vintage-postmark svg {
  width: 100%;
  height: 100%;
}
</style>
