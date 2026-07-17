<template>
  <div class="app-shell">
    <router-view v-slot="{ Component, route }">
      <transition name="page" mode="out-in" :disabled="prefersReducedMotion">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const prefersReducedMotion = ref(false)
let motionQuery = null

function onMotionChange(e) {
  prefersReducedMotion.value = e.matches
}

onMounted(() => {
  if (typeof window === 'undefined') return
  motionQuery = window.matchMedia?.('(prefers-reduced-motion: reduce)')
  prefersReducedMotion.value = motionQuery?.matches ?? false
  motionQuery?.addEventListener?.('change', onMotionChange) ?? motionQuery?.addListener?.(onMotionChange)
})

onBeforeUnmount(() => {
  motionQuery?.removeEventListener?.('change', onMotionChange) ?? motionQuery?.removeListener?.(onMotionChange)
})
</script>

<style>
.app-shell {
  min-height: 100vh;
  background: var(--ink-950);
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
