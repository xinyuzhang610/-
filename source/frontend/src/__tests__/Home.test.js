import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import Home from '../views/Home.vue'

const EmptyView = { template: '<div />' }

async function mountHome() {
  vi.stubGlobal('matchMedia', vi.fn().mockImplementation(() => ({
    matches: true,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn()
  })))

  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: Home },
      { path: '/login', component: EmptyView },
      { path: '/student/guidance', component: EmptyView },
      { path: '/feature/discover', component: EmptyView },
      { path: '/feature/agent', component: EmptyView },
      { path: '/feature/resource', component: EmptyView },
      { path: '/feature/analysis', component: EmptyView },
      { path: '/teacher/tools', component: EmptyView },
      { path: '/teacher/dashboard', component: EmptyView },
      { path: '/student/plaza', component: EmptyView },
      { path: '/student/chat', component: EmptyView },
      { path: '/student/records', component: EmptyView }
    ]
  })

  await router.push('/')
  await router.isReady()
  return mount(Home, { global: { plugins: [router] } })
}

describe('Home.vue', () => {
  it('renders the canonical story as six narrative sections', async () => {
    const wrapper = await mountHome()

    expect(wrapper.get('h1').text()).toContain('让每一次提问，照亮学习路径')
    expect(wrapper.text()).toContain('发现需求')
    expect(wrapper.text()).toContain('工具广场')
    expect(wrapper.findAll('[data-narrative-section]')).toHaveLength(6)
  })

  it('offers valid teacher and student entry routes without router warnings', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const wrapper = await mountHome()

    expect(wrapper.get('[data-testid="teacher-entry"]').attributes('href')).toBe('/login?role=teacher')
    expect(wrapper.get('[data-testid="student-entry"]').attributes('href')).toBe('/student/guidance')
    expect(wrapper.findAll('.entry-link')).toHaveLength(4)
    expect(wrapper.findAll('.entry-link__glyph')).toHaveLength(4)
    expect(wrapper.text()).not.toContain('→')
    expect(warn.mock.calls.flat().join(' ')).not.toMatch(/router-link|No match found/i)
    warn.mockRestore()
  })
})
