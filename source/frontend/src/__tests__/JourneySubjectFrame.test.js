import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import JourneySubjectFrame from '../components/home/JourneySubjectFrame.vue'

const asset = { src: '/teacher.webp', width: 1693, height: 929, alt: '教师组织知识路径' }

describe('JourneySubjectFrame', () => {
  it('separates the atmospheric fill from the complete foreground subject', () => {
    const wrapper = mount(JourneySubjectFrame, { props: { asset, tone: 'teacher' } })

    expect(wrapper.get('.journey-subject__atmosphere').attributes('aria-hidden')).toBe('true')
    expect(wrapper.get('.journey-subject__subject').attributes('alt')).toBe(asset.alt)
    expect(wrapper.get('.journey-subject__subject').attributes('width')).toBe('1693')
    expect(wrapper.classes()).toContain('journey-subject--teacher')
  })

  it('removes broken layers and retains a designed fallback surface', async () => {
    const wrapper = mount(JourneySubjectFrame, { props: { asset, tone: 'teacher' } })
    await wrapper.get('.journey-subject__subject').trigger('error')

    expect(wrapper.findAll('img')).toHaveLength(0)
    expect(wrapper.classes()).toContain('journey-subject--fallback')
  })
})
