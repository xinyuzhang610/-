<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useMotionPreference } from '../../composables/useMotionPreference'

const canvas = ref(null)
const canvasSupported = ref(false)
const { canAnimate } = useMotionPreference()

const PARTICLE_COUNT = 42
const particles = Array.from({ length: PARTICLE_COUNT }, (_, index) => {
  const ring = 0.22 + (index % 7) * 0.085
  const angle = index * 2.399963229728653
  return {
    angle,
    ring,
    speed: 0.00008 + (index % 5) * 0.000012,
    size: 1.15 + (index % 3) * 0.55
  }
})

let context
let frameId
let resizeObserver
let removeResizeListener
let width = 1
let height = 1
let pointerX = 0
let pointerY = 0
let runGeneration = 0

function resizeCanvas() {
  if (!canvas.value || !context) return
  const bounds = canvas.value.getBoundingClientRect()
  width = Math.max(1, bounds.width)
  height = Math.max(1, bounds.height)
  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  canvas.value.width = Math.round(width * dpr)
  canvas.value.height = Math.round(height * dpr)
  context.setTransform(dpr, 0, 0, dpr, 0, 0)
}

function draw(time = 0) {
  if (!context || !canvas.value || !canAnimate.value) return
  context.clearRect(0, 0, width, height)
  const centerX = width / 2 + pointerX * 10
  const centerY = height / 2 + pointerY * 8
  const radius = Math.min(width, height) * 0.36

  const halo = context.createRadialGradient(centerX, centerY, 2, centerX, centerY, radius)
  halo.addColorStop(0, 'rgba(241, 217, 157, 0.86)')
  halo.addColorStop(0.22, 'rgba(66, 185, 154, 0.42)')
  halo.addColorStop(1, 'rgba(23, 107, 90, 0)')
  context.fillStyle = halo
  context.beginPath()
  context.arc(centerX, centerY, radius, 0, Math.PI * 2)
  context.fill()

  for (let index = 0; index < particles.length; index += 1) {
    const particle = particles[index]
    const angle = particle.angle + time * particle.speed
    const x = centerX + Math.cos(angle) * radius * particle.ring
    const y = centerY + Math.sin(angle) * radius * particle.ring * 0.72

    if (index % 3 === 0) {
      context.beginPath()
      context.moveTo(centerX, centerY)
      context.lineTo(x, y)
      context.strokeStyle = 'rgba(169, 221, 206, 0.17)'
      context.lineWidth = 0.7
      context.stroke()
    }

    context.beginPath()
    context.arc(x, y, particle.size, 0, Math.PI * 2)
    context.fillStyle = index % 5 === 0 ? 'rgba(213, 166, 79, 0.92)' : 'rgba(66, 185, 154, 0.82)'
    context.fill()
  }

  context.beginPath()
  context.arc(centerX, centerY, radius * 0.15, 0, Math.PI * 2)
  context.fillStyle = 'rgba(248, 250, 245, 0.92)'
  context.fill()
  context.strokeStyle = 'rgba(213, 166, 79, 0.9)'
  context.lineWidth = 1.5
  context.stroke()
  frameId = window.requestAnimationFrame(draw)
}

function stopCanvas() {
  runGeneration += 1
  if (frameId != null) window.cancelAnimationFrame(frameId)
  frameId = undefined
  resizeObserver?.disconnect()
  resizeObserver = undefined
  removeResizeListener?.()
  removeResizeListener = undefined
  context = undefined
}

async function startCanvas() {
  stopCanvas()
  const generation = runGeneration
  if (!canAnimate.value || typeof window === 'undefined') {
    canvasSupported.value = false
    return
  }

  canvasSupported.value = true
  await nextTick()
  if (generation !== runGeneration || !canAnimate.value) return
  context = canvas.value?.getContext?.('2d') || undefined
  if (!context) {
    canvasSupported.value = false
    return
  }

  resizeCanvas()
  if (typeof window.ResizeObserver === 'function') {
    resizeObserver = new window.ResizeObserver(resizeCanvas)
    resizeObserver.observe(canvas.value)
  } else {
    window.addEventListener('resize', resizeCanvas, { passive: true })
    removeResizeListener = () => window.removeEventListener('resize', resizeCanvas)
  }
  frameId = window.requestAnimationFrame(draw)
}

function handlePointerMove(event) {
  if (!canAnimate.value) return
  const bounds = event.currentTarget.getBoundingClientRect()
  pointerX = ((event.clientX - bounds.left) / Math.max(bounds.width, 1) - 0.5) * 2
  pointerY = ((event.clientY - bounds.top) / Math.max(bounds.height, 1) - 0.5) * 2
}

function resetPointer() {
  pointerX = 0
  pointerY = 0
}

onMounted(startCanvas)
watch(canAnimate, startCanvas)
onBeforeUnmount(stopCanvas)
</script>

<template>
  <div
    class="knowledge-core"
    aria-hidden="true"
    @pointermove="handlePointerMove"
    @pointerleave="resetPointer"
  >
    <canvas v-if="canvasSupported && canAnimate" ref="canvas" class="knowledge-core__canvas" />
    <svg
      v-else
      class="knowledge-core__fallback"
      viewBox="0 0 360 360"
      focusable="false"
    >
      <defs>
        <radialGradient id="knowledge-core-halo">
          <stop offset="0" stop-color="var(--gold-200)" stop-opacity=".92" />
          <stop offset=".32" stop-color="var(--jade-400)" stop-opacity=".42" />
          <stop offset="1" stop-color="var(--jade-700)" stop-opacity="0" />
        </radialGradient>
      </defs>
      <circle cx="180" cy="180" r="150" fill="url(#knowledge-core-halo)" />
      <g class="knowledge-core__fallback-lines">
        <path d="M180 180 97 111M180 180l111-53M180 180l-89 75M180 180l105 76" />
        <ellipse cx="180" cy="180" rx="105" ry="69" />
        <ellipse cx="180" cy="180" rx="70" ry="112" transform="rotate(42 180 180)" />
      </g>
      <g class="knowledge-core__fallback-nodes">
        <circle cx="97" cy="111" r="6" />
        <circle cx="291" cy="127" r="5" />
        <circle cx="91" cy="255" r="5" />
        <circle cx="285" cy="256" r="6" />
        <circle cx="180" cy="180" r="20" class="knowledge-core__fallback-center" />
      </g>
    </svg>
  </div>
</template>

<style scoped>
.knowledge-core {
  position: relative;
  width: min(100%, 36rem);
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 50%;
  background: radial-gradient(circle, rgb(169 221 206 / 16%), transparent 66%);
  contain: layout paint size;
}

.knowledge-core__canvas,
.knowledge-core__fallback {
  width: 100%;
  height: 100%;
}

.knowledge-core__fallback-lines {
  fill: none;
  stroke: var(--jade-500);
  stroke-opacity: 0.36;
  stroke-width: 1.5;
}

.knowledge-core__fallback-nodes { fill: var(--gold-400); }
.knowledge-core__fallback-center { fill: var(--moon-50); stroke: var(--gold-400); stroke-width: 2; }
</style>
