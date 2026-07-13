<script setup>
import { computed, ref } from 'vue'
import { useMotionPreference } from '../../composables/useMotionPreference'

const props = defineProps({
  parallax: {
    type: Boolean,
    default: true
  }
})

const { canAnimate } = useMotionPreference()
const offsetX = ref(0)
const offsetY = ref(0)
const isStatic = computed(() => !props.parallax || !canAnimate.value)
const landscapeStyle = computed(() => ({
  '--art-x': `${offsetX.value * -4}px`,
  '--art-y': `${offsetY.value * -3}px`,
  '--far-x': `${offsetX.value * 5}px`,
  '--far-y': `${offsetY.value * 2}px`,
  '--near-x': `${offsetX.value * 11}px`,
  '--near-y': `${offsetY.value * 4}px`,
  '--mist-upper-x': `${offsetX.value * -8}px`,
  '--mist-lower-x': `${offsetX.value * 6}px`
}))

function handlePointerMove(event) {
  if (isStatic.value) return
  const bounds = event.currentTarget.getBoundingClientRect()
  offsetX.value = ((event.clientX - bounds.left) / Math.max(bounds.width, 1) - 0.5) * 2
  offsetY.value = ((event.clientY - bounds.top) / Math.max(bounds.height, 1) - 0.5) * 2
}

function resetPointer() {
  offsetX.value = 0
  offsetY.value = 0
}
</script>

<template>
  <div
    class="ink-landscape"
    :class="{ 'ink-landscape--static': isStatic }"
    :style="landscapeStyle"
    aria-hidden="true"
    @pointermove="handlePointerMove"
    @pointerleave="resetPointer"
  >
    <svg class="ink-landscape__artwork" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <defs>
        <linearGradient id="ink-sky" x1="0" y1="0" x2="0" y2="1">
          <stop stop-color="var(--moon-50)" stop-opacity="0" />
          <stop offset="1" stop-color="var(--jade-200)" stop-opacity=".26" />
        </linearGradient>
      </defs>
      <rect width="1200" height="520" fill="url(#ink-sky)" />
      <circle cx="900" cy="108" r="58" fill="var(--gold-200)" fill-opacity=".7" />
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

.ink-landscape__artwork { transform: translate3d(var(--art-x), var(--art-y), 0) scale(1.02); }

.ink-landscape__mountains--far {
  fill: var(--jade-700);
  fill-opacity: 0.12;
  transform: translate3d(var(--far-x), var(--far-y), 0) scale(1.025);
}

.ink-landscape__mountains--near {
  fill: var(--ink-800);
  fill-opacity: 0.72;
  transform: translate3d(var(--near-x), var(--near-y), 0) scale(1.04);
}

.ink-landscape__ridge {
  fill: none;
  stroke: var(--gold-400);
  stroke-linecap: round;
  stroke-width: 2;
}

.ink-landscape__mist {
  background: linear-gradient(90deg, transparent, rgb(248 250 245 / 82%) 30%, rgb(240 242 233 / 66%) 64%, transparent);
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
    radial-gradient(circle at 20% 30%, var(--ink-600) 0 0.5px, transparent 0.7px),
    radial-gradient(circle at 70% 60%, var(--gold-600) 0 0.45px, transparent 0.7px);
  background-size: 7px 7px, 11px 11px;
  mix-blend-mode: multiply;
}

.ink-landscape--static > * { transform: none; transition: none; }

@media (prefers-reduced-motion: reduce) {
  .ink-landscape > * { transform: none; transition: none; }
}
</style>
