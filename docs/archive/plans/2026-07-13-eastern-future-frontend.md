# Eastern Future Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the 智教通 Vue frontend as a cohesive “东方未来主义” experience with a cinematic landing page, refined teacher/student workspaces, generated visual assets, responsive behavior, and verified existing routes.

**Architecture:** Keep Vue 3, Vue Router, Pinia, Element Plus, and the existing API modules. Introduce focused brand, motion, UI, data, and feedback components; keep heavy visuals lazy and self-contained; expose demo mode through an explicit environment variable rather than silent API fallback.

**Tech Stack:** Vue 3 Composition API, Vue Router, Pinia, Element Plus, Vitest, Vue Test Utils, CSS custom properties, Canvas 2D, IntersectionObserver, generated WebP assets.

---

## File map

- `src/styles/tokens.css`: color, type, spacing, material, shadow, and motion tokens.
- `src/styles/global.css`: reset, typography, focus, reduced-motion, and shared page primitives.
- `src/composables/useMotionPreference.js`: reduced-motion and animation capability state.
- `src/composables/useReveal.js`: reusable IntersectionObserver reveal behavior.
- `src/composables/useDemoMode.js`: explicit demo-mode flag and label.
- `src/components/brand/KnowledgeCore.vue`: animated Canvas knowledge core with static fallback.
- `src/components/brand/InkLandscape.vue`: layered hero artwork and parallax wrapper.
- `src/components/brand/BrandMark.vue`: consistent 智教通 mark.
- `src/components/motion/RevealSection.vue`: accessible reveal container.
- `src/components/ui/AppButton.vue`, `GlassPanel.vue`, `StatusState.vue`: shared interaction and state primitives.
- `src/components/data/MetricCard.vue`: dashboard metric primitive.
- `src/data/demo.js`: explicitly labeled teacher/student presentation data.
- `src/assets/generated/`: project-bound generated artwork.
- `src/views/Home.vue`: cinematic marketing narrative.
- `src/layout/index.vue`: unified teacher/student workspace shell.
- `src/views/Login.vue`, `Register.vue`: identity-led authentication experience.
- `src/views/teacher/*.vue`: teacher dashboard, guidance, and tools experience.
- `src/views/student/*.vue`: student guidance, plaza, chat, records, and tool use experience.
- `src/__tests__/`: behavior tests for primitives, routing, demo mode, and core screens.

### Task 1: Establish design tokens and motion foundations

**Files:**
- Create: `source/frontend/src/styles/tokens.css`
- Create: `source/frontend/src/composables/useMotionPreference.js`
- Create: `source/frontend/src/composables/useReveal.js`
- Modify: `source/frontend/src/styles/global.css`
- Modify: `source/frontend/src/main.js`
- Test: `source/frontend/src/__tests__/motionPreference.test.js`

- [ ] **Step 1: Write the failing motion-preference test**

```js
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useMotionPreference } from '../composables/useMotionPreference'

describe('useMotionPreference', () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockReturnValue({
      matches: true,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    })
  })

  it('disables decorative motion when the user prefers reduced motion', () => {
    const { canAnimate } = useMotionPreference()
    expect(canAnimate.value).toBe(false)
  })
})
```

- [ ] **Step 2: Run the test and verify the module is missing**

Run: `cd source/frontend && npm test -- --run src/__tests__/motionPreference.test.js`  
Expected: FAIL because `useMotionPreference.js` does not exist.

- [ ] **Step 3: Implement the motion preference composable**

```js
import { computed, onBeforeUnmount, ref } from 'vue'

export function useMotionPreference() {
  const query = window.matchMedia('(prefers-reduced-motion: reduce)')
  const reduced = ref(query.matches)
  const update = (event) => { reduced.value = event.matches }
  query.addEventListener?.('change', update)
  onBeforeUnmount(() => query.removeEventListener?.('change', update))
  return { reduced, canAnimate: computed(() => !reduced.value) }
}
```

- [ ] **Step 4: Add tokens and global accessibility rules**

Define `--ink-950`, `--jade-400`, `--gold-400`, `--moon-50`, `--cinnabar-500`, typography sizes, spacing, radii, shadows, material backgrounds, `:focus-visible`, selection colors, and a `prefers-reduced-motion` block. Import `tokens.css` before `global.css` in `main.js`.

- [ ] **Step 5: Implement `useReveal`**

Return `{ target, visible }`; use `IntersectionObserver` with `{ threshold: 0.18 }`, immediately reveal when reduced motion is enabled, and disconnect on unmount.

- [ ] **Step 6: Run the focused and existing tests**

Run: `cd source/frontend && npm test -- --run`  
Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add source/frontend/src/styles source/frontend/src/composables source/frontend/src/main.js source/frontend/src/__tests__/motionPreference.test.js
git commit -m "feat: establish eastern future design foundations"
```

### Task 2: Build the brand and UI primitives

**Files:**
- Create: `source/frontend/src/components/brand/BrandMark.vue`
- Create: `source/frontend/src/components/brand/KnowledgeCore.vue`
- Create: `source/frontend/src/components/brand/InkLandscape.vue`
- Create: `source/frontend/src/components/motion/RevealSection.vue`
- Create: `source/frontend/src/components/ui/AppButton.vue`
- Create: `source/frontend/src/components/ui/GlassPanel.vue`
- Create: `source/frontend/src/components/ui/StatusState.vue`
- Test: `source/frontend/src/__tests__/brandPrimitives.test.js`

- [ ] **Step 1: Write failing primitive tests**

```js
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BrandMark from '../components/brand/BrandMark.vue'
import AppButton from '../components/ui/AppButton.vue'

describe('brand primitives', () => {
  it('renders the canonical product name', () => {
    expect(mount(BrandMark).text()).toContain('智教通')
  })

  it('emits click and exposes a minimum-size button class', async () => {
    const wrapper = mount(AppButton, { slots: { default: '开始体验' } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toHaveLength(1)
    expect(wrapper.classes()).toContain('app-button')
  })
})
```

- [ ] **Step 2: Run the tests and confirm missing components**

Run: `cd source/frontend && npm test -- --run src/__tests__/brandPrimitives.test.js`  
Expected: FAIL with component import errors.

- [ ] **Step 3: Implement BrandMark, AppButton, GlassPanel, and StatusState**

`BrandMark` renders an SVG seal plus “智教通”; `AppButton` supports `variant="gold|jade|ghost"`, native `disabled`, and a loading label; `GlassPanel` exposes a default slot; `StatusState` accepts `type`, `title`, and `description` and emits `retry`.

- [ ] **Step 4: Implement KnowledgeCore**

Use a Canvas 2D renderer with a capped particle count, `requestAnimationFrame`, `ResizeObserver`, mouse parallax, device-pixel-ratio clamping at 2, cleanup on unmount, and a static SVG/CSS fallback when `canAnimate` is false.

- [ ] **Step 5: Implement InkLandscape and RevealSection**

`InkLandscape` renders separate artwork, mist, mountain, and grain layers; `RevealSection` consumes `useReveal` and exposes `data-visible` without hiding semantic content from assistive technology.

- [ ] **Step 6: Run tests and build**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and Vite build succeeds.

- [ ] **Step 7: Commit**

```bash
git add source/frontend/src/components source/frontend/src/__tests__/brandPrimitives.test.js
git commit -m "feat: add eastern future brand primitives"
```

### Task 3: Generate and integrate project artwork

**Files:**
- Create: `source/frontend/src/assets/generated/hero-ink-landscape.webp`
- Create: `source/frontend/src/assets/generated/teacher-orbit.webp`
- Create: `source/frontend/src/assets/generated/student-orbit.webp`
- Create: `source/frontend/src/assets/generated/knowledge-universe.webp`
- Create: `source/frontend/src/assets/generated/asset-manifest.js`
- Test: `source/frontend/src/__tests__/assets.test.js`

- [ ] **Step 1: Write the asset-manifest test**

```js
import { describe, expect, it } from 'vitest'
import { generatedAssets } from '../assets/generated/asset-manifest'

describe('generated artwork manifest', () => {
  it('provides alt text and dimensions for every content image', () => {
    for (const asset of Object.values(generatedAssets)) {
      expect(asset.src).toMatch(/\.webp$/)
      expect(asset.width).toBeGreaterThan(1000)
      expect(asset.height).toBeGreaterThan(500)
      expect(typeof asset.alt).toBe('string')
    }
  })
})
```

- [ ] **Step 2: Generate four raster assets with the image-generation skill**

Use these fixed constraints for every prompt: Eastern futurism, cinematic high contrast, ink-black/gold/jade palette, no text, no logos, no watermark, no robots, intentional negative space for UI copy. Generate the hero as a wide digital Chinese landscape; teacher/student scenes as abstract human silhouettes interacting with knowledge orbits; knowledge universe as tools and learning nodes around a luminous core.

- [ ] **Step 3: Inspect every generated image**

Confirm subject, palette, usable negative space, absence of text/watermark, and consistency. Regenerate only the asset that violates a constraint.

- [ ] **Step 4: Save optimized project assets and manifest**

Convert selected images to WebP, retain useful source dimensions, and export objects with `src`, `width`, `height`, and meaningful `alt` text. Decorative hero layers use an empty `alt` at the consuming component.

- [ ] **Step 5: Run asset tests and build**

Run: `cd source/frontend && npm test -- --run src/__tests__/assets.test.js && npm run build`  
Expected: manifest test PASS and images resolve in the production build.

- [ ] **Step 6: Commit**

```bash
git add source/frontend/src/assets/generated source/frontend/src/__tests__/assets.test.js
git commit -m "feat: add generated eastern future artwork"
```

### Task 4: Rebuild the cinematic landing page

**Files:**
- Create: `source/frontend/src/components/home/HeroSection.vue`
- Create: `source/frontend/src/components/home/PainSection.vue`
- Create: `source/frontend/src/components/home/CapabilityOrbit.vue`
- Create: `source/frontend/src/components/home/DualJourney.vue`
- Create: `source/frontend/src/components/home/ProductShowcase.vue`
- Create: `source/frontend/src/components/home/FinalCall.vue`
- Rewrite: `source/frontend/src/views/Home.vue`
- Modify: `source/frontend/src/__tests__/Home.test.js`

- [ ] **Step 1: Replace the Home test with narrative and navigation expectations**

```js
it('renders the complete knowledge-awakening narrative', () => {
  const wrapper = mount(Home, { global: { plugins: [router] } })
  expect(wrapper.text()).toContain('让每一次提问，照亮学习路径')
  expect(wrapper.text()).toContain('发现需求')
  expect(wrapper.text()).toContain('工具广场')
  expect(wrapper.find('[data-testid="teacher-entry"]').exists()).toBe(true)
  expect(wrapper.find('[data-testid="student-entry"]').exists()).toBe(true)
})
```

- [ ] **Step 2: Run Home tests and verify they fail against the old page**

Run: `cd source/frontend && npm test -- --run src/__tests__/Home.test.js`  
Expected: FAIL because the new headline and test IDs are absent.

- [ ] **Step 3: Implement HeroSection and Home composition**

Use `InkLandscape`, `KnowledgeCore`, `BrandMark`, semantic `h1`, teacher route `/login?role=teacher`, student route `/student/guidance`, skip-animation control, and fixed-height artwork space to avoid layout shift.

- [ ] **Step 4: Implement the five narrative sections**

Each section is a focused component. CapabilityOrbit lists exactly five existing capabilities; DualJourney links only to existing routes; ProductShowcase uses real screen content; FinalCall repeats the two valid entry actions.

- [ ] **Step 5: Add responsive and reduced-motion behavior**

At widths below 900px, replace sticky split layouts with a single flow; below 640px, simplify the orbit to cards; in reduced-motion mode, render every section visible without transform transitions.

- [ ] **Step 6: Run Home tests and production build**

Run: `cd source/frontend && npm test -- --run src/__tests__/Home.test.js && npm run build`  
Expected: tests PASS and Vite build succeeds.

- [ ] **Step 7: Commit**

```bash
git add source/frontend/src/views/Home.vue source/frontend/src/components/home source/frontend/src/__tests__/Home.test.js
git commit -m "feat: rebuild cinematic knowledge awakening home"
```

### Task 5: Redesign identity, login, and registration

**Files:**
- Create: `source/frontend/src/components/auth/IdentitySwitch.vue`
- Create: `source/frontend/src/components/auth/AuthScene.vue`
- Modify: `source/frontend/src/views/Login.vue`
- Modify: `source/frontend/src/views/Register.vue`
- Modify: `source/frontend/src/router/index.js`
- Test: `source/frontend/src/__tests__/authExperience.test.js`

- [ ] **Step 1: Write failing identity-selection tests**

Test that `?role=teacher` preselects teacher, student selection links to `/student/guidance`, labels remain visible, and submitting emits the existing login action rather than a mock success.

- [ ] **Step 2: Run the focused test and verify failure**

Run: `cd source/frontend && npm test -- --run src/__tests__/authExperience.test.js`  
Expected: FAIL because `IdentitySwitch` is missing.

- [ ] **Step 3: Implement AuthScene and IdentitySwitch**

Use the teacher/student generated art, maintain visible field labels, expose selected role through `v-model`, and preserve keyboard arrow/Tab behavior.

- [ ] **Step 4: Refactor Login and Register**

Retain the existing Pinia/API submission methods and validation rules. Replace page styling and hierarchy, add pending/error states, link back to `/`, and use canonical “智教通” copy.

- [ ] **Step 5: Repair mojibake in touched router labels**

Replace corrupted comments and `meta.title` values with valid UTF-8 Chinese without changing route paths or auth semantics.

- [ ] **Step 6: Run tests and commit**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and build succeeds.

```bash
git add source/frontend/src/components/auth source/frontend/src/views/Login.vue source/frontend/src/views/Register.vue source/frontend/src/router/index.js source/frontend/src/__tests__/authExperience.test.js
git commit -m "feat: redesign identity and authentication experience"
```

### Task 6: Create the unified workspace shell and teacher experience

**Files:**
- Rewrite: `source/frontend/src/layout/index.vue`
- Create: `source/frontend/src/components/data/MetricCard.vue`
- Create: `source/frontend/src/components/teacher/GuidanceStep.vue`
- Modify: `source/frontend/src/views/teacher/Home.vue`
- Modify: `source/frontend/src/views/teacher/Tools.vue`
- Modify: `source/frontend/src/views/teacher/Dashboard.vue`
- Test: `source/frontend/src/__tests__/teacherExperience.test.js`

- [ ] **Step 1: Write failing teacher navigation and guidance tests**

Assert the shell exposes “需求引导 / 我的工具 / 数据洞察”, active route state uses `aria-current="page"`, the guidance has three named stages, and tool/dashboard empty states render through `StatusState`.

- [ ] **Step 2: Run the focused test and confirm failure**

Run: `cd source/frontend && npm test -- --run src/__tests__/teacherExperience.test.js`  
Expected: FAIL against the old shell.

- [ ] **Step 3: Rebuild the shared workspace shell**

Use a collapsible ink-panel sidebar, canonical brand mark, role-aware menu, page title, profile control, mobile drawer, and one `router-view`. Preserve teacher and student route paths.

- [ ] **Step 4: Rebuild teacher Home as the three-stage knowledge map**

Stage 1 selects subject domain, stage 2 selects teaching goal, stage 3 renders existing recommendation results. Keep current API calls and disable progression until required selections exist.

- [ ] **Step 5: Rebuild Tools and Dashboard**

Tools distinguishes preset/self-created/external types with clear actions. Dashboard uses `MetricCard`, trend, ranking, and recent records; charts preserve explicit labels and values.

- [ ] **Step 6: Run tests, build, and commit**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and build succeeds.

```bash
git add source/frontend/src/layout source/frontend/src/components/data source/frontend/src/components/teacher source/frontend/src/views/teacher source/frontend/src/__tests__/teacherExperience.test.js
git commit -m "feat: redesign teacher workspace"
```

### Task 7: Redesign the student knowledge journey

**Files:**
- Create: `source/frontend/src/components/student/InterestBubble.vue`
- Create: `source/frontend/src/components/student/ToolCard.vue`
- Modify: `source/frontend/src/views/student/Guidance.vue`
- Modify: `source/frontend/src/views/student/Plaza.vue`
- Modify: `source/frontend/src/views/student/Chat.vue`
- Modify: `source/frontend/src/views/student/Records.vue`
- Modify: `source/frontend/src/views/student/ToolUse.vue`
- Test: `source/frontend/src/__tests__/studentExperience.test.js`

- [ ] **Step 1: Write failing student-flow tests**

Assert guidance exposes three selectable interest layers, Plaza supports category/search controls, Chat keeps the input after a simulated timeout, Records exposes labeled metrics, and ToolUse renders the route tool ID.

- [ ] **Step 2: Run the focused test and confirm failure**

Run: `cd source/frontend && npm test -- --run src/__tests__/studentExperience.test.js`  
Expected: FAIL because the new primitives and state behavior are absent.

- [ ] **Step 3: Rebuild Guidance as a knowledge universe**

Use accessible buttons for bubbles, visible selection state, three layers only, a live progress label, and static layout in reduced-motion mode.

- [ ] **Step 4: Rebuild Plaza and ToolCard**

Retain existing category/search behavior and route destinations. Use responsive CSS grid, semantic headings, keyboard-visible cards, and explicit empty/loading/error states.

- [ ] **Step 5: Rebuild Chat, ToolUse, and Records**

Chat and ToolUse use the two-column learning-context layout on desktop and one column on mobile. Preserve user text on request failure and expose retry. Records combines metrics, timeline, and empty state without inventing missing backend data.

- [ ] **Step 6: Run tests, build, and commit**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and build succeeds.

```bash
git add source/frontend/src/components/student source/frontend/src/views/student source/frontend/src/__tests__/studentExperience.test.js
git commit -m "feat: redesign student knowledge journey"
```

### Task 8: Add explicit demo mode and complete async states

**Files:**
- Create: `source/frontend/src/composables/useDemoMode.js`
- Create: `source/frontend/src/data/demo.js`
- Modify: `source/frontend/.env.example`
- Modify: teacher/student data pages from Tasks 6–7
- Test: `source/frontend/src/__tests__/demoMode.test.js`

- [ ] **Step 1: Write a failing demo-mode test**

```js
it('marks demo data instead of presenting it as live API data', () => {
  const { enabled, label } = useDemoMode({ VITE_DEMO_MODE: 'true' })
  expect(enabled.value).toBe(true)
  expect(label).toBe('演示数据')
})
```

- [ ] **Step 2: Run the test and confirm the composable is missing**

Run: `cd source/frontend && npm test -- --run src/__tests__/demoMode.test.js`  
Expected: FAIL on missing module.

- [ ] **Step 3: Implement explicit environment-controlled demo mode**

`useDemoMode(env = import.meta.env)` returns `enabled`, `label`, and `getDemoData(key)`. It must never catch a live API error and silently substitute demo data.

- [ ] **Step 4: Add representative data matching existing view models**

Create fixed teacher metrics, trend points, tools, student learning history, and plaza cards using only fields already consumed by current pages. Add `VITE_DEMO_MODE=false` to `.env.example`.

- [ ] **Step 5: Connect page states**

When enabled, show a persistent “演示数据” chip. When disabled, show loading, empty, error, and retry states from real calls.

- [ ] **Step 6: Run tests and commit**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and build succeeds.

```bash
git add source/frontend/src/composables/useDemoMode.js source/frontend/src/data/demo.js source/frontend/.env.example source/frontend/src/views source/frontend/src/__tests__/demoMode.test.js
git commit -m "feat: add explicit presentation demo mode"
```

### Task 9: Responsive, accessibility, and performance pass

**Files:**
- Modify: `source/frontend/src/styles/global.css`
- Modify: all new components with responsive or canvas behavior
- Modify: `source/frontend/vite.config.js`
- Test: `source/frontend/src/__tests__/accessibility.test.js`

- [ ] **Step 1: Add structural accessibility tests**

Test one `main` landmark per page, an `h1` on Home/Login/workspace landing pages, named icon buttons, visible form labels, `aria-current` navigation, and no clickable non-interactive `div` in the new guidance components.

- [ ] **Step 2: Run the test and record failing assertions**

Run: `cd source/frontend && npm test -- --run src/__tests__/accessibility.test.js`  
Expected: FAIL for any missing landmark or accessible name.

- [ ] **Step 3: Fix responsive layouts**

Verify breakpoints at 1440, 1080, 768, and 390 CSS pixels. Remove horizontal overflow, convert sidebars to drawers, maintain 44×44 targets, and prevent fixed artwork from covering content.

- [ ] **Step 4: Split large bundles**

Configure Rollup `manualChunks` for Vue/Router/Pinia and Element Plus, keep every route lazy, and ensure generated artwork is referenced per section rather than imported into the global entry.

- [ ] **Step 5: Validate reduced-motion and Canvas cleanup**

Confirm particle animation stops when hidden/unmounted, respects reduced motion, and does not create duplicate animation loops after route navigation.

- [ ] **Step 6: Run the full verification suite**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS; build succeeds; no chunk exceeds the current 1.04 MB baseline.

- [ ] **Step 7: Commit**

```bash
git add source/frontend/src source/frontend/vite.config.js
git commit -m "perf: polish responsive accessible frontend"
```

### Task 10: Browser QA and final presentation launch

**Files:**
- Create: `docs/superpowers/reports/2026-07-13-frontend-redesign-qa.md`
- Modify: files found defective during QA only

- [ ] **Step 1: Start the presentation build**

Run: `cd source/frontend && npm run dev -- --host 127.0.0.1 --port 5173`  
Expected: Vite reports `http://127.0.0.1:5173/`.

- [ ] **Step 2: Inspect the landing page in a real browser**

Check headline, generated artwork, knowledge core, teacher/student entry routes, all six narrative sections, scroll-back behavior, console errors, network failures, and reduced-motion behavior.

- [ ] **Step 3: Inspect teacher routes**

With demo mode explicitly enabled, verify `/login?role=teacher`, `/teacher/home`, `/teacher/tools`, and `/teacher/dashboard`. Confirm active navigation, empty/error states, keyboard focus, and no page overflow.

- [ ] **Step 4: Inspect student routes**

Verify `/student/guidance`, `/student/plaza`, `/student/chat`, `/student/records`, and `/tool/1`. Confirm bubble selection, filters, message error retention, responsive layout, and route transitions.

- [ ] **Step 5: Capture desktop and mobile screenshots**

Capture Home, teacher dashboard, student guidance, and student chat at 1440×900 and 390×844. Inspect each screenshot for clipped text, broken images, weak contrast, inconsistent spacing, and accidental generic Element Plus styling.

- [ ] **Step 6: Fix defects and rerun verification**

Run: `cd source/frontend && npm test -- --run && npm run build`  
Expected: all tests PASS and production build succeeds after fixes.

- [ ] **Step 7: Write the QA report and commit**

Record commands, results, reviewed routes, remaining backend-only limitations, and screenshot paths.

```bash
git add source/frontend docs/superpowers/reports/2026-07-13-frontend-redesign-qa.md
git commit -m "test: verify eastern future frontend experience"
```

