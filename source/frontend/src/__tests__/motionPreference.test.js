import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, effectScope, h, nextTick } from 'vue'
import { mount } from '@vue/test-utils'
import { useMotionPreference } from '../composables/useMotionPreference'
import { useReveal } from '../composables/useReveal'

describe('useMotionPreference', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('disables animation when reduced motion is preferred', () => {
    const addEventListener = vi.fn()
    const removeEventListener = vi.fn()
    let changeHandler
    const matchMedia = vi.fn(() => ({
      matches: true,
      addEventListener: vi.fn((event, handler) => {
        addEventListener(event, handler)
        changeHandler = handler
      }),
      removeEventListener
    }))
    vi.stubGlobal('matchMedia', matchMedia)

    const scope = effectScope()
    const preference = scope.run(() => useMotionPreference())

    expect(preference.reduced.value).toBe(true)
    expect(preference.canAnimate.value).toBe(false)
    expect(matchMedia).toHaveBeenCalledWith('(prefers-reduced-motion: reduce)')
    expect(addEventListener).toHaveBeenCalledWith('change', expect.any(Function))

    changeHandler({ matches: false })
    expect(preference.reduced.value).toBe(false)
    expect(preference.canAnimate.value).toBe(true)

    scope.stop()
    expect(removeEventListener).toHaveBeenCalledWith('change', expect.any(Function))
  })

  it('defaults to allowing animation when matchMedia is unavailable', () => {
    vi.stubGlobal('matchMedia', undefined)

    const scope = effectScope()
    const preference = scope.run(() => useMotionPreference())

    expect(preference.canAnimate.value).toBe(true)
    scope.stop()
  })
})

describe('useReveal', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('reveals an observed target and disconnects on unmount', async () => {
    let callback
    const observe = vi.fn()
    const disconnect = vi.fn()
    const IntersectionObserver = vi.fn((observerCallback) => {
      callback = observerCallback
      return { observe, disconnect }
    })
    vi.stubGlobal('IntersectionObserver', IntersectionObserver)
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    })))

    const component = defineComponent({
      setup() {
        return useReveal()
      },
      render() {
        return h('div', { ref: 'target' }, String(this.visible))
      }
    })
    const wrapper = mount(component)

    expect(IntersectionObserver).toHaveBeenCalledWith(expect.any(Function), { threshold: 0.18 })
    expect(observe).toHaveBeenCalledWith(wrapper.element)

    callback([{ isIntersecting: true }])
    await nextTick()
    expect(wrapper.text()).toBe('true')

    wrapper.unmount()
    expect(disconnect).toHaveBeenCalledOnce()
  })

  it('reveals immediately when IntersectionObserver is unavailable', async () => {
    Object.defineProperty(window, 'IntersectionObserver', {
      configurable: true,
      value: undefined
    })
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    })))

    const component = defineComponent({
      setup() {
        return useReveal()
      },
      render() {
        return h('div', { ref: 'target' }, String(this.visible))
      }
    })
    const wrapper = mount(component)

    await nextTick()
    expect(wrapper.text()).toBe('true')
    wrapper.unmount()
  })
})
