import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Home from '../views/Home.vue'

describe('Home.vue', () => {
  it('renders correctly', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'el-button': true,
          'router-link': true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('displays the title', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'el-button': true,
          'router-link': true
        }
      }
    })
    expect(wrapper.text()).toContain('智教通')
  })

  it('displays the welcome message', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'el-button': true,
          'router-link': true
        }
      }
    })
    expect(wrapper.text()).toContain('为什么选择智教通')
  })

  it('has a button', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'el-button': {
            template: '<button><slot /></button>'
          },
          'router-link': true
        }
      }
    })
    expect(wrapper.find('button').exists()).toBe(true)
  })
})
