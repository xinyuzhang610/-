import { computed, onScopeDispose, ref } from 'vue'

export function useMotionPreference() {
  const reduced = ref(false)
  const prefersReducedMotion = reduced
  const canAnimate = computed(() => !reduced.value)

  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return { reduced, canAnimate, prefersReducedMotion }
  }

  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  const updatePreference = (event) => {
    reduced.value = event.matches
  }

  reduced.value = mediaQuery.matches

  if (typeof mediaQuery.addEventListener === 'function') {
    mediaQuery.addEventListener('change', updatePreference)
    onScopeDispose(() => mediaQuery.removeEventListener('change', updatePreference))
  } else if (typeof mediaQuery.addListener === 'function') {
    mediaQuery.addListener(updatePreference)
    onScopeDispose(() => mediaQuery.removeListener(updatePreference))
  }

  return { reduced, canAnimate, prefersReducedMotion }
}
