<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useMotionPreference } from '../../composables/useMotionPreference'

const props = defineProps({
  parallax: {
    type: Boolean,
    default: true
  }
})

const { canAnimate } = useMotionPreference()
const root = ref(null)
const coarsePointer = ref(false)
const isStatic = computed(() => !props.parallax || !canAnimate.value || coarsePointer.value)
let pointerFrameId
let pointerX = 0
let pointerY = 0
let pointerMedia

function applyOffsets(x, y) {
  if (!root.value) return
  const style = root.value.style
  style.setProperty('--art-x', `${x * -4}px`)
  style.setProperty('--art-y', `${y * -3}px`)
  style.setProperty('--far-x', `${x * 5}px`)
  style.setProperty('--far-y', `${y * 2}px`)
  style.setProperty('--near-x', `${x * 11}px`)
  style.setProperty('--near-y', `${y * 4}px`)
  style.setProperty('--mist-upper-x', `${x * -8}px`)
  style.setProperty('--mist-lower-x', `${x * 6}px`)
}

function flushPointer() {
  pointerFrameId = undefined
  if (isStatic.value || !root.value) return
  const bounds = root.value.getBoundingClientRect()
  const x = ((pointerX - bounds.left) / Math.max(bounds.width, 1) - 0.5) * 2
  const y = ((pointerY - bounds.top) / Math.max(bounds.height, 1) - 0.5) * 2
  applyOffsets(x, y)
}

function handlePointerMove(event) {
  if (isStatic.value) return
  pointerX = event.clientX
  pointerY = event.clientY
  if (pointerFrameId == null) pointerFrameId = window.requestAnimationFrame(flushPointer)
}

function resetPointer() {
  if (pointerFrameId != null) window.cancelAnimationFrame(pointerFrameId)
  pointerFrameId = undefined
  applyOffsets(0, 0)
}

function updatePointerCapability(event) {
  coarsePointer.value = event.matches
}

onMounted(() => {
  if (typeof window.matchMedia !== 'function') return
  pointerMedia = window.matchMedia('(pointer: coarse)')
  coarsePointer.value = pointerMedia.matches
  if (typeof pointerMedia.addEventListener === 'function') {
    pointerMedia.addEventListener('change', updatePointerCapability)
  } else pointerMedia.addListener?.(updatePointerCapability)
})

watch(isStatic, (staticMode) => {
  if (staticMode) resetPointer()
})

onBeforeUnmount(() => {
  resetPointer()
  if (typeof pointerMedia?.removeEventListener === 'function') {
    pointerMedia.removeEventListener('change', updatePointerCapability)
  } else pointerMedia?.removeListener?.(updatePointerCapability)
})
</script>

<template>
  <div
    ref="root"
    class="ink-landscape"
    :class="{ 'ink-landscape--static': isStatic }"
    aria-hidden="true"
    @pointermove="handlePointerMove"
    @pointerleave="resetPointer"
  >
    <svg class="ink-landscape__artwork" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <circle cx="900" cy="108" r="58" fill="var(--effect-landscape-moon)" />
    </svg>
    <svg class="ink-landscape__mountains ink-landscape__mountains--far" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <path d="M0 388 164 238l73 68 132-173 132 163 92-91 171 180 120-152 116 99 100-142 100 116v214H0Z" />
    </svg>
    <div class="ink-landscape__mist ink-landscape__mist--upper" />
    <svg class="ink-landscape__mountains ink-landscape__mountains--near" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <path d="M0 460 173 330l105 59 164-164 144 145 125-119 140 151 127-79 212 137v60H0Z" />
      <path class="ink-landscape__ridge" d="m424 243 22-18 32 31 23 40M694 267l17-16 33 35 18 40M151 347l22-17 39 22" />
    </svg>
    <div class="ink-landscape__mist ink-landscape__mist--lower" />
    <div class="ink-landscape__grain" />
  </div>
</template>

<style scoped>
.ink-landscape {
  position: relative;
  width: 100%;
  min-height: clamp(18rem, 44vw, 32rem);
  overflow: hidden;
  background: var(--moon-50);
  isolation: isolate;
  --art-x: 0px;
  --art-y: 0px;
  --far-x: 0px;
  --far-y: 0px;
  --near-x: 0px;
  --near-y: 0px;
  --mist-upper-x: 0px;
  --mist-lower-x: 0px;
}

.ink-landscape__artwork,
.ink-landscape__mountains,
.ink-landscape__mist,
.ink-landscape__grain {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  transition: transform var(--duration-slow) var(--ease-out);
}

.ink-landscape__artwork {
  background: var(--effect-landscape-sky);
  transform: translate3d(var(--art-x), var(--art-y), 0) scale(1.02);
}

.ink-landscape__mountains--far {
  fill: var(--effect-landscape-far-ink);
  transform: translate3d(var(--far-x), var(--far-y), 0) scale(1.025);
}

.ink-landscape__mountains--near {
  fill: var(--effect-landscape-near-ink);
  transform: translate3d(var(--near-x), var(--near-y), 0) scale(1.04);
}

.ink-landscape__ridge {
  fill: none;
  stroke: var(--effect-landscape-ridge);
  stroke-linecap: round;
  stroke-width: 2;
}

.ink-landscape__mist {
  background: var(--effect-landscape-mist);
  filter: blur(1.25rem);
}

.ink-landscape__mist--upper {
  top: 42%;
  height: 16%;
  transform: translateX(var(--mist-upper-x));
}

.ink-landscape__mist--lower {
  top: 68%;
  height: 13%;
  transform: translateX(var(--mist-lower-x));
}

.ink-landscape__grain {
  opacity: 0.16;
  background-image:
    radial-gradient(circle at 20% 30%, var(--effect-landscape-grain-ink) 0 0.5px, transparent 0.7px),
    radial-gradient(circle at 70% 60%, var(--effect-landscape-grain-gold) 0 0.45px, transparent 0.7px);
  background-size: 7px 7px, 11px 11px;
  mix-blend-mode: multiply;
}

.ink-landscape--static > * { transform: none; transition: none; }

@media (prefers-reduced-motion: reduce) {
  .ink-landscape > * { transform: none; transition: none; }
}
</style>
