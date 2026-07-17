<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  INK_REVEAL,
  createInkStamp,
  interpolateStroke,
  sampleInkStamp
} from './heroScratch'

const props = defineProps({ skipped: { type: Boolean, default: false } })
const emit = defineEmits(['first-reveal', 'static-mode'])

const canvas = ref(null)
const staticMode = ref(false)
const stamps = []
const MAX_SAMPLE_GAP = 80
let context
let observer
let frame = 0
let running = false
let lastPoint
let width = 0
let height = 0
let firstRevealSent = false
let staticModeSent = false

function paintMask() {
  if (!context || !width || !height) return
  context.globalCompositeOperation = 'source-over'
  const wash = context.createLinearGradient(0, 0, width, height)
  wash.addColorStop(0, 'rgb(3 17 13)')
  wash.addColorStop(.48, 'rgb(8 26 20)')
  wash.addColorStop(1, 'rgb(24 40 31)')
  context.fillStyle = wash
  context.fillRect(0, 0, width, height)
}

function carveInk(sample) {
  const brush = context.createRadialGradient(
    sample.x,
    sample.y,
    sample.radius * .25,
    sample.x,
    sample.y,
    sample.radius
  )
  brush.addColorStop(0, `rgba(0, 0, 0, ${.95 * sample.alpha})`)
  brush.addColorStop(.55, `rgba(0, 0, 0, ${.88 * sample.alpha})`)
  brush.addColorStop(1, 'rgba(0, 0, 0, 0)')
  context.fillStyle = brush
  context.beginPath()
  const segments = 32
  for (let index = 0; index <= segments; index += 1) {
    const angle = (index / segments) * Math.PI * 2
    const wobble = 0.78
      + 0.14 * Math.sin(angle * 3 + sample.seed)
      + 0.08 * Math.sin(angle * 7 + sample.seed * 2.1)
      + 0.05 * Math.sin(angle * 13 + sample.seed * .7)
    const radius = sample.radius * wobble
    const x = sample.x + Math.cos(angle) * radius
    const y = sample.y + Math.sin(angle) * radius
    if (index === 0) context.moveTo(x, y)
    else context.lineTo(x, y)
  }
  context.closePath()
  context.fill()
}

function drawFrame(now) {
  frame = 0
  if (!context || staticMode.value || props.skipped) {
    running = false
    return
  }

  paintMask()
  context.globalCompositeOperation = 'destination-out'
  for (let index = stamps.length - 1; index >= 0; index -= 1) {
    const sample = sampleInkStamp(stamps[index], now)
    if (!sample) {
      stamps.splice(index, 1)
      continue
    }
    carveInk(sample)
  }

  if (stamps.length) frame = requestAnimationFrame(drawFrame)
  else running = false
}

function startLoop() {
  if (running) return
  running = true
  frame = requestAnimationFrame(drawFrame)
}

function addStamp(point, now) {
  if (stamps.length >= INK_REVEAL.maxStamps) stamps.shift()
  stamps.push(createInkStamp({ x: point.x, y: point.y, now }))
}

function queuePoint(event) {
  if (staticMode.value || props.skipped || !canvas.value || !context) return
  const rect = canvas.value.getBoundingClientRect()
  const now = performance.now()
  const current = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top,
    time: now
  }
  const samples = lastPoint && now - lastPoint.time <= MAX_SAMPLE_GAP
    ? interpolateStroke(lastPoint, current, INK_REVEAL.spacing)
    : [current]

  samples.forEach((sample) => addStamp(sample, now))
  lastPoint = current
  if (!firstRevealSent) {
    firstRevealSent = true
    emit('first-reveal')
  }
  startLoop()
}

function onPointerLeave() {
  lastPoint = undefined
}

function resizeAndRedraw() {
  if (!canvas.value || staticMode.value || props.skipped || !context) return
  const rect = canvas.value.getBoundingClientRect()
  if (!rect.width || !rect.height) return
  const ratio = Math.min(window.devicePixelRatio || 1, 2)
  width = rect.width
  height = rect.height
  canvas.value.width = Math.round(width * ratio)
  canvas.value.height = Math.round(height * ratio)
  context.setTransform(ratio, 0, 0, ratio, 0, 0)
  cancelAnimationFrame(frame)
  frame = 0
  running = false
  lastPoint = undefined
  stamps.length = 0
  paintMask()
}

function addListeners() {
  canvas.value?.addEventListener('pointerenter', queuePoint)
  canvas.value?.addEventListener('pointermove', queuePoint)
  canvas.value?.addEventListener('pointerleave', onPointerLeave)
}

function removeListeners() {
  canvas.value?.removeEventListener('pointerenter', queuePoint)
  canvas.value?.removeEventListener('pointermove', queuePoint)
  canvas.value?.removeEventListener('pointerleave', onPointerLeave)
  window.removeEventListener('resize', resizeAndRedraw)
}

function enterStaticMode() {
  staticMode.value = true
  cancelAnimationFrame(frame)
  frame = 0
  running = false
  stamps.length = 0
  lastPoint = undefined
  removeListeners()
  observer?.disconnect()
  if (canvas.value) canvas.value.hidden = true
  if (!staticModeSent) {
    staticModeSent = true
    emit('static-mode')
  }
}

onMounted(() => {
  const hoverQuery = window.matchMedia?.('(hover: hover)')
  const motionQuery = window.matchMedia?.('(prefers-reduced-motion: reduce)')
  const canHover = hoverQuery?.matches === true
  const reduced = motionQuery ? motionQuery.matches : true
  const lowMemory = Number(navigator.deviceMemory || 4) <= 2
  if (props.skipped || !canHover || reduced || lowMemory) {
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
  stamps.length = 0
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
.hero-scratch { position: absolute; z-index: 1; inset: 0; background: transparent; pointer-events: none; }
.hero-scratch[data-static='true'] { display: none; }
.hero-scratch__canvas { width: 100%; height: 100%; filter: contrast(1.04); pointer-events: auto; }
.hero-scratch__canvas[hidden] { display: none; }
</style>
