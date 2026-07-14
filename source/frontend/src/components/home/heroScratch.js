export const INK_REVEAL = Object.freeze({
  startRadius: 8,
  endRadius: 128,
  radiusVariation: 0.45,
  lifetime: 520,
  spacing: 12,
  maxStamps: 160
})

export function createInkStamp({ x, y, now, random = Math.random }) {
  return {
    x,
    y,
    born: now,
    seed: random() * Math.PI * 2,
    maxRadius: INK_REVEAL.endRadius * (
      1 - INK_REVEAL.radiusVariation + random() * INK_REVEAL.radiusVariation
    )
  }
}

export function sampleInkStamp(stamp, now) {
  const progress = (now - stamp.born) / INK_REVEAL.lifetime
  if (progress >= 1) return null
  const bounded = Math.max(0, progress)
  const eased = 1 - Math.pow(1 - bounded, 3)
  return {
    ...stamp,
    radius: INK_REVEAL.startRadius + (stamp.maxRadius - INK_REVEAL.startRadius) * eased,
    alpha: 1 - bounded * bounded
  }
}

export function interpolateStroke(from, to, spacing) {
  const distance = Math.hypot(to.x - from.x, to.y - from.y)
  const steps = Math.max(1, Math.ceil(distance / spacing))
  return Array.from({ length: steps }, (_, index) => {
    const progress = (index + 1) / steps
    return {
      x: from.x + (to.x - from.x) * progress,
      y: from.y + (to.y - from.y) * progress
    }
  })
}
