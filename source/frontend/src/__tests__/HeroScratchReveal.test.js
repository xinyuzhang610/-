import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HeroScratchReveal from '../components/home/HeroScratchReveal.vue'

const gradient = { addColorStop: vi.fn() }
const context = {
  clearRect: vi.fn(),
  fillRect: vi.fn(),
  beginPath: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  closePath: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  createLinearGradient: vi.fn(() => gradient),
  createRadialGradient: vi.fn(() => gradient),
  setTransform: vi.fn(),
  globalCompositeOperation: 'source-over',
  fillStyle: ''
}
const disconnect = vi.fn()
const animationFrames = []

function runNextFrame(now) {
  const callback = animationFrames.shift()
  expect(callback).toBeTypeOf('function')
  callback(now)
}

function installBrowserStubs({ reduced = false, hover = true } = {}) {
  vi.stubGlobal('matchMedia', vi.fn((query) => ({
    matches: query === '(hover: hover)' ? hover : reduced,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn()
  })))
  vi.stubGlobal('requestAnimationFrame', vi.fn((callback) => {
    animationFrames.push(callback)
    return animationFrames.length
  }))
  vi.stubGlobal('cancelAnimationFrame', vi.fn())
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    disconnect() { disconnect() }
  })
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
  vi.spyOn(performance, 'now').mockReturnValue(20)
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
    left: 0, top: 0, width: 1000, height: 700, right: 1000, bottom: 700
  })
}

describe('HeroScratchReveal', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    animationFrames.length = 0
    installBrowserStubs()
  })

  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
    animationFrames.length = 0
  })

  it('repaints the mask before carving each living ink frame', async () => {
    const wrapper = mount(HeroScratchReveal, { attachTo: document.body })
    const initialPaints = context.fillRect.mock.calls.length

    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
    })
    runNextFrame(20)

    expect(context.fillRect.mock.calls.length).toBeGreaterThan(initialPaints)
    expect(context.createRadialGradient).toHaveBeenCalled()
    expect(context.lineTo).toHaveBeenCalled()
    expect(wrapper.emitted('first-reveal')).toHaveLength(1)
    wrapper.unmount()
  })

  it('closes the revealed area after the stamp lifetime', async () => {
    const wrapper = mount(HeroScratchReveal)
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
    })
    runNextFrame(20)
    const carvedPaths = context.beginPath.mock.calls.length
    runNextFrame(541)

    expect(context.fillRect.mock.calls.length).toBeGreaterThan(2)
    expect(context.beginPath.mock.calls.length).toBe(carvedPaths)
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
    runNextFrame(20)
    const firstFrameGradients = context.createRadialGradient.mock.calls.length

    await wrapper.get('canvas').trigger('pointerleave', { pointerType: 'mouse' })
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 900, clientY: 200, timeStamp: 40
    })
    runNextFrame(40)

    expect(context.createRadialGradient.mock.calls.length - firstFrameGradients).toBeLessThanOrEqual(3)
    wrapper.unmount()
  })

  it('uses the static fallback when reduced motion is requested', async () => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
    installBrowserStubs({ reduced: true })
    const wrapper = mount(HeroScratchReveal)
    await wrapper.vm.$nextTick()

    expect(wrapper.attributes('data-static')).toBe('true')
    expect(wrapper.emitted('static-mode')).toHaveLength(1)
  })

  it('uses the static fallback when hover is unavailable', async () => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
    installBrowserStubs({ hover: false })
    const wrapper = mount(HeroScratchReveal)
    await wrapper.vm.$nextTick()

    expect(wrapper.attributes('data-static')).toBe('true')
    expect(wrapper.get('canvas').attributes('hidden')).toBeDefined()
  })

  it('cancels animation work and observers on unmount', async () => {
    const wrapper = mount(HeroScratchReveal)
    await wrapper.get('canvas').trigger('pointermove', {
      pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
    })
    wrapper.unmount()

    expect(cancelAnimationFrame).toHaveBeenCalled()
    expect(disconnect).toHaveBeenCalled()
  })
})
