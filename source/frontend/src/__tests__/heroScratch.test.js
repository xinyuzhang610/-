import { describe, expect, it } from 'vitest'
import { brushRadius, interpolateStroke } from '../components/home/heroScratch'

describe('hero scratch helpers', () => {
  it('uses a broader brush for faster movement within safe bounds', () => {
    expect(brushRadius(0, 1000)).toBe(34)
    expect(brushRadius(2, 1000)).toBeGreaterThan(34)
    expect(brushRadius(100, 1000)).toBe(82)
  })

  it('interpolates long movements without gaps and preserves the destination', () => {
    const points = interpolateStroke({ x: 0, y: 0 }, { x: 100, y: 0 }, 20)

    expect(points.length).toBeGreaterThan(4)
    expect(points.at(-1)).toEqual({ x: 100, y: 0 })
    expect(points.every((point, index) => index === 0 || point.x - points[index - 1].x <= 20)).toBe(true)
  })
})
