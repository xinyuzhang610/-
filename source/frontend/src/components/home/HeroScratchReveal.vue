<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { brushRadius, interpolateStroke } from './heroScratch'

const props = defineProps({ skipped: { type: Boolean, default: false } })
const emit = defineEmits(['first-reveal', 'static-mode'])

const canvas = ref(null)
const staticMode = ref(false)
const normalizedPoints = []
const pendingPoints = []
let context
let observer
let frame = 0
let lastPoint
let firstRevealSent = false
let staticModeSent = false
let touchActive = false
let touchRevealActive = false
let touchOrigin

function paintMask() {
  if (!context || !canvas.value) return
  const { width, height } = canvas.value.getBoundingClientRect()
  context.globalCompositeOperation = 'source-over'
  context.clearRect(0, 0, width, height)
  const wash = context.createLinearGradient(0, 0, width, height)
  wash.addColorStop(0, 'rgba(6, 16, 13, .98)')
  wash.addColorStop(.48, 'rgba(14, 29, 23, .94)')
  wash.addColorStop(1, 'rgba(41, 50, 41, .86)')
  context.fillStyle = wash
  context.fillRect(0, 0, width, height)
}

function erasePoint(point) {
  if (!context) return
  const texturedRadius = point.radius * (.88 + Math.sin(point.seed * 1.71) * .08)
  const brush = context.createRadialGradient(
    point.x,
    point.y,
    texturedRadius * .18,
    point.x,
    point.y,
    texturedRadius
  )
  brush.addColorStop(0, 'rgba(0, 0, 0, 1)')
  brush.addColorStop(.68, 'rgba(0, 0, 0, .9)')
  brush.addColorStop(1, 'rgba(0, 0, 0, 0)')
  context.globalCompositeOperation = 'destination-out'
  context.fillStyle = brush
  context.beginPath()
  context.arc(point.x, point.y, texturedRadius, 0, Math.PI * 2)
  context.fill()
}

function resizeAndRedraw() {
  if (!canvas.value || staticMode.value || props.skipped || !context) return
  lastPoint = undefined
  const rect = canvas.value.getBoundingClientRect()
  if (!rect.width || !rect.height) return
  const ratio = Math.min(window.devicePixelRatio || 1, 2)
  canvas.value.width = Math.round(rect.width * ratio)
  canvas.value.height = Math.round(rect.height * ratio)
  context.setTransform(ratio, 0, 0, ratio, 0, 0)
  paintMask()
  const shortestSide = Math.min(rect.width, rect.height)
  normalizedPoints.forEach((point) => erasePoint({
    x: point.x * rect.width,
    y: point.y * rect.height,
    radius: point.radius * shortestSide,
    seed: point.seed
  }))
}

function flushPoints() {
  frame = 0
  pendingPoints.splice(0).forEach(erasePoint)
}

function isIntentionalTouchMove(event, current) {
  if (event.pointerType !== 'touch') return true
  if (!touchActive || !touchOrigin) return false
  if (touchRevealActive) return true
  const dx = Math.abs(current.x - touchOrigin.x)
  const dy = Math.abs(current.y - touchOrigin.y)
  touchRevealActive = dx >= 10 && dx >= dy * .65
  return touchRevealActive
}

function queuePoint(event) {
  if (staticMode.value || props.skipped || !canvas.value || !context) return
  const rect = canvas.value.getBoundingClientRect()
  const current = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top,
    time: event.timeStamp || performance.now()
  }
  if (!isIntentionalTouchMove(event, current)) return

  const elapsed = Math.max(8, current.time - (lastPoint?.time || current.time - 16))
  const distance = lastPoint ? Math.hypot(current.x - lastPoint.x, current.y - lastPoint.y) : 0
  const speed = distance / elapsed
  const shortestSide = Math.min(rect.width, rect.height)
  const radius = brushRadius(speed, shortestSide)
  const samples = lastPoint
    ? interpolateStroke(lastPoint, current, Math.max(8, radius * .24))
    : [current]

  samples.forEach((sample) => {
    const point = { x: sample.x, y: sample.y, radius, seed: normalizedPoints.length + 1 }
    pendingPoints.push(point)
    normalizedPoints.push({
      x: sample.x / rect.width,
      y: sample.y / rect.height,
      radius: radius / shortestSide,
      seed: point.seed
    })
  })
  lastPoint = current
  if (!firstRevealSent) {
    firstRevealSent = true
    emit('first-reveal')
  }
  if (!frame) frame = requestAnimationFrame(flushPoints)
}

function onPointerDown(event) {
  if (event.pointerType !== 'touch' || !canvas.value) return
  const rect = canvas.value.getBoundingClientRect()
  lastPoint = undefined
  touchActive = true
  touchRevealActive = false
  touchOrigin = { x: event.clientX - rect.left, y: event.clientY - rect.top }
}

function onPointerLeave(event) {
  if (event.pointerType !== 'touch') lastPoint = undefined
}

function onPointerUp() {
  touchActive = false
  touchRevealActive = false
  touchOrigin = undefined
  lastPoint = undefined
}

function enterStaticMode() {
  staticMode.value = true
  pendingPoints.length = 0
  normalizedPoints.length = 0
  if (canvas.value) canvas.value.hidden = true
  if (!staticModeSent) {
    staticModeSent = true
    emit('static-mode')
  }
}

function addListeners() {
  canvas.value.addEventListener('pointermove', queuePoint)
  canvas.value.addEventListener('pointerdown', onPointerDown)
  canvas.value.addEventListener('pointerup', onPointerUp)
  canvas.value.addEventListener('pointercancel', onPointerUp)
  canvas.value.addEventListener('pointerleave', onPointerLeave)
}

function removeListeners() {
  canvas.value?.removeEventListener('pointermove', queuePoint)
  canvas.value?.removeEventListener('pointerdown', onPointerDown)
  canvas.value?.removeEventListener('pointerup', onPointerUp)
  canvas.value?.removeEventListener('pointercancel', onPointerUp)
  canvas.value?.removeEventListener('pointerleave', onPointerLeave)
  window.removeEventListener('resize', resizeAndRedraw)
}

onMounted(() => {
  const motionQuery = window.matchMedia?.('(prefers-reduced-motion: reduce)')
  const reduced = motionQuery ? motionQuery.matches : true
  const lowMemory = Number(navigator.deviceMemory || 4) <= 2
  if (props.skipped || reduced || lowMemory) {
    enterStaticMode()
    return
  }
  try {
    context = canvas.value?.getContext('2d')
  } catch {
    context = null
  }
  if (!context) {
    enterStaticMode()
    return
  }

  addListeners()
  if ('ResizeObserver' in window) {
    observer = new ResizeObserver(resizeAndRedraw)
    observer.observe(canvas.value)
  } else {
    window.addEventListener('resize', resizeAndRedraw, { passive: true })
  }
  resizeAndRedraw()
})

watch(() => props.skipped, (skipped) => {
  if (skipped) enterStaticMode()
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  observer?.disconnect()
  removeListeners()
  pendingPoints.length = 0
  normalizedPoints.length = 0
})
</script>

<template>
  <div
    class="hero-scratch"
    data-testid="hero-scratch-reveal"
    :data-static="staticMode ? 'true' : 'false'"
  >
    <canvas
      ref="canvas"
      class="hero-scratch__canvas"
      data-testid="hero-reveal-canvas"
      aria-hidden="true"
      :hidden="staticMode || skipped"
    />
  </div>
</template>

<style scoped>
.hero-scratch { position: absolute; z-index: 1; inset: 0; background: #0a1411; pointer-events: none; }
.hero-scratch[data-static='true'] { display: none; }
.hero-scratch__canvas { width: 100%; height: 100%; filter: contrast(1.03); pointer-events: auto; touch-action: pan-y; }
.hero-scratch__canvas[hidden] { display: none; }
</style>
