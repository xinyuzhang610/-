# Home Visual Feedback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refine the 智教通 homepage so its entry controls, problem heading, journey portraits, and interactive hero reveal match the approved Eastern editorial design at every target viewport.

**Architecture:** Introduce three focused presentation units: `EntryLink` for shared CTA language, `JourneySubjectFrame` for crop-safe portrait composition, and `HeroScratchReveal` plus pure brush helpers for the Canvas interaction. Existing homepage sections keep ownership of their copy and routing; the new units receive narrow props and expose only the events their parents need.

**Tech Stack:** Vue 3 Composition API, Vue Router, scoped CSS, HTML Canvas 2D, Vitest, Vue Test Utils, jsdom, Vite.

---

## File map

- Create `source/frontend/src/components/home/EntryLink.vue`: shared teacher/student CTA with SVG guide glyph.
- Create `source/frontend/src/components/home/JourneySubjectFrame.vue`: blurred atmosphere plus uncropped foreground subject.
- Create `source/frontend/src/components/home/heroScratch.js`: deterministic brush radius and stroke interpolation helpers.
- Create `source/frontend/src/components/home/HeroScratchReveal.vue`: Canvas lifecycle, pointer sampling, redraw, fallback, and cleanup.
- Create `source/frontend/src/__tests__/EntryLink.test.js`: CTA structure, role theme, link, and accessible glyph checks.
- Create `source/frontend/src/__tests__/JourneySubjectFrame.test.js`: subject/background layer and alt-text checks.
- Create `source/frontend/src/__tests__/heroScratch.test.js`: pure interpolation and radius behavior.
- Create `source/frontend/src/__tests__/HeroScratchReveal.test.js`: reduced-motion, fallback, pointer, skip, and cleanup behavior.
- Modify `source/frontend/src/components/home/HeroSection.vue`: integrate shared links and Canvas reveal.
- Modify `source/frontend/src/components/home/PainSection.vue`: semantic two-line heading and stable responsive layout.
- Modify `source/frontend/src/components/home/DualJourney.vue`: integrate crop-safe frames and remove fixed cover behavior.
- Modify `source/frontend/src/components/home/FinalCall.vue`: reuse shared entry links.
- Modify `source/frontend/src/__tests__/Home.test.js`: integration assertions for all four feedback areas.
- Create `docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md`: viewport and interaction verification record.

### Task 1: Establish the shared Eastern editorial entry link

**Files:**
- Create: `source/frontend/src/components/home/EntryLink.vue`
- Create: `source/frontend/src/__tests__/EntryLink.test.js`
- Modify: `source/frontend/src/components/home/HeroSection.vue`
- Modify: `source/frontend/src/components/home/FinalCall.vue`
- Modify: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Write the failing component and integration tests**

Create `EntryLink.test.js`:

```js
import { describe, expect, it } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import EntryLink from '../components/home/EntryLink.vue'

function mountEntry(props) {
  return mount(EntryLink, {
    props,
    global: { stubs: { RouterLink: RouterLinkStub } }
  })
}

describe('EntryLink', () => {
  it('renders an SVG guide glyph instead of a text arrow', () => {
    const wrapper = mountEntry({ role: 'teacher', label: '教师入口', to: '/login?role=teacher' })

    expect(wrapper.text()).toBe('教师入口')
    expect(wrapper.text()).not.toContain('→')
    expect(wrapper.get('.entry-link__glyph svg').attributes('aria-hidden')).toBe('true')
    expect(wrapper.getComponent(RouterLinkStub).props('to')).toBe('/login?role=teacher')
  })

  it('applies the student theme without changing the component structure', () => {
    const wrapper = mountEntry({ role: 'student', label: '学生入口', to: '/student/guidance' })

    expect(wrapper.classes()).toContain('entry-link--student')
    expect(wrapper.findAll('.entry-link__frame')).toHaveLength(1)
  })
})
```

Extend the route test in `Home.test.js` with:

```js
expect(wrapper.findAll('.entry-link')).toHaveLength(4)
expect(wrapper.findAll('.entry-link__glyph svg')).toHaveLength(4)
expect(wrapper.text()).not.toContain('→')
```

- [ ] **Step 2: Run the tests and confirm the new contract fails**

Run:

```powershell
npm test -- --run src/__tests__/EntryLink.test.js src/__tests__/Home.test.js
```

Expected: FAIL because `EntryLink.vue` does not exist and the homepage still renders text arrows.

- [ ] **Step 3: Implement the shared link component**

Create `EntryLink.vue`:

```vue
<script setup>
defineProps({
  role: { type: String, required: true, validator: value => ['teacher', 'student'].includes(value) },
  label: { type: String, required: true },
  to: { type: [String, Object], required: true },
  testId: { type: String, default: '' }
})
</script>

<template>
  <RouterLink
    class="entry-link"
    :class="`entry-link--${role}`"
    :to="to"
    :data-testid="testId || undefined"
  >
    <span class="entry-link__frame" aria-hidden="true" />
    <span class="entry-link__label">{{ label }}</span>
    <span class="entry-link__glyph" aria-hidden="true">
      <svg viewBox="0 0 42 12" focusable="false">
        <path d="M1 6h34M29 1l7 5-7 5" />
      </svg>
    </span>
  </RouterLink>
</template>

<style scoped>
.entry-link { position: relative; display: inline-flex; min-height: 3rem; align-items: center; gap: 1.05rem; padding: .75rem 1rem .75rem 1.2rem; border: 1px solid rgb(213 166 79 / 72%); border-radius: .3rem; background: var(--ink-950); color: var(--moon-50); font-family: var(--font-body); font-size: .9rem; font-weight: 520; letter-spacing: .08em; text-decoration: none; transition: border-color var(--duration-fast), background var(--duration-fast), color var(--duration-fast); }
.entry-link__frame { position: absolute; inset: .22rem; border: 1px solid rgb(213 166 79 / 26%); border-radius: .16rem; pointer-events: none; }
.entry-link__label, .entry-link__glyph { position: relative; z-index: 1; }
.entry-link__glyph { display: inline-flex; color: var(--gold-200); transition: transform var(--duration-fast) var(--ease-out); }
.entry-link__glyph svg { width: 2.6rem; height: .75rem; overflow: visible; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1; }
.entry-link--student { border-color: rgb(110 210 181 / 66%); background: var(--jade-800); }
.entry-link:hover { color: var(--moon-50); }
.entry-link:hover .entry-link__glyph { transform: translateX(.25rem); }
.entry-link:focus-visible { outline: 2px solid var(--moon-50); outline-offset: .25rem; }
@media (prefers-reduced-motion: reduce) { .entry-link__glyph { transition: none; } .entry-link:hover .entry-link__glyph { transform: none; } }
</style>
```

Import `EntryLink` in `HeroSection.vue` and replace the two existing `RouterLink.entry` nodes with:

```vue
<EntryLink role="teacher" label="教师入口" to="/login?role=teacher" test-id="teacher-entry" />
<EntryLink role="student" label="学生入口" to="/student/guidance" test-id="student-entry" />
```

Delete the old `.entry`, `.entry--teacher`, `.entry--student`, and `.entry:hover` CSS rules.

Import `EntryLink` in `FinalCall.vue` and replace the two existing links with:

```vue
<EntryLink role="teacher" label="以教师身份开始" to="/login?role=teacher" />
<EntryLink role="student" label="以学生身份探索" to="/student/guidance" />
```

Delete the old `.call__actions a` and `.call__actions a:last-child` rules.

- [ ] **Step 4: Run the focused tests**

Run:

```powershell
npm test -- --run src/__tests__/EntryLink.test.js src/__tests__/Home.test.js
```

Expected: both test files PASS; four homepage entry links contain SVG glyphs and no text arrow.

- [ ] **Step 5: Commit the shared CTA work**

```powershell
git add source/frontend/src/components/home/EntryLink.vue source/frontend/src/components/home/HeroSection.vue source/frontend/src/components/home/FinalCall.vue source/frontend/src/__tests__/EntryLink.test.js source/frontend/src/__tests__/Home.test.js
git commit -m "feat: unify homepage entry links"
```

### Task 2: Stabilize the problem heading and its responsive grid

**Files:**
- Modify: `source/frontend/src/components/home/PainSection.vue`
- Modify: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Add the failing semantic-line assertion**

Add to `Home.test.js`:

```js
it('keeps the problem statement in two intentional semantic lines', async () => {
  const wrapper = await mountHome()
  const lines = wrapper.findAll('[data-testid="pain-heading-line"]')

  expect(lines).toHaveLength(2)
  expect(lines.map(line => line.text())).toEqual(['问题不在工具多少', '而在知识尚未成路'])
})
```

- [ ] **Step 2: Run the test and verify the old `<br>` structure fails**

Run:

```powershell
npm test -- --run src/__tests__/Home.test.js
```

Expected: FAIL because `[data-testid="pain-heading-line"]` does not exist.

- [ ] **Step 3: Implement intentional line structure and stable breakpoints**

Replace the heading in `PainSection.vue` with:

```vue
<h2>
  <span data-testid="pain-heading-line">问题不在工具多少</span>
  <strong data-testid="pain-heading-line">而在知识尚未成路</strong>
</h2>
```

Replace the grid and heading-related CSS with:

```css
.pain__grid { display: grid; grid-template-columns: minmax(18rem, .78fr) minmax(32rem, 1.35fr); gap: clamp(3rem, 7vw, 8rem); }
.pain__intro { position: sticky; top: 5rem; align-self: start; min-width: 0; }
h2 { max-width: 8.6em; font-family: var(--font-title); font-size: clamp(2.35rem, 4vw, 4.35rem); font-weight: 500; letter-spacing: -.035em; line-height: 1.12; }
h2 span, h2 strong { display: block; }
h2 span { color: var(--color-ink-soft); font-size: .66em; font-weight: 500; letter-spacing: .02em; }
h2 strong { margin-top: .35em; color: var(--ink-950); font-weight: 520; }
@media (max-width: 1100px) { .pain__grid { grid-template-columns: 1fr; gap: 3rem; } .pain__intro { position: static; } h2 { max-width: 11em; } }
@media (max-width: 640px) { h2 { font-size: clamp(2.05rem, 10vw, 3rem); } .pain__signals li { grid-template-columns: 2.5rem 1fr; } .pain__signal { grid-column: 2; max-width: none; } }
```

- [ ] **Step 4: Run the homepage tests**

Run:

```powershell
npm test -- --run src/__tests__/Home.test.js
```

Expected: PASS, with the two lines found in the approved order.

- [ ] **Step 5: Commit the heading refinement**

```powershell
git add source/frontend/src/components/home/PainSection.vue source/frontend/src/__tests__/Home.test.js
git commit -m "fix: stabilize homepage problem heading"
```

### Task 3: Replace cropped journey art with a complete subject frame

**Files:**
- Create: `source/frontend/src/components/home/JourneySubjectFrame.vue`
- Create: `source/frontend/src/__tests__/JourneySubjectFrame.test.js`
- Modify: `source/frontend/src/components/home/DualJourney.vue`
- Modify: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Write failing layer and integration tests**

Create `JourneySubjectFrame.test.js`:

```js
import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import JourneySubjectFrame from '../components/home/JourneySubjectFrame.vue'

const asset = { src: '/teacher.webp', width: 1693, height: 929, alt: '教师组织知识路径' }

describe('JourneySubjectFrame', () => {
  it('separates an atmospheric fill from the complete foreground subject', () => {
    const wrapper = mount(JourneySubjectFrame, { props: { asset, tone: 'teacher' } })

    expect(wrapper.get('.journey-subject__atmosphere').attributes('aria-hidden')).toBe('true')
    expect(wrapper.get('.journey-subject__subject').attributes('alt')).toBe(asset.alt)
    expect(wrapper.get('.journey-subject__subject').attributes('width')).toBe('1693')
    expect(wrapper.classes()).toContain('journey-subject--teacher')
  })

  it('removes broken image layers and retains the designed fallback surface', async () => {
    const wrapper = mount(JourneySubjectFrame, { props: { asset, tone: 'teacher' } })
    await wrapper.get('.journey-subject__subject').trigger('error')

    expect(wrapper.findAll('img')).toHaveLength(0)
    expect(wrapper.classes()).toContain('journey-subject--fallback')
  })
})
```

Add to `Home.test.js`:

```js
it('renders both journey illustrations in crop-safe subject frames', async () => {
  const wrapper = await mountHome()

  expect(wrapper.findAll('.journey-subject')).toHaveLength(2)
  expect(wrapper.findAll('.journey-subject__atmosphere')).toHaveLength(2)
  expect(wrapper.findAll('.journey-subject__subject')).toHaveLength(2)
})
```

- [ ] **Step 2: Run tests and confirm the frame is missing**

Run:

```powershell
npm test -- --run src/__tests__/JourneySubjectFrame.test.js src/__tests__/Home.test.js
```

Expected: FAIL because `JourneySubjectFrame.vue` and its layer classes do not exist.

- [ ] **Step 3: Implement the crop-safe frame**

Create `JourneySubjectFrame.vue`:

```vue
<script setup>
import { ref } from 'vue'

defineProps({
  asset: { type: Object, required: true },
  tone: { type: String, required: true, validator: value => ['teacher', 'student'].includes(value) }
})

const imageFailed = ref(false)
</script>

<template>
  <div
    class="journey-subject"
    :class="[`journey-subject--${tone}`, { 'journey-subject--fallback': imageFailed }]"
  >
    <img v-if="!imageFailed" class="journey-subject__atmosphere" :src="asset.src" alt="" aria-hidden="true" @error="imageFailed = true">
    <img
      v-if="!imageFailed"
      class="journey-subject__subject"
      :src="asset.src"
      :width="asset.width"
      :height="asset.height"
      :alt="asset.alt"
      loading="lazy"
      @error="imageFailed = true"
    >
  </div>
</template>

<style scoped>
.journey-subject { position: absolute; inset: 0; overflow: hidden; background: #17231f; }
.journey-subject__atmosphere { position: absolute; inset: -5%; width: 110%; height: 110%; object-fit: cover; filter: blur(1.3rem) saturate(.72) brightness(.64); opacity: .76; transform: scale(1.06); }
.journey-subject__subject { position: absolute; inset: 3% 2% 17%; width: 96%; height: 80%; object-fit: contain; object-position: center bottom; filter: drop-shadow(0 1.2rem 1.8rem rgb(4 12 9 / 28%)); transition: transform var(--duration-slow) var(--ease-out); }
.journey-subject--student { background: #16352f; }
.journey-subject--fallback::before { content: ''; position: absolute; inset: 10% 18%; border: 1px solid rgb(213 166 79 / 18%); border-radius: 50%; box-shadow: 0 0 5rem rgb(66 185 154 / 14%); }
@media (prefers-reduced-motion: reduce) { .journey-subject__subject { transition: none; } }
</style>
```

- [ ] **Step 4: Integrate the frame and remove cover cropping**

Import the component in `DualJourney.vue` and replace each direct `<img>` with:

```vue
<JourneySubjectFrame :asset="generatedAssets.teacherOrbit" tone="teacher" />
```

and:

```vue
<JourneySubjectFrame :asset="generatedAssets.studentOrbit" tone="student" />
```

Replace the card sizing, overlay, and hover rules with:

```css
.journey__split { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.journey__path { position: relative; min-height: 36rem; aspect-ratio: 1 / 1.06; overflow: hidden; color: var(--moon-50); }
.journey__path::after { content: ''; position: absolute; inset: 0; background: linear-gradient(0deg, rgb(10 20 17 / 96%) 0%, rgb(10 20 17 / 42%) 42%, transparent 72%); }
.journey__content { position: absolute; z-index: 2; right: 0; bottom: 0; left: 0; padding: clamp(2rem, 4vw, 4rem); }
.journey__path:hover :deep(.journey-subject__subject) { transform: translateY(-.4rem) scale(1.012); }
@media (max-width: 900px) { .journey__split { grid-template-columns: 1fr; } .journey__path { min-height: 34rem; aspect-ratio: auto; } }
@media (prefers-reduced-motion: reduce) { .journey__path:hover :deep(.journey-subject__subject) { transform: none; } }
```

Delete the old `.journey__path img` and `.journey__path:hover img` rules.

- [ ] **Step 5: Run focused tests and commit**

Run:

```powershell
npm test -- --run src/__tests__/JourneySubjectFrame.test.js src/__tests__/Home.test.js
```

Expected: PASS; both paths expose separate atmospheric and subject layers.

Commit:

```powershell
git add source/frontend/src/components/home/JourneySubjectFrame.vue source/frontend/src/components/home/DualJourney.vue source/frontend/src/__tests__/JourneySubjectFrame.test.js source/frontend/src/__tests__/Home.test.js
git commit -m "fix: preserve complete journey subjects"
```

### Task 4: Build and test deterministic brush math

**Files:**
- Create: `source/frontend/src/components/home/heroScratch.js`
- Create: `source/frontend/src/__tests__/heroScratch.test.js`

- [ ] **Step 1: Write failing brush helper tests**

Create `heroScratch.test.js`:

```js
import { describe, expect, it } from 'vitest'
import { brushRadius, interpolateStroke } from '../components/home/heroScratch'

describe('hero scratch helpers', () => {
  it('uses a broader brush for faster movement within safe bounds', () => {
    expect(brushRadius(0, 1000)).toBe(34)
    expect(brushRadius(2, 1000)).toBeGreaterThan(34)
    expect(brushRadius(100, 1000)).toBe(82)
  })

  it('interpolates long movements without gaps and preserves the destination', () => {
    const points = interpolateStroke({ x: 0, y: 0 }, { x: 100, y: 0 }, 20)

    expect(points.length).toBeGreaterThan(4)
    expect(points.at(-1)).toEqual({ x: 100, y: 0 })
    expect(points.every((point, index) => index === 0 || point.x - points[index - 1].x <= 20)).toBe(true)
  })
})
```

- [ ] **Step 2: Run the helper tests and confirm missing exports**

Run:

```powershell
npm test -- --run src/__tests__/heroScratch.test.js
```

Expected: FAIL because `heroScratch.js` does not exist.

- [ ] **Step 3: Implement the pure helpers**

Create `heroScratch.js`:

```js
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
```

- [ ] **Step 4: Run tests and commit the pure brush layer**

Run:

```powershell
npm test -- --run src/__tests__/heroScratch.test.js
```

Expected: PASS.

Commit:

```powershell
git add source/frontend/src/components/home/heroScratch.js source/frontend/src/__tests__/heroScratch.test.js
git commit -m "test: define hero scratch brush behavior"
```

### Task 5: Implement the Canvas reveal lifecycle and integrate it into the hero

**Files:**
- Create: `source/frontend/src/components/home/HeroScratchReveal.vue`
- Create: `source/frontend/src/__tests__/HeroScratchReveal.test.js`
- Modify: `source/frontend/src/components/home/HeroSection.vue`
- Modify: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Write failing Canvas lifecycle tests**

Create `HeroScratchReveal.test.js` with a reusable 2D context stub:

```js
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HeroScratchReveal from '../components/home/HeroScratchReveal.vue'

const gradient = { addColorStop: vi.fn() }
const context = {
  clearRect: vi.fn(), fillRect: vi.fn(), beginPath: vi.fn(), arc: vi.fn(), fill: vi.fn(),
  createLinearGradient: vi.fn(() => gradient), createRadialGradient: vi.fn(() => gradient),
  setTransform: vi.fn(), globalCompositeOperation: 'source-over', fillStyle: ''
}

function installBrowserStubs(reduced = false) {
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: reduced, addEventListener: vi.fn(), removeEventListener: vi.fn() })))
  vi.stubGlobal('requestAnimationFrame', vi.fn(callback => { callback(); return 1 }))
  vi.stubGlobal('cancelAnimationFrame', vi.fn())
  vi.stubGlobal('ResizeObserver', class { observe() {} disconnect() {} })
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context)
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({ left: 0, top: 0, width: 1000, height: 700, right: 1000, bottom: 700 })
}

describe('HeroScratchReveal', () => {
  beforeEach(() => installBrowserStubs(false))
  afterEach(() => vi.restoreAllMocks())

  it('paints a mask and erases it after desktop pointer movement', async () => {
    const wrapper = mount(HeroScratchReveal, { attachTo: document.body })
    await wrapper.get('canvas').trigger('pointermove', { pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20 })

    expect(context.fillRect).toHaveBeenCalled()
    expect(context.globalCompositeOperation).toBe('destination-out')
    expect(context.arc).toHaveBeenCalled()
    expect(wrapper.emitted('first-reveal')).toHaveLength(1)
  })

  it('removes the visual mask when skipped', async () => {
    const wrapper = mount(HeroScratchReveal, { props: { skipped: false } })
    await wrapper.setProps({ skipped: true })

    expect(wrapper.get('canvas').attributes('hidden')).toBeDefined()
  })

  it('uses the static fallback when reduced motion is requested', () => {
    vi.restoreAllMocks()
    installBrowserStubs(true)
    const wrapper = mount(HeroScratchReveal)

    expect(wrapper.attributes('data-static')).toBe('true')
  })

  it('cancels animation work and observers on unmount', () => {
    const wrapper = mount(HeroScratchReveal)
    wrapper.unmount()

    expect(cancelAnimationFrame).toHaveBeenCalled()
  })
})
```

Add to `Home.test.js`:

```js
it('provides a progressive hero reveal with a static reduced-motion state', async () => {
  const wrapper = await mountHome()

  expect(wrapper.get('[data-testid="hero-reveal-canvas"]').exists()).toBe(true)
  expect(wrapper.get('[data-testid="hero-scratch-reveal"]').attributes('data-static')).toBe('true')
})

it('keeps a clean hero surface when the background image cannot load', async () => {
  const wrapper = await mountHome()
  await wrapper.get('[data-testid="hero-background-image"]').trigger('error')

  expect(wrapper.find('[data-testid="hero-background-image"]').exists()).toBe(false)
  expect(wrapper.get('.hero__art').classes()).toContain('hero__art--fallback')
  expect(wrapper.get('[data-testid="teacher-entry"]').exists()).toBe(true)
})
```

- [ ] **Step 2: Run tests and verify the reveal component is missing**

Run:

```powershell
npm test -- --run src/__tests__/HeroScratchReveal.test.js src/__tests__/Home.test.js
```

Expected: FAIL because `HeroScratchReveal.vue` and the hero reveal test IDs do not exist.

- [ ] **Step 3: Implement the Canvas component**

Create `HeroScratchReveal.vue`:

```vue
<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { brushRadius, interpolateStroke } from './heroScratch'

const props = defineProps({ skipped: { type: Boolean, default: false } })
const emit = defineEmits(['first-reveal'])

const canvas = ref(null)
const staticMode = ref(false)
const points = []
let context
let observer
let frame = 0
let lastPoint
let firstRevealSent = false
let touchActive = false

function paintMask() {
  if (!context || !canvas.value) return
  const { width, height } = canvas.value.getBoundingClientRect()
  context.globalCompositeOperation = 'source-over'
  context.clearRect(0, 0, width, height)
  const wash = context.createLinearGradient(0, 0, width, height)
  wash.addColorStop(0, 'rgba(7, 17, 14, .97)')
  wash.addColorStop(.55, 'rgba(16, 31, 25, .90)')
  wash.addColorStop(1, 'rgba(43, 52, 43, .82)')
  context.fillStyle = wash
  context.fillRect(0, 0, width, height)
}

function erasePoint(point) {
  const edge = point.radius * (0.82 + Math.sin(point.seed) * 0.08)
  const brush = context.createRadialGradient(point.x, point.y, edge * .22, point.x, point.y, edge)
  brush.addColorStop(0, 'rgba(0, 0, 0, 1)')
  brush.addColorStop(.7, 'rgba(0, 0, 0, .88)')
  brush.addColorStop(1, 'rgba(0, 0, 0, 0)')
  context.globalCompositeOperation = 'destination-out'
  context.fillStyle = brush
  context.beginPath()
  context.arc(point.x, point.y, edge, 0, Math.PI * 2)
  context.fill()
}

function redraw() {
  if (!canvas.value || staticMode.value || props.skipped) return
  const rect = canvas.value.getBoundingClientRect()
  const ratio = Math.min(window.devicePixelRatio || 1, 2)
  canvas.value.width = Math.round(rect.width * ratio)
  canvas.value.height = Math.round(rect.height * ratio)
  context.setTransform(ratio, 0, 0, ratio, 0, 0)
  paintMask()
  points.forEach(point => erasePoint({ x: point.x * rect.width, y: point.y * rect.height, radius: point.radius * Math.min(rect.width, rect.height), seed: point.seed }))
}

function queuePoint(event) {
  if (staticMode.value || props.skipped || (event.pointerType === 'touch' && !touchActive)) return
  const rect = canvas.value.getBoundingClientRect()
  const current = { x: event.clientX - rect.left, y: event.clientY - rect.top, time: event.timeStamp || performance.now() }
  const elapsed = Math.max(8, current.time - (lastPoint?.time || current.time - 16))
  const distance = lastPoint ? Math.hypot(current.x - lastPoint.x, current.y - lastPoint.y) : 0
  const speed = distance / elapsed
  const radius = brushRadius(speed, Math.min(rect.width, rect.height))
  const samples = lastPoint ? interpolateStroke(lastPoint, current, Math.max(8, radius * .24)) : [current]
  samples.forEach((sample, index) => points.push({ x: sample.x / rect.width, y: sample.y / rect.height, radius: radius / Math.min(rect.width, rect.height), seed: points.length + index }))
  lastPoint = current
  if (!firstRevealSent) { firstRevealSent = true; emit('first-reveal') }
  if (!frame) frame = requestAnimationFrame(() => { frame = 0; redraw() })
}

function onPointerDown(event) { if (event.pointerType === 'touch') touchActive = true }
function onPointerUp() { touchActive = false; lastPoint = undefined }

function enterStaticMode() {
  staticMode.value = true
  points.length = 0
  if (canvas.value) canvas.value.hidden = true
}

onMounted(async () => {
  await nextTick()
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const lowMemory = Number(navigator.deviceMemory || 4) <= 2
  try { context = canvas.value?.getContext('2d') } catch { context = null }
  if (props.skipped || reduced || lowMemory || !context) { enterStaticMode(); return }
  canvas.value.addEventListener('pointermove', queuePoint)
  canvas.value.addEventListener('pointerdown', onPointerDown)
  canvas.value.addEventListener('pointerup', onPointerUp)
  canvas.value.addEventListener('pointercancel', onPointerUp)
  observer = new ResizeObserver(redraw)
  observer.observe(canvas.value)
  redraw()
})

watch(() => props.skipped, skipped => { if (skipped) enterStaticMode() })

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  observer?.disconnect()
  canvas.value?.removeEventListener('pointermove', queuePoint)
  canvas.value?.removeEventListener('pointerdown', onPointerDown)
  canvas.value?.removeEventListener('pointerup', onPointerUp)
  canvas.value?.removeEventListener('pointercancel', onPointerUp)
  points.length = 0
})
</script>

<template>
  <div class="hero-scratch" data-testid="hero-scratch-reveal" :data-static="staticMode ? 'true' : 'false'">
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
.hero-scratch { position: absolute; z-index: 1; inset: 0; pointer-events: none; }
.hero-scratch__canvas { width: 100%; height: 100%; pointer-events: auto; touch-action: pan-y; }
.hero-scratch__canvas[hidden] { display: none; }
</style>
```

- [ ] **Step 4: Integrate reveal state and guidance into `HeroSection.vue`**

Import `HeroScratchReveal`, add `hasRevealed` and `heroArtFailed`, and keep `animationSkipped`:

```js
import HeroScratchReveal from './HeroScratchReveal.vue'

const animationSkipped = ref(false)
const hasRevealed = ref(false)
const heroArtFailed = ref(false)
```

Update the `.hero__art` root and background image so a failed request leaves the designed background instead of a broken image icon:

```vue
<div class="hero__art" :class="{ 'hero__art--fallback': heroArtFailed }">
  <img
    v-if="!heroArtFailed"
    data-testid="hero-background-image"
    :src="generatedAssets.heroInkLandscape.src"
    :width="generatedAssets.heroInkLandscape.width"
    :height="generatedAssets.heroInkLandscape.height"
    :alt="generatedAssets.heroInkLandscape.alt"
    fetchpriority="high"
    @error="heroArtFailed = true"
  >
  <InkLandscape :parallax="!animationSkipped" class="hero__ink" />
  <KnowledgeCore class="hero__core" />
</div>
```

Place the reveal directly after `.hero__art` and before `.hero__content`:

```vue
<HeroScratchReveal :skipped="animationSkipped" @first-reveal="hasRevealed = true" />
```

Place the guidance after `.hero__actions`:

```vue
<p v-if="!hasRevealed && !animationSkipped" class="hero__reveal-hint" aria-hidden="true">
  移动光标，唤醒画卷
</p>
```

Change the art and content stacking and add guidance styles:

```css
.hero__art { position: absolute; z-index: 0; inset: 0; min-height: 46rem; }
.hero__art--fallback { background: radial-gradient(circle at 76% 42%, rgb(66 185 154 / 18%), transparent 28%), linear-gradient(135deg, #07110e, #17271f); }
.hero__content { position: relative; z-index: 2; display: flex; min-height: max(46rem, 100svh); flex-direction: column; justify-content: center; align-items: flex-start; padding-block: 8rem 5rem; pointer-events: none; }
.hero__content :is(a, button) { pointer-events: auto; }
.hero__reveal-hint { margin-top: 1rem; color: rgb(248 250 245 / 56%); font-size: .72rem; letter-spacing: .18em; }
```

This stacking lets the Canvas receive pointer movement in empty hero areas while links and the skip button remain clickable.

- [ ] **Step 5: Run lifecycle and integration tests**

Run:

```powershell
npm test -- --run src/__tests__/heroScratch.test.js src/__tests__/HeroScratchReveal.test.js src/__tests__/Home.test.js
```

Expected: PASS; reduced-motion mounting reports static state, normal mounting paints and erases, and homepage entry links remain present.

- [ ] **Step 6: Run the full suite and commit the reveal**

Run:

```powershell
npm test -- --run
```

Expected: all Vitest files PASS with no unhandled errors.

Commit:

```powershell
git add source/frontend/src/components/home/HeroScratchReveal.vue source/frontend/src/components/home/heroScratch.js source/frontend/src/components/home/HeroSection.vue source/frontend/src/__tests__/HeroScratchReveal.test.js source/frontend/src/__tests__/Home.test.js
git commit -m "feat: add interactive hero ink reveal"
```

### Task 6: Build, inspect every target viewport, and leave the demo running

**Files:**
- Create: `docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md`

- [ ] **Step 1: Run engineering verification from the frontend directory**

Run:

```powershell
npm test -- --run
npm run build
git diff --check
```

Expected: tests PASS, Vite production build exits with code 0, and `git diff --check` prints no errors.

- [ ] **Step 2: Ensure the demo server is running in demo mode**

From `source/frontend`, stop only the stale Vite process bound to port 5173 if necessary, then run:

```powershell
$env:VITE_DEMO_MODE='true'
npm run dev -- --host 127.0.0.1 --port 5173
```

Expected: Vite reports `http://127.0.0.1:5173/` and the page returns HTTP 200.

- [ ] **Step 3: Inspect desktop 1440×900**

Use the browser QA tool to open `http://127.0.0.1:5173/` at 1440×900. Move the pointer across the hero without pressing a button and verify irregular soft-edge reveal marks appear while unvisited areas remain covered. Verify all four CTAs use the thin SVG guide glyph and no text arrow.

- [ ] **Step 4: Inspect the two reported intermediate viewports**

At 1088×778 and 851×778, verify:

- the problem heading stays in the approved two semantic lines;
- teacher and student heads, hands, and principal silhouettes are complete;
- the atmosphere layer fills each card without visible empty bands;
- entry labels and guide glyphs remain aligned;
- links stay clickable above the Canvas;
- no horizontal scrollbar appears.

- [ ] **Step 5: Inspect mobile 390×844 and reduced motion**

At 390×844, verify journey cards are single-column and subjects remain complete. Emulate touch input: vertical swipes scroll and horizontal/diagonal drags reveal the hero. Emulate `prefers-reduced-motion: reduce` and verify the background is static with no Canvas mask while all content remains visible.

- [ ] **Step 6: Check runtime health**

Verify the browser console has no errors after hero movement, resize, route navigation, and return to `/`. Confirm there is no retained Canvas listener behavior after leaving the homepage.

- [ ] **Step 7: Record QA evidence**

After completing every check, create `docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md` with this exact structure. Save `PASS` only for checks supported by the current run; stop and fix the implementation before recording any failed check as complete:

```markdown
# Home Visual Feedback QA — 2026-07-14

## Automated verification

- Vitest: PASS
- Vite production build: PASS
- `git diff --check`: PASS

## Viewports

| Viewport | CTA | Pain heading | Complete subjects | Scratch interaction | Overflow/console |
| --- | --- | --- | --- | --- | --- |
| 1440×900 | PASS | PASS | PASS | PASS | PASS |
| 1088×778 | PASS | PASS | PASS | PASS | PASS |
| 851×778 | PASS | PASS | PASS | PASS | PASS |
| 390×844 | PASS | PASS | PASS | PASS | PASS |

## Accessibility and fallback

- Keyboard focus and link activation: PASS
- Reduced-motion static fallback: PASS
- Touch vertical scrolling and deliberate reveal: PASS

## Runtime

- Demo URL: http://127.0.0.1:5173/
- Browser console errors: none
```

- [ ] **Step 8: Commit verified QA evidence**

```powershell
git add docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md
git commit -m "test: verify homepage visual feedback fixes"
```

- [ ] **Step 9: Leave the Vite service running for user acceptance**

Open `http://127.0.0.1:5173/` in the app browser and do not stop the Vite process. Report the exact URL, test/build results, and any known visual limitation to the user.

## Plan self-review

- Spec coverage: tasks map to all eight feedback items, the approved CTA direction, persistent unrevealed mask, pointer-without-click desktop behavior, deliberate touch behavior, resize replay, fallback, cleanup, and all four target viewports.
- Placeholder scan: implementation steps contain concrete files, code, commands, expected results, and QA criteria; no deferred decisions remain.
- Type consistency: `role`, `label`, `to`, `testId`, `asset`, `tone`, `skipped`, and `first-reveal` use the same names in component definitions, parents, and tests.
