import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import Home from '../views/Home.vue'
import Guidance from '../views/student/Guidance.vue'
import InterestBubble from '../components/student/InterestBubble.vue'
import { readFileSync } from 'node:fs'

async function mountWithRouter(component, path = '/') {
  const router = createRouter({ history: createMemoryHistory(), routes: [
    { path: '/', component }, { path: '/login', component: { template: '<main><h1>登录</h1></main>' } },
    { path: '/student/guidance', component }, { path: '/student/plaza', component: { template: '<main />' } },
    { path: '/:pathMatch(.*)*', component: { template: '<main />' } }
  ] })
  await router.push(path); await router.isReady()
  return mount(component, { global: { plugins: [router], stubs: { KnowledgeCore: true } } })
}

describe('responsive accessibility and performance structure', () => {
  it('gives the landing page one main landmark and one primary heading', async () => {
    const wrapper = await mountWithRouter(Home)
    expect(wrapper.findAll('main')).toHaveLength(1)
    expect(wrapper.findAll('h1')).toHaveLength(1)
  })

  it('uses native named buttons for student guidance interactions', async () => {
    const wrapper = await mountWithRouter(Guidance, '/student/guidance')
    expect(wrapper.findAll('[data-interest-layer]')).toHaveLength(3)
    expect(wrapper.find('[data-interest-layer] div[role="button"]').exists()).toBe(false)
    for (const button of wrapper.findAll('button')) expect(button.attributes('aria-label') || button.text()).toBeTruthy()
  })

  it('exposes a pressed state and a 44px-capable class on interest controls', () => {
    const wrapper = mount(InterestBubble, { props: { label: '数学', selected: true } })
    expect(wrapper.element.tagName).toBe('BUTTON')
    expect(wrapper.attributes('aria-pressed')).toBe('true')
    expect(wrapper.classes()).toContain('interest-bubble')
  })

  it('splits framework and Element Plus dependencies into separate chunks', () => {
    const config = readFileSync(`${process.cwd()}/vite.config.js`, 'utf8')
    expect(config).toContain('manualChunks')
    expect(config).toContain("'vue-vendor'")
    expect(config).toContain("'element-plus'")
  })
})
