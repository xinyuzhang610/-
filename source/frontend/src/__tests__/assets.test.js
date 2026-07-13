import { describe, expect, it } from 'vitest'
import { generatedAssets } from '../assets/generated/asset-manifest.js'

const requiredAssetKeys = [
  'heroInkLandscape',
  'teacherOrbit',
  'studentOrbit',
  'knowledgeUniverse'
]

describe('generated artwork manifest', () => {
  it('exposes exactly the four production-ready Eastern future assets', () => {
    expect(Object.keys(generatedAssets).sort()).toEqual([...requiredAssetKeys].sort())

    for (const asset of Object.values(generatedAssets)) {
      expect(asset.src).toMatch(/\.webp$/)
      expect(asset.width).toBeGreaterThan(1000)
      expect(asset.height).toBeGreaterThan(500)
      expect(typeof asset.alt).toBe('string')
    }
  })
})
