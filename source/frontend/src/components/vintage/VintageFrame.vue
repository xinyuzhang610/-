<script setup>
const props = defineProps({
  tone: { type: String, default: 'gold' } // gold | brown
})
</script>

<template>
  <div class="vintage-frame" :class="`is-${tone}`">
    <svg class="frame-svg" viewBox="0 0 200 200" preserveAspectRatio="none" aria-hidden="true">
      <path
        d="M10 30c10-10 20-15 30-15h120c10 0 20 5 30 15v140c-10 10-20 15-30 15h-120c-10 0-20-5-30-15z"
        fill="none"
        stroke="currentColor"
        stroke-width="1.2"
      />
      <path
        d="M18 38c8-8 16-12 24-12h116c8 0 16 4 24 12v124c-8 8-16 12-24 12h-116c-8 0-16-4-24-12z"
        fill="none"
        stroke="currentColor"
        stroke-width="0.6"
        stroke-dasharray="2 2"
      />
      <!-- 四角花饰 -->
      <path d="M10 30c5 0 10-5 10-10M10 170c5 0 10 5 10 10M190 30c-5 0-10-5-10-10M190 170c-5 0-10 5-10 10" stroke="currentColor" stroke-width="1" fill="none" />
    </svg>
    <div class="frame-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.vintage-frame {
  position: relative;
  padding: 1rem;
}

.vintage-frame.is-gold {
  color: #b8a16e;
}

.vintage-frame.is-brown {
  color: #8b6f47;
}

.frame-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.7;
}

.frame-content {
  position: relative;
  z-index: 1;
  padding: 1rem 1.25rem;
}
</style>
