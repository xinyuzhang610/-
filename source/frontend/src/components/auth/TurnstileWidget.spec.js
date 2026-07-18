import { describe, expect, it, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import TurnstileWidget from './TurnstileWidget.vue'

describe('TurnstileWidget', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.unstubAllGlobals()
  })

  it('shows error when siteKey is missing', async () => {
    const wrapper = mount(TurnstileWidget, { props: { siteKey: '' } })
    await nextTick()
    expect(wrapper.find('.turnstile-error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Turnstile 配置错误')
  })

  it('loads turnstile script', async () => {
    const appendChild = vi.spyOn(document.head, 'appendChild')
    mount(TurnstileWidget, { props: { siteKey: 'test-key' } })
    await nextTick()
    expect(appendChild).toHaveBeenCalled()
    const script = appendChild.mock.calls.find(([el]) => el.tagName === 'SCRIPT')?.[0]
    expect(script?.src).toContain('challenges.cloudflare.com')
  })

  it('exposes reset method', () => {
    const wrapper = mount(TurnstileWidget, { props: { siteKey: '' } })
    expect(typeof wrapper.vm.reset).toBe('function')
  })
})
