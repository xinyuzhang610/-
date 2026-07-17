<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const root = ref(null)
const canvas = ref(null)

const STARS = 280
const COLORS = ['#e4c477', '#42b99a', '#7ad4e8', '#ce93d8', '#ff8a65']
const LABELS = ['需求发现', '智能推荐', 'AI问答', '工具广场', '学习分析']

let ctx, w, h, raf
let stars = [], mains = []
let mx = -999, my = -999
let cx, cy, rx, ry

function init() {
  cx = w * .5; cy = h * .5
  rx = w * .38; ry = h * .34
  stars = Array.from({ length: STARS }, () => ({
    x: Math.random() * w, y: Math.random() * h,
    r: Math.random() * 3 + 1,
    phase: Math.random() * Math.PI * 2,
    spd: Math.random() * .04 + .01,
    color: COLORS[Math.floor(Math.random() * COLORS.length)]
  }))
  mains = COLORS.map((c, i) => {
    const a = (i / 5) * Math.PI * 2 - Math.PI / 2
    const x = cx + Math.cos(a) * rx
    const y = cy + Math.sin(a) * ry
    return { a, x, y, r: 14, baseR: 14, color: c, label: LABELS[i], trail: [] }
  })
}

function drawGlowRing() {
  // inner glow ring
  ctx.beginPath()
  ctx.strokeStyle = 'rgba(180,220,240,.25)'
  ctx.lineWidth = 4
  ctx.shadowColor = 'rgba(180,220,240,.5)'
  ctx.shadowBlur = 18
  ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.shadowBlur = 0
  // outer soft ring
  ctx.beginPath()
  ctx.strokeStyle = 'rgba(180,220,240,.08)'
  ctx.lineWidth = 2
  ctx.shadowColor = 'rgba(180,220,240,.25)'
  ctx.shadowBlur = 30
  ctx.ellipse(cx, cy, rx * 1.06, ry * 1.06, 0, 0, Math.PI * 2)
  ctx.stroke()
  ctx.shadowBlur = 0
}

function drawStarShape(x, y, r, color) {
  ctx.beginPath()
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2 - Math.PI / 2
    const or = i === 0 ? r * 2 : r * .7
    if (i === 0) ctx.moveTo(x + Math.cos(a) * or, y + Math.sin(a) * or)
    ctx.lineTo(x + Math.cos(a + Math.PI / 5) * r * .3, y + Math.sin(a + Math.PI / 5) * r * .3)
    ctx.lineTo(x + Math.cos(a + Math.PI * 2 / 5) * or, y + Math.sin(a + Math.PI * 2 / 5) * or)
  }
  ctx.closePath(); ctx.fill()
}

function draw(t) {
  ctx.clearRect(0, 0, w, h)

  // halo ring
  drawGlowRing()

  // small stars
  stars.forEach(s => {
    s.phase += s.spd
    const alpha = .25 + .5 * (.5 + .5 * Math.sin(s.phase))
    ctx.globalAlpha = alpha
    ctx.fillStyle = s.color
    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill()
  })
  ctx.globalAlpha = 1

  // orbit trails
  const tc = ['#e4c477','#42b99a','#7ad4e8','#ce93d8','#ff8a65']
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2 - Math.PI / 2 + t * .0015
    for (let j = 0; j < 10; j++) {
      const ba = a - j * .03
      const al = .14 - j * .013
      if (al <= 0) continue
      ctx.globalAlpha = al; ctx.fillStyle = tc[i]
      ctx.beginPath(); ctx.arc(cx + Math.cos(ba) * rx, cy + Math.sin(ba) * ry, 3, 0, Math.PI * 2); ctx.fill()
    }
  }
  ctx.globalAlpha = 1

  raf = requestAnimationFrame(draw)
}

function resize() {
  if (!canvas.value || !root.value) return
  const r = root.value.getBoundingClientRect()
  w = r.width; h = r.height
  if (w < 10 || h < 10) return
  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  canvas.value.width = w * dpr; canvas.value.height = h * dpr
  ctx = canvas.value.getContext('2d')
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  cancelAnimationFrame(raf)
  init()
  raf = requestAnimationFrame(draw)
}

function mv(e) {
  const r = canvas.value.getBoundingClientRect()
  mx = e.clientX - r.left; my = e.clientY - r.top
}

onMounted(() => {
  resize()
  window.addEventListener('resize', resize)
  canvas.value?.addEventListener('pointermove', mv)
  canvas.value?.addEventListener('pointerleave', () => { mx = -999; my = -999 })
})
onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  window.removeEventListener('resize', resize)
})
</script>

<template>
  <div ref="root" class="starfield" aria-hidden="true">
    <canvas ref="canvas" class="starfield__canvas" />
  </div>
</template>

<style scoped>
.starfield { position: absolute; inset: 0; overflow: hidden; }
.starfield__canvas { width: 100%; height: 100%; }
</style>
