# Hero Living Ink Reveal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the permanent hero scratch trail with a Xiaomi-inspired, short-lived ink reveal that exposes the existing generated landscape only around the current pointer path.

**Architecture:** Keep the generated landscape as the bottom layer and use a transparent wrapper containing a Canvas mask above it. Model each pointer sample as a time-bound ink stamp; every animation frame repaints the full mask, removes expired stamps, and carves only living stamps with irregular radial gradients.

**Tech Stack:** Vue 3 Composition API, Canvas 2D, Vitest, Vue Test Utils, Vite, agent-browser

---

## File map

- Modify `source/frontend/src/components/home/heroScratch.js`: own lifecycle constants and pure stamp sampling helpers.
- Modify `source/frontend/src/__tests__/heroScratch.test.js`: verify lifetime, easing, radius variation, expiration, and path interpolation.
- Modify `source/frontend/src/components/home/HeroScratchReveal.vue`: own Canvas sizing, live stamp queue, per-frame repaint/carve loop, and cleanup.
- Modify `source/frontend/src/__tests__/HeroScratchReveal.test.js`: verify frame repaint, temporary reveal, re-entry behavior, static fallback, and cleanup.
- Modify `source/frontend/src/components/home/HeroSection.vue`: expose the generated art more clearly and preserve text contrast.
- Modify `source/frontend/src/__tests__/Home.test.js`: verify the generated image remains the reveal target and the reveal layer stays between art and content.

### Task 1: Add pure living-ink lifecycle helpers

**Files:**
- Modify: `source/frontend/src/components/home/heroScratch.js`
- Test: `source/frontend/src/__tests__/heroScratch.test.js`

- [ ] **Step 1: Write failing lifecycle tests**

Add imports and tests that define the exact public behavior:

```js
import {
  INK_REVEAL,
  createInkStamp,
  interpolateStroke,
  sampleInkStamp
} from '../components/home/heroScratch'

it('matches the approved living ink timing and spacing', () => {
  expect(INK_REVEAL).toMatchObject({
    startRadius: 8,
    endRadius: 128,
    radiusVariation: 0.45,
    lifetime: 520,
    spacing: 12,
    maxStamps: 160
  })
})

it('expands and fades a deterministic stamp during its lifetime', () => {
  const stamp = createInkStamp({ x: 20, y: 30, now: 100, random: () => 0.5 })
  const sample = sampleInkStamp(stamp, 360)

  expect(sample.x).toBe(20)
  expect(sample.y).toBe(30)
  expect(sample.radius).toBeCloseTo(87.8, 1)
  expect(sample.alpha).toBeCloseTo(0.75, 2)
})

it('expires a stamp after 520 milliseconds', () => {
  const stamp = createInkStamp({ x: 20, y: 30, now: 100, random: () => 0.5 })
  expect(sampleInkStamp(stamp, 620)).toBeNull()
})
```

Update the existing interpolation test to use `INK_REVEAL.spacing` and retain its destination and maximum-gap assertions.

- [ ] **Step 2: Run the helper tests and verify RED**

Run:

```powershell
cd source/frontend
npm test -- --run src/__tests__/heroScratch.test.js
```

Expected: FAIL because `INK_REVEAL`, `createInkStamp`, and `sampleInkStamp` are not exported.

- [ ] **Step 3: Implement the minimal lifecycle helpers**

Replace the speed-dependent permanent brush helper with:

```js
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
```

Keep `interpolateStroke(from, to, spacing)` unchanged because it already provides bounded-gap samples.

- [ ] **Step 4: Run helper tests and verify GREEN**

Run the same focused command. Expected: all `heroScratch.test.js` tests PASS.

- [ ] **Step 5: Commit the helper cycle**

```powershell
git add source/frontend/src/components/home/heroScratch.js source/frontend/src/__tests__/heroScratch.test.js
git commit -m "feat: model temporary hero ink stamps"
```

### Task 2: Repaint and close the Canvas mask every frame

**Files:**
- Modify: `source/frontend/src/components/home/HeroScratchReveal.vue`
- Test: `source/frontend/src/__tests__/HeroScratchReveal.test.js`

- [ ] **Step 1: Rewrite the browser stubs for controllable animation frames**

Use a queued animation-frame stub instead of invoking callbacks synchronously:

```js
const animationFrames = []

function runNextFrame(now) {
  const callback = animationFrames.shift()
  expect(callback).toBeTypeOf('function')
  callback(now)
}

vi.stubGlobal('requestAnimationFrame', vi.fn((callback) => {
  animationFrames.push(callback)
  return animationFrames.length
}))
```

Extend the context mock with `moveTo`, `lineTo`, and `closePath`. Make `matchMedia` return `true` for `(hover: hover)` and the supplied reduced-motion value for `(prefers-reduced-motion: reduce)`.

- [ ] **Step 2: Write failing component behavior tests**

Replace the permanent-erasure assertion with temporary-frame behavior:

```js
it('repaints the mask before carving each living ink frame', async () => {
  const wrapper = mount(HeroScratchReveal, { attachTo: document.body })
  const initialPaints = context.fillRect.mock.calls.length

  await wrapper.get('canvas').trigger('pointermove', {
    pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
  })
  runNextFrame(20)

  expect(context.fillRect.mock.calls.length).toBeGreaterThan(initialPaints)
  expect(context.createRadialGradient).toHaveBeenCalled()
  expect(context.lineTo).toHaveBeenCalled()
  expect(wrapper.emitted('first-reveal')).toHaveLength(1)
  wrapper.unmount()
})

it('closes the revealed area after the stamp lifetime', async () => {
  const wrapper = mount(HeroScratchReveal)
  await wrapper.get('canvas').trigger('pointermove', {
    pointerType: 'mouse', clientX: 300, clientY: 260, timeStamp: 20
  })
  runNextFrame(20)
  const carvedPaths = context.beginPath.mock.calls.length
  runNextFrame(541)

  expect(context.fillRect.mock.calls.length).toBeGreaterThan(2)
  expect(context.beginPath.mock.calls.length).toBe(carvedPaths)
  wrapper.unmount()
})
```

Retain and adapt the pointer-leave, reduced-motion, skipped, and cleanup tests. Add a no-hover assertion that expects `data-static="true"`.

- [ ] **Step 3: Run the component test and verify RED**

Run:

```powershell
cd source/frontend
npm test -- --run src/__tests__/HeroScratchReveal.test.js
```

Expected: FAIL because the component still keeps permanent normalized points and does not repaint on animation frames.

- [ ] **Step 4: Implement the living stamp loop**

Import the pure helpers:

```js
import {
  INK_REVEAL,
  createInkStamp,
  interpolateStroke,
  sampleInkStamp
} from './heroScratch'
```

Replace permanent `normalizedPoints` and `pendingPoints` with `const stamps = []`, `let lastPoint`, and `let running = false`. Add stamps with `createInkStamp`, cap the array at `INK_REVEAL.maxStamps`, and interpolate using `INK_REVEAL.spacing`.

Implement a frame loop with this order:

```js
function drawFrame(now) {
  frame = 0
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
```

`carveInk` must create a radial gradient with stops at `0`, `0.55`, and `1`, then draw a 32-segment closed path. Perturb each segment radius with:

```js
const wobble = 0.78
  + 0.14 * Math.sin(angle * 3 + sample.seed)
  + 0.08 * Math.sin(angle * 7 + sample.seed * 2.1)
  + 0.05 * Math.sin(angle * 13 + sample.seed * 0.7)
```

`resizeAndRedraw` must resize for DPR, call `paintMask()`, reset `lastPoint`, and never replay prior stamps. `pointerleave` resets only `lastPoint`; existing stamps continue to expire naturally.

Enable the effect only when `(hover: hover)` is true, reduced motion is false, memory is above 2 GB, and Canvas is available. Remove touch gesture state and handlers because touch uses the static full-art fallback.

- [ ] **Step 5: Remove the opaque wrapper background**

Change the component styles to:

```css
.hero-scratch {
  position: absolute;
  z-index: 1;
  inset: 0;
  background: transparent;
  pointer-events: none;
}

.hero-scratch__canvas {
  width: 100%;
  height: 100%;
  filter: contrast(1.04);
  pointer-events: auto;
}
```

Keep the static and hidden selectors. This is the key layer fix: transparent Canvas pixels now reveal `hero__art` rather than the wrapper.

- [ ] **Step 6: Run component and helper tests and verify GREEN**

Run:

```powershell
npm test -- --run src/__tests__/heroScratch.test.js src/__tests__/HeroScratchReveal.test.js
```

Expected: both files PASS with no unhandled animation callbacks.

- [ ] **Step 7: Commit the Canvas cycle**

```powershell
git add source/frontend/src/components/home/HeroScratchReveal.vue source/frontend/src/__tests__/HeroScratchReveal.test.js
git commit -m "feat: add self-closing hero ink reveal"
```

### Task 3: Make the revealed generated landscape visually rewarding

**Files:**
- Modify: `source/frontend/src/components/home/HeroSection.vue`
- Test: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Add a failing reveal-target and layer-order test**

Mount the home page and assert that the art, reveal component, and content appear in that DOM order and that the generated background image remains present:

```js
const hero = wrapper.get('[data-testid="hero-section"]')
const children = [...hero.element.children]
const artIndex = children.findIndex((node) => node.classList.contains('hero__art'))
const revealIndex = children.findIndex((node) => node.matches('[data-testid="hero-scratch-reveal"]'))
const contentIndex = children.findIndex((node) => node.classList.contains('hero__content'))

expect(artIndex).toBeLessThan(revealIndex)
expect(revealIndex).toBeLessThan(contentIndex)
expect(hero.get('.hero__art').attributes('data-reveal-target')).toBe('generated-landscape')
expect(hero.get('[data-testid="hero-background-image"]').attributes('src')).toContain('hero-ink-landscape')
```

- [ ] **Step 2: Run the home test and verify RED**

Run:

```powershell
npm test -- --run src/__tests__/Home.test.js
```

Expected: FAIL because `.hero__art` does not yet expose `data-reveal-target="generated-landscape"`.

- [ ] **Step 3: Tune the art without changing content layout**

Add the explicit reveal target to the existing art wrapper:

```vue
<div
  class="hero__art"
  data-reveal-target="generated-landscape"
  :class="{ 'hero__art--fallback': heroArtFailed }"
>
```

Keep `hero-ink-landscape.webp` and update only visual treatment:

```css
.hero__art::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgb(5 15 12 / 90%) 0%, rgb(7 18 14 / 58%) 42%, rgb(7 18 14 / 8%) 72%),
    linear-gradient(0deg, rgb(5 14 11 / 72%), transparent 34%);
}

.hero__art > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: .96;
  filter: saturate(1.06) contrast(1.05) brightness(1.04);
}
```

Keep the existing mobile text-protection gradient. Do not change copy, typography, buttons, or generated assets.

- [ ] **Step 4: Run the home test and verify GREEN**

Run the focused home test. Expected: PASS.

- [ ] **Step 5: Commit the visual cycle**

```powershell
git add source/frontend/src/components/home/HeroSection.vue source/frontend/src/__tests__/Home.test.js
git commit -m "style: clarify the hero reveal artwork"
```

### Task 4: Full verification and browser acceptance

**Files:**
- Update: `docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md`

- [ ] **Step 1: Run the complete automated suite**

```powershell
cd source/frontend
npm test -- --run
```

Expected: all test files and tests PASS.

- [ ] **Step 2: Build production assets and check whitespace**

```powershell
npm run build
git diff --check
```

Expected: Vite exits `0`; `git diff --check` prints no errors.

- [ ] **Step 3: Inspect the effect in a real browser**

At `1440x900`, `1088x778`, and `851x778`:

1. Capture the untouched hero.
2. Move across the generated knowledge core and capture within `120ms`; the landscape must be visibly exposed.
3. Capture again after at least `700ms` without moving; the prior reveal must be closed.
4. Move to a distant point; no bridge may connect the old and new locations.
5. Confirm entry links remain clickable, horizontal overflow is zero, and browser errors are empty.

At `390x844` and with reduced motion:

1. Confirm `data-static="true"`.
2. Confirm the Canvas is hidden and the full artwork is visible.
3. Confirm teacher and student entry links remain usable.

- [ ] **Step 4: Record QA evidence**

Append the exact automated counts, build result, viewport results, temporary reveal timing, static fallback result, and console-error result to `docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md`.

- [ ] **Step 5: Commit QA evidence**

```powershell
git add docs/superpowers/reports/2026-07-14-home-visual-feedback-qa.md
git commit -m "test: verify temporary hero ink reveal"
```
