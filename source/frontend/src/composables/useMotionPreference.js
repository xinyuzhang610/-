import { computed, onScopeDispose, ref } from 'vue'

export function useMotionPreference() {
  const prefersReducedMotion = ref(false)
  const canAnimate = computed(() => !prefersReducedMotion.value)

  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return { canAnimate, prefersReducedMotion }
  }

  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  const updatePreference = (event) => {
    prefersReducedMotion.value = event.matches
  }

  prefersReducedMotion.value = mediaQuery.matches

  if (typeof mediaQuery.addEventListener === 'function') {
    mediaQuery.addEventListener('change', updatePreference)
    onScopeDispose(() => mediaQuery.removeEventListener('change', updatePreference))
  } else if (typeof mediaQuery.addListener === 'function') {
    mediaQuery.addListener(updatePreference)
    onScopeDispose(() => mediaQuery.removeListener(updatePreference))
  }

  return { canAnimate, prefersReducedMotion }
}
