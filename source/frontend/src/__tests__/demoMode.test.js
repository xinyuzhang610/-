import { describe, expect, it } from 'vitest'
import { useDemoMode } from '../composables/useDemoMode'

describe('explicit demo mode', () => {
  it('only enables from the explicit true flag and labels demo data', () => {
    const enabledMode = useDemoMode({ VITE_DEMO_MODE: 'true' })
    const disabledMode = useDemoMode({ VITE_DEMO_MODE: 'false' })
    expect(enabledMode.enabled.value).toBe(true)
    expect(enabledMode.label).toBe('演示数据')
    expect(disabledMode.enabled.value).toBe(false)
  })

  it('returns isolated demo values only when explicitly enabled', () => {
    const active = useDemoMode({ VITE_DEMO_MODE: 'true' })
    const inactive = useDemoMode({})
    const first = active.getDemoData('plaza')
    first.tools[0].name = 'changed'
    expect(active.getDemoData('plaza').tools[0].name).not.toBe('changed')
    expect(inactive.getDemoData('plaza')).toBeUndefined()
  })

  it('resolves a demo tool by route id only in explicit demo mode', () => {
    const active = useDemoMode({ VITE_DEMO_MODE: 'true' })
    const inactive = useDemoMode({ VITE_DEMO_MODE: 'false' })
    expect(active.getDemoTool('1')).toMatchObject({ id: 1, name: '古诗词趣味赏析' })
    expect(inactive.getDemoTool('1')).toBeUndefined()
  })
})
