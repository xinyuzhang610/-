import {
  getCurrentInstance,
  getCurrentScope,
  onBeforeUnmount,
  onMounted,
  ref,
  watch
} from 'vue'
import { useMotionPreference } from './useMotionPreference'

export function useReveal() {
  const target = ref(null)
  const visible = ref(false)

  if (!getCurrentInstance() || !getCurrentScope()) {
    visible.value = true
    return { target, visible }
  }

  const { canAnimate } = useMotionPreference()
  let observer

  const reveal = () => {
    visible.value = true
  }

  onMounted(() => {
    if (
      !canAnimate.value
      || typeof window === 'undefined'
      || typeof window.IntersectionObserver !== 'function'
    ) {
      reveal()
      return
    }

    observer = new window.IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) reveal()
    }, { threshold: 0.18 })

    if (target.value) observer.observe(target.value)
  })

  watch(canAnimate, (allowed) => {
    if (!allowed) reveal()
  })

  onBeforeUnmount(() => {
    observer?.disconnect()
  })

  return { target, visible }
}
