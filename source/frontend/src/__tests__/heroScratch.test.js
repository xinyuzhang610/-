import { describe, expect, it } from 'vitest'
import {
  INK_REVEAL,
  createInkStamp,
  interpolateStroke,
  sampleInkStamp
} from '../components/home/heroScratch'

describe('hero scratch helpers', () => {
  it('matches the approved living ink timing and spacing', () => {
    expect(INK_REVEAL).toMatchObject({
      startRadius: 8,
      endRadius: 128,
      radiusVariation: 0.45,
      lifetime: 520,
      spacing: 12,
      maxStamps: 160
    })
  })

  it('expands and fades a deterministic stamp during its lifetime', () => {
    const stamp = createInkStamp({ x: 20, y: 30, now: 100, random: () => 0.5 })
    const sample = sampleInkStamp(stamp, 360)

    expect(sample.x).toBe(20)
    expect(sample.y).toBe(30)
    expect(sample.radius).toBeCloseTo(87.8, 1)
    expect(sample.alpha).toBeCloseTo(0.75, 2)
  })

  it('expires a stamp after 520 milliseconds', () => {
    const stamp = createInkStamp({ x: 20, y: 30, now: 100, random: () => 0.5 })

    expect(sampleInkStamp(stamp, 620)).toBeNull()
  })

  it('interpolates long movements without gaps and preserves the destination', () => {
    const points = interpolateStroke(
      { x: 0, y: 0 },
      { x: 100, y: 0 },
      INK_REVEAL.spacing
    )

    expect(points.length).toBeGreaterThan(8)
    expect(points.at(-1)).toEqual({ x: 100, y: 0 })
    expect(points.every((point, index) => (
      index === 0 || point.x - points[index - 1].x <= INK_REVEAL.spacing
    ))).toBe(true)
  })
})
