import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HeroScratchReveal from '../components/home/HeroScratchReveal.vue'

const gradient = { addColorStop: vi.fn() }
const context = {
  clearRect: vi.fn(),
  fillRect: vi.fn(),
  beginPath: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  createLinearGradient: vi.fn(() => gradient),
  createRadialGradient: vi.fn(() => gradient),
  setTransform: vi.fn(),
  globalCompositeOperation: 'source-over',
  fillStyle: ''
}
const disconnect = vi.fn()

function installBrowserStubs(reduced = false) {
  vi.stubGlobal('matchMedia', vi.fn(() => ({
    matches: reduced,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn()
  })))
  vi.stubGlobal('requestAnimationFrame', vi.fn((callback) => {
    callback()
    return 0
  }))
  vi.stubGlobal('cancelAnimationFrame', vi.fn())
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    disconnect() { disconnect() }
  })
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
    left: 0, top: 0, width: 1000, height: 700, right: 1000, bottom: 700
  })
}

describe('HeroScratchReveal', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    installBrowserStubs(false)
  })
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('paints a mask and erases it after desktop pointer movement', async () => {
    const wrapper = mount(HeroScratchReveal, { attachTo: document.body })
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
    })

    expect(context.fillRect).toHaveBeenCalled()
    expect(context.globalCompositeOperation).toBe('destination-out')
    expect(context.arc).toHaveBeenCalled()
    expect(wrapper.emitted('first-reveal')).toHaveLength(1)
    wrapper.unmount()
  })

  it('removes the visual mask when skipped', async () => {
    const wrapper = mount(HeroScratchReveal, { props: { skipped: false } })
    await wrapper.setProps({ skipped: true })

    expect(wrapper.get('canvas').attributes('hidden')).toBeDefined()
  })

  it('does not bridge untouched space after the pointer leaves and re-enters', async () => {
    const wrapper = mount(HeroScratchReveal)
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 100, clientY: 200, timeStamp: 20
    })
    const firstStrokeCalls = context.arc.mock.calls.length

    await wrapper.get('canvas').trigger('pointerleave', { pointerType: 'mouse' })
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 900, clientY: 200, timeStamp: 40
    })

    expect(context.arc.mock.calls.length - firstStrokeCalls).toBe(1)
  })

  it('uses the static fallback when reduced motion is requested', async () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: true,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    })))
    const wrapper = mount(HeroScratchReveal)
    await wrapper.vm.$nextTick()

    expect(wrapper.attributes('data-static')).toBe('true')
    expect(wrapper.emitted('static-mode')).toHaveLength(1)
  })

  it('cancels animation work and observers on unmount', () => {
    const wrapper = mount(HeroScratchReveal)
    wrapper.unmount()

    expect(cancelAnimationFrame).toHaveBeenCalled()
    expect(disconnect).toHaveBeenCalled()
  })
})
