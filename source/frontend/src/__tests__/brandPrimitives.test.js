import { afterEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import AppButton from '../components/ui/AppButton.vue'
import BrandMark from '../components/brand/BrandMark.vue'
import GlassPanel from '../components/ui/GlassPanel.vue'
import InkLandscape from '../components/brand/InkLandscape.vue'
import KnowledgeCore from '../components/brand/KnowledgeCore.vue'
import RevealSection from '../components/motion/RevealSection.vue'
import StatusState from '../components/ui/StatusState.vue'

function stubMotionPreference(matches = false) {
  vi.stubGlobal('matchMedia', vi.fn(() => ({
    matches,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn()
  })))
}

function createRafQueue() {
  let nextId = 0
  const callbacks = new Map()
  const requestAnimationFrame = vi.fn((callback) => {
    const id = ++nextId
    callbacks.set(id, callback)
    return id
  })
  const cancelAnimationFrame = vi.fn((id) => callbacks.delete(id))
  vi.stubGlobal('requestAnimationFrame', requestAnimationFrame)
  vi.stubGlobal('cancelAnimationFrame', cancelAnimationFrame)

  return {
    callbacks,
    cancelAnimationFrame,
    requestAnimationFrame,
    runNext(time = 16) {
      const entry = callbacks.entries().next().value
      if (!entry) return false
      const [id, callback] = entry
      callbacks.delete(id)
      callback(time)
      return true
    }
  }
}

function createCanvasContext() {
  return {
    arc: vi.fn(),
    beginPath: vi.fn(),
    clearRect: vi.fn(),
    createRadialGradient: vi.fn(() => ({ addColorStop: vi.fn() })),
    fill: vi.fn(),
    lineTo: vi.fn(),
    moveTo: vi.fn(),
    setTransform: vi.fn(),
    stroke: vi.fn()
  }
}

describe('brand primitives', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('renders the canonical brand name and an accessible original SVG mark', () => {
    const wrapper = mount(BrandMark)

    expect(wrapper.text()).toContain('智教通')
    expect(wrapper.get('svg').attributes('aria-hidden')).toBe('true')
    expect(wrapper.get('.brand-mark').attributes('aria-label')).toContain('智教通')
    expect(wrapper.find('.brand-mark__name').exists()).toBe(true)
  })

  it('supports compact brand presentation without removing its accessible name', () => {
    const wrapper = mount(BrandMark, { props: { compact: true } })

    expect(wrapper.classes()).toContain('brand-mark--compact')
    expect(wrapper.get('.brand-mark').attributes('aria-label')).toContain('智教通')
  })

  it('renders a native button and emits a click exactly once', async () => {
    const wrapper = mount(AppButton, {
      props: { type: 'submit', variant: 'jade' },
      slots: { default: '开始学习' }
    })

    const button = wrapper.get('button')
    expect(button.attributes('type')).toBe('submit')
    expect(button.classes()).toContain('app-button')
    expect(button.classes()).toContain('app-button--jade')

    await button.trigger('click')
    expect(wrapper.emitted('click')).toHaveLength(1)
  })

  it.each([
    ['disabled', { disabled: true }],
    ['loading', { loading: true }]
  ])('prevents action while %s', async (_state, props) => {
    const wrapper = mount(AppButton, {
      props,
      slots: { default: '提交' }
    })
    const button = wrapper.get('button')

    expect(button.attributes()).toHaveProperty('disabled')
    await button.trigger('click')
    expect(wrapper.emitted('click')).toBeUndefined()
  })

  it('announces a loading button accessibly', () => {
    const wrapper = mount(AppButton, {
      props: { loading: true },
      slots: { default: '保存课程' }
    })

    expect(wrapper.get('button').attributes('aria-busy')).toBe('true')
    expect(wrapper.get('[role="status"]').text()).toContain('处理中')
  })

  it('renders glass content with the requested semantic tag', () => {
    const wrapper = mount(GlassPanel, {
      props: { tag: 'article' },
      slots: { default: '<p>课程内容</p>' }
    })

    expect(wrapper.element.tagName).toBe('ARTICLE')
    expect(wrapper.classes()).toContain('glass-panel')
    expect(wrapper.text()).toContain('课程内容')
  })

  it('uses alert semantics and emits retry from the error state', async () => {
    const wrapper = mount(StatusState, {
      props: {
        type: 'error',
        title: '内容加载失败',
        description: '请检查网络后重试'
      }
    })

    expect(wrapper.attributes('role')).toBe('alert')
    expect(wrapper.text()).toContain('内容加载失败')
    await wrapper.get('button').trigger('click')
    expect(wrapper.emitted('retry')).toHaveLength(1)
  })

  it('mounts a polished static knowledge core when motion and Canvas APIs are unavailable', async () => {
    stubMotionPreference(true)
    vi.stubGlobal('ResizeObserver', undefined)
    const getContext = vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(null)

    const wrapper = mount(KnowledgeCore)
    await nextTick()

    expect(wrapper.find('canvas').exists()).toBe(false)
    expect(wrapper.get('.knowledge-core__fallback').element.tagName).toBe('svg')
    expect(wrapper.attributes('aria-hidden')).toBe('true')
    expect(getContext).not.toHaveBeenCalled()
    getContext.mockRestore()
  })

  it('falls back when Canvas 2D is unsupported', async () => {
    stubMotionPreference(false)
    const getContext = vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(null)

    const wrapper = mount(KnowledgeCore)
    await nextTick()
    await nextTick()

    expect(getContext).toHaveBeenCalledWith('2d')
    expect(wrapper.find('canvas').exists()).toBe(false)
    expect(wrapper.find('.knowledge-core__fallback').exists()).toBe(true)
    getContext.mockRestore()
  })

  it('cleans every animated knowledge core run during rapid motion changes', async () => {
    let motionHandler
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn((_event, handler) => { motionHandler = handler }),
      removeEventListener: vi.fn()
    })))
    vi.stubGlobal('devicePixelRatio', 3)
    const context = {
      arc: vi.fn(),
      beginPath: vi.fn(),
      clearRect: vi.fn(),
      createRadialGradient: vi.fn(() => ({ addColorStop: vi.fn() })),
      fill: vi.fn(),
      lineTo: vi.fn(),
      moveTo: vi.fn(),
      setTransform: vi.fn(),
      stroke: vi.fn()
    }
    const getContext = vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
    const observers = []
    vi.stubGlobal('ResizeObserver', vi.fn(function ResizeObserver() {
      const observer = { observe: vi.fn(), disconnect: vi.fn() }
      observers.push(observer)
      return observer
    }))
    let rafId = 0
    const requestAnimationFrame = vi.fn(() => ++rafId)
    const cancelAnimationFrame = vi.fn()
    vi.stubGlobal('requestAnimationFrame', requestAnimationFrame)
    vi.stubGlobal('cancelAnimationFrame', cancelAnimationFrame)

    const wrapper = mount(KnowledgeCore)
    motionHandler({ matches: true })
    await Promise.resolve()
    motionHandler({ matches: false })
    await Promise.resolve()
    motionHandler({ matches: true })
    await Promise.resolve()
    motionHandler({ matches: false })
    await nextTick()
    await nextTick()

    expect(context.setTransform).toHaveBeenCalledWith(2, 0, 0, 2, 0, 0)
    expect(observers).toHaveLength(1)
    expect(requestAnimationFrame).toHaveBeenCalledOnce()

    wrapper.unmount()
    expect(observers.every((observer) => observer.disconnect.mock.calls.length === 1)).toBe(true)
    expect(cancelAnimationFrame).toHaveBeenCalledWith(1)
    getContext.mockRestore()
  })

  it('pauses the knowledge core offscreen, while hidden, and after motion is disabled', async () => {
    let motionHandler
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn((_event, handler) => { motionHandler = handler }),
      removeEventListener: vi.fn()
    })))
    let documentHidden = false
    vi.spyOn(document, 'hidden', 'get').mockImplementation(() => documentHidden)
    const context = createCanvasContext()
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
    let intersectionCallback
    const intersectionObserver = { observe: vi.fn(), disconnect: vi.fn() }
    vi.stubGlobal('IntersectionObserver', vi.fn((callback) => {
      intersectionCallback = callback
      return intersectionObserver
    }))
    let resizeCallback
    const resizeObserver = { observe: vi.fn(), disconnect: vi.fn() }
    vi.stubGlobal('ResizeObserver', vi.fn((callback) => {
      resizeCallback = callback
      return resizeObserver
    }))
    const removeDocumentListener = vi.spyOn(document, 'removeEventListener')
    const raf = createRafQueue()

    const wrapper = mount(KnowledgeCore)
    await nextTick()
    await nextTick()

    expect(intersectionObserver.observe).toHaveBeenCalledWith(wrapper.element)
    expect(raf.callbacks.size).toBe(0)

    intersectionCallback([{ isIntersecting: true }])
    expect(raf.callbacks.size).toBe(1)
    raf.runNext(16)
    expect(context.clearRect).toHaveBeenCalledOnce()

    documentHidden = true
    document.dispatchEvent(new Event('visibilitychange'))
    expect(raf.callbacks.size).toBe(0)
    expect(raf.runNext(32)).toBe(false)
    expect(context.clearRect).toHaveBeenCalledOnce()

    documentHidden = false
    document.dispatchEvent(new Event('visibilitychange'))
    expect(raf.callbacks.size).toBe(1)
    intersectionCallback([{ isIntersecting: false }])
    expect(raf.callbacks.size).toBe(0)

    intersectionCallback([{ isIntersecting: true }])
    motionHandler({ matches: true })
    await nextTick()
    expect(raf.callbacks.size).toBe(0)
    expect(wrapper.find('canvas').exists()).toBe(false)

    wrapper.unmount()
    expect(intersectionObserver.disconnect).toHaveBeenCalledOnce()
    expect(resizeObserver.disconnect).toHaveBeenCalledOnce()
    expect(raf.callbacks.size).toBe(0)
    const transformCalls = context.setTransform.mock.calls.length
    resizeCallback()
    intersectionCallback([{ isIntersecting: true }])
    document.dispatchEvent(new Event('visibilitychange'))
    expect(context.setTransform).toHaveBeenCalledTimes(transformCalls)
    expect(context.clearRect).toHaveBeenCalledOnce()
    expect(raf.callbacks.size).toBe(0)
    expect(removeDocumentListener).toHaveBeenCalledWith('visibilitychange', expect.any(Function))
  })

  it('reduces knowledge-core work after a slow frame and responds to resize', async () => {
    stubMotionPreference(false)
    let intersectionCallback
    vi.stubGlobal('IntersectionObserver', vi.fn((callback) => {
      intersectionCallback = callback
      return { observe: vi.fn(), disconnect: vi.fn() }
    }))
    let resizeCallback
    vi.stubGlobal('ResizeObserver', vi.fn((callback) => {
      resizeCallback = callback
      return { observe: vi.fn(), disconnect: vi.fn() }
    }))
    vi.stubGlobal('devicePixelRatio', 2.5)
    const context = createCanvasContext()
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
    const raf = createRafQueue()
    const now = vi.spyOn(performance, 'now')

    const wrapper = mount(KnowledgeCore)
    await nextTick()
    await nextTick()
    const canvas = wrapper.get('canvas').element
    vi.spyOn(canvas, 'getBoundingClientRect').mockReturnValue({ width: 600, height: 600 })
    resizeCallback()
    expect(context.setTransform).toHaveBeenLastCalledWith(2, 0, 0, 2, 0, 0)

    intersectionCallback([{ isIntersecting: true }])
    now.mockReset()
    now.mockReturnValueOnce(0).mockReturnValueOnce(18)
      .mockReturnValueOnce(20).mockReturnValueOnce(21)
    raf.runNext(20)
    const firstFrameArcs = context.arc.mock.calls.length
    raf.runNext(60)
    const secondFrameArcs = context.arc.mock.calls.length - firstFrameArcs

    expect(secondFrameArcs).toBeLessThan(firstFrameArcs)
    wrapper.unmount()
  })

  it('keeps decorative landscape layers static for reduced motion', () => {
    stubMotionPreference(true)
    const wrapper = mount(InkLandscape, { props: { parallax: true } })

    expect(wrapper.attributes('aria-hidden')).toBe('true')
    expect(wrapper.classes()).toContain('ink-landscape--static')
    expect(wrapper.find('.ink-landscape__artwork').exists()).toBe(true)
    expect(wrapper.find('.ink-landscape__mist').exists()).toBe(true)
    expect(wrapper.find('.ink-landscape__mountains').exists()).toBe(true)
    expect(wrapper.find('.ink-landscape__grain').exists()).toBe(true)
  })

  it('coalesces landscape pointer updates into one animation frame', async () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    })))
    const raf = createRafQueue()
    const wrapper = mount(InkLandscape, { props: { parallax: true } })
    vi.spyOn(wrapper.element, 'getBoundingClientRect').mockReturnValue({
      left: 0,
      top: 0,
      width: 200,
      height: 100
    })

    await wrapper.trigger('pointermove', { clientX: 20, clientY: 20 })
    await wrapper.trigger('pointermove', { clientX: 180, clientY: 80 })
    expect(raf.requestAnimationFrame).toHaveBeenCalledOnce()

    raf.runNext()
    expect(parseFloat(wrapper.element.style.getPropertyValue('--near-x'))).toBeCloseTo(8.8)
    expect(parseFloat(wrapper.element.style.getPropertyValue('--near-y'))).toBeCloseTo(2.4)

    await wrapper.trigger('pointermove', { clientX: 100, clientY: 50 })
    wrapper.unmount()
    expect(raf.callbacks.size).toBe(0)
  })

  it('disables landscape parallax for coarse pointers', async () => {
    const removeCoarseListener = vi.fn()
    vi.stubGlobal('matchMedia', vi.fn((query) => ({
      matches: query === '(pointer: coarse)',
      addEventListener: vi.fn(),
      removeEventListener: query === '(pointer: coarse)' ? removeCoarseListener : vi.fn()
    })))
    const raf = createRafQueue()
    const wrapper = mount(InkLandscape, { props: { parallax: true } })
    await nextTick()

    expect(wrapper.classes()).toContain('ink-landscape--static')
    await wrapper.trigger('pointermove', { clientX: 30, clientY: 20 })
    expect(raf.requestAnimationFrame).not.toHaveBeenCalled()
    wrapper.unmount()
    expect(removeCoarseListener).toHaveBeenCalledWith('change', expect.any(Function))
  })

  it('exposes reveal state without removing content from the accessibility tree', async () => {
    stubMotionPreference(true)
    const wrapper = mount(RevealSection, {
      props: { tag: 'article' },
      slots: { default: '<h2>学习路径</h2>' }
    })
    await nextTick()

    expect(wrapper.element.tagName).toBe('ARTICLE')
    expect(wrapper.attributes('data-visible')).toBe('true')
    expect(wrapper.classes()).toContain('is-visible')
    expect(wrapper.text()).toContain('学习路径')
  })
})
