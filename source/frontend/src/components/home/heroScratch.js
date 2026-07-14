export function brushRadius(speed, shortestSide) {
  const scale = Math.min(Math.max(shortestSide / 1000, 0.72), 1.35)
  return Math.round(Math.min(82, 34 + speed * 12) * scale)
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
