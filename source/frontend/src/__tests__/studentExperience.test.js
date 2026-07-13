import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import Guidance from '../views/student/Guidance.vue'
import Plaza from '../views/student/Plaza.vue'
import Chat from '../views/student/Chat.vue'
import Records from '../views/student/Records.vue'
import ToolUse from '../views/student/ToolUse.vue'

const plazaRequest = vi.fn()
const chatRequest = vi.fn()
const toolRequest = vi.fn()
const usageRequest = vi.fn()

vi.mock('../api/plaza', () => ({ getPlaza: (...args) => plazaRequest(...args) }))
vi.mock('../api/chat', () => ({ sendChat: (...args) => chatRequest(...args) }))
vi.mock('../api/tools', () => ({ getTool: (...args) => toolRequest(...args) }))
vi.mock('../api/usage', () => ({ getMyUsage: (...args) => usageRequest(...args) }))

async function mountAt(component, path) {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/student/:page', component: { template: '<div />' } },
      { path: '/tool/:id', component }
    ]
  })
  await router.push(path)
  await router.isReady()
  return mount(component, { global: { plugins: [router], stubs: { RouterLink: false } } })
}

describe('student knowledge journey', () => {
  beforeEach(() => {
    plazaRequest.mockReset()
    chatRequest.mockReset()
    toolRequest.mockReset()
    usageRequest.mockReset()
    localStorage.clear()
  })

  it('offers exactly three accessible interest layers with live progress', async () => {
    const wrapper = await mountAt(Guidance, '/student/guidance')
    expect(wrapper.findAll('[data-interest-layer]')).toHaveLength(3)
    expect(wrapper.get('[role="status"]').text()).toContain('第 1 层，共 3 层')
    const first = wrapper.get('button[aria-pressed]')
    await first.trigger('click')
    expect(first.attributes('aria-pressed')).toBe('true')
  })

  it('loads plaza data and sends category and search controls to the API', async () => {
    plazaRequest.mockResolvedValue({ data: { categories: [{ value: '理科', label: '理科专区' }], tools: [], hot_tools: [] } })
    const wrapper = await mountAt(Plaza, '/student/plaza')
    await flushPromises()
    await wrapper.get('[aria-label="搜索工具"] input').setValue('公式')
    await wrapper.get('[aria-label="理科专区"]').trigger('click')
    await wrapper.get('form').trigger('submit')
    expect(plazaRequest).toHaveBeenLastCalledWith({ category: '理科', search: '公式' })
  })

  it('keeps chat input after a failed request and exposes retry', async () => {
    chatRequest.mockRejectedValue(new Error('timeout'))
    const wrapper = await mountAt(Chat, '/student/chat')
    await wrapper.get('textarea').setValue('请解释勾股定理')
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    expect(wrapper.get('textarea').element.value).toBe('请解释勾股定理')
    expect(wrapper.get('[data-testid="retry-message"]').exists()).toBe(true)
  })

  it('derives labeled record metrics from the real usage response', async () => {
    usageRequest.mockResolvedValue({ data: [{ id: 1, tool_id: 7, input_text: '勾股定理', output_text: '回答', created_at: '2026-07-14T08:00:00Z' }] })
    localStorage.setItem('user_id', '8')
    const wrapper = await mountAt(Records, '/student/records')
    await flushPromises()
    expect(wrapper.text()).toContain('使用次数')
    expect(wrapper.text()).toContain('使用工具数')
    expect(wrapper.text()).toContain('1')
    expect(usageRequest).toHaveBeenCalledWith('8')
  })

  it('loads the route tool and sends its numeric ID with chat', async () => {
    toolRequest.mockResolvedValue({ data: { id: 42, name: '概念辨析器', description: '厘清易混概念', category: '理科', usage_count: 3 } })
    chatRequest.mockResolvedValue({ data: { reply: '已辨析', session_id: 'session-1', tool_name: '概念辨析器' } })
    const wrapper = await mountAt(ToolUse, '/tool/42')
    await flushPromises()
    expect(toolRequest).toHaveBeenCalledWith('42')
    expect(wrapper.text()).toContain('工具编号 42')
    await wrapper.get('textarea').setValue('质量和重量')
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    expect(chatRequest).toHaveBeenCalledWith(expect.objectContaining({ message: '质量和重量', tool_id: 42 }))
  })
})
