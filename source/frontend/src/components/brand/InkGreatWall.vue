<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useMotionPreference } from '../../composables/useMotionPreference'

const props = defineProps({ parallax: { type: Boolean, default: true } })
const { canAnimate } = useMotionPreference()
const root = ref(null)
const coarsePointer = ref(false)
const isStatic = computed(() => !props.parallax || !canAnimate.value || coarsePointer.value)
let pointerFrameId, pointerX = 0, pointerY = 0, pointerMedia

function applyOffsets(x, y) {
  if (!root.value) return
  const s = root.value.style
  s.setProperty('--ax', `${x * -4}px`); s.setProperty('--ay', `${y * -3}px`)
  s.setProperty('--fx', `${x * 5}px`); s.setProperty('--fy', `${y * 2}px`)
  s.setProperty('--nx', `${x * 11}px`); s.setProperty('--ny', `${y * 4}px`)
  s.setProperty('--mx', `${x * -8}px`); s.setProperty('--lx', `${x * 6}px`)
}

function flushPointer() {
  pointerFrameId = undefined
  if (isStatic.value || !root.value) return
  const b = root.value.getBoundingClientRect()
  applyOffsets(((pointerX - b.left) / Math.max(b.width, 1) - 0.5) * 2, ((pointerY - b.top) / Math.max(b.height, 1) - 0.5) * 2)
}

function onMove(e) { if (!isStatic.value) { pointerX = e.clientX; pointerY = e.clientY; pointerFrameId ||= requestAnimationFrame(flushPointer) } }
function reset() { cancelAnimationFrame(pointerFrameId); pointerFrameId = undefined; applyOffsets(0, 0) }
function onCap(e) { coarsePointer.value = e.matches }

onMounted(() => {
  if (typeof window.matchMedia !== 'function') return
  pointerMedia = window.matchMedia('(pointer: coarse)')
  coarsePointer.value = pointerMedia.matches
  pointerMedia.addEventListener?.('change', onCap) ?? pointerMedia.addListener?.(onCap)
})
watch(isStatic, v => { if (v) reset() })
onBeforeUnmount(() => { reset(); pointerMedia?.removeEventListener?.('change', onCap) ?? pointerMedia?.removeListener?.(onCap) })
</script>

<template>
  <div ref="root" class="ink-wall" :class="{ 'ink-wall--static': isStatic }" aria-hidden="true" @pointermove="onMove" @pointerleave="reset">
    <!-- 天光 -->
    <svg class="ink-wall__sky" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <circle cx="200" cy="120" r="72" fill="var(--wl-sun)" opacity=".7" />
    </svg>
    <!-- 远山 -->
    <svg class="ink-wall__far" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <path d="M0 388 140 250l65 55 118-148 115 140 88-82 155 160 105-132 118 95 96-128 95 108 105-62v186H0Z" />
    </svg>
    <!-- 上雾 -->
    <div class="ink-wall__mist ink-wall__mist--upper" />
    <!-- 近山 + 长城 -->
    <svg class="ink-wall__near" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" focusable="false">
      <!-- 山体 -->
      <path d="M0 460 140 340l95 48 145-138 120 124 108-98 130 140 115-70 190 124 157-98v150H0Z" />
      <!-- 城墙 -->
      <path class="ink-wall__brick" d="M62 390h38M138 358l18-3v8l-18 3M230 318l72-9v8l-72 9M345 286l58-5v8l-58 5M440 318l52-2v8l-52 2M532 310l48 4v8l-48-4M618 318l44 6v8l-44-6M700 340l42 10v8l-42-10M785 362l36 10v8l-36-10M860 334l52 8v8l-52-8M940 342l50 6v8l-50-6M1020 326l60-6v8l-60 6M1100 330l40-4v8l-40 4" />
      <!-- 烽火台 -->
      <g class="ink-wall__tower" v-for="t in [{x:142,y:348},{y:280},{y:335},{y:302},{y:324},{y:324},{y:356},{y:340},{y:332},{y:322}]" :key="t.x">
        <rect :x="t.x" :y="t.y" width="10" height="18" rx="1" />
        <rect :x="t.x+2" :y="t.y-3" width="6" height="4" rx="1" />
      </g>
    </svg>
    <!-- 下雾 -->
    <div class="ink-wall__mist ink-wall__mist--lower" />
    <!-- 颗粒 -->
    <div class="ink-wall__grain" />
  </div>
</template>

<style scoped>
.ink-wall {
  position: relative;
  width: 100%;
  min-height: clamp(18rem, 44vw, 32rem);
  overflow: hidden;
  background: linear-gradient(to bottom, #1a1208, #2d1f0a 40%, #3d2a10 100%);
  isolation: isolate;
  --ax: 0px; --ay: 0px; --fx: 0px; --fy: 0px; --nx: 0px; --ny: 0px; --mx: 0px; --lx: 0px;
  --wl-sun: #e8b848;
}
.ink-wall__sky, .ink-wall__far, .ink-wall__near, .ink-wall__mist, .ink-wall__grain {
  position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none;
  transition: transform var(--duration-slow) var(--ease-out);
}
.ink-wall__sky {
  background: linear-gradient(to bottom, #3a2010, transparent);
  transform: translate3d(var(--ax), var(--ay), 0) scale(1.02);
}
.ink-wall__far {
  fill: #5a3820;
  transform: translate3d(var(--fx), var(--fy), 0) scale(1.025);
}
.ink-wall__near {
  fill: #3a2210;
  transform: translate3d(var(--nx), var(--ny), 0) scale(1.04);
}
.ink-wall__brick {
  fill: none;
  stroke: #c89048;
  stroke-linecap: round;
  stroke-width: 2.5;
}
.ink-wall__tower rect {
  fill: #4a2a12;
  stroke: #c89048;
  stroke-width: 1.2;
}
.ink-wall__mist {
  background: linear-gradient(90deg, transparent, rgb(232 184 72 / 12%) 30%, rgb(200 144 72 / 8%) 64%, transparent);
  filter: blur(1.25rem);
}
.ink-wall__mist--upper { top: 42%; height: 16%; transform: translateX(var(--mx)); }
.ink-wall__mist--lower { top: 68%; height: 13%; transform: translateX(var(--lx)); }
.ink-wall__grain {
  opacity: .18;
  background-image:
    radial-gradient(circle at 20% 30%, #8a6430 0 .5px, transparent .7px),
    radial-gradient(circle at 70% 60%, #c89048 0 .45px, transparent .7px);
  background-size: 7px 7px, 11px 11px;
  mix-blend-mode: overlay;
}
.ink-wall--static > * { transform: none; transition: none; }
@media (prefers-reduced-motion: reduce) { .ink-wall > * { transform: none; transition: none; } }
</style>
