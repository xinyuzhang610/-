# Home Visual Feedback QA — 2026-07-14

## Automated verification

- Vitest: PASS — 14 files, 65 tests
- Vite production build: PASS — 1,751 modules transformed
- `git diff --check`: PASS

## Viewports

| Viewport | CTA | Pain heading | Complete subjects | Scratch interaction | Overflow / console |
| --- | --- | --- | --- | --- | --- |
| 1440×900 | PASS | PASS | PASS | PASS | PASS |
| 1088×778 | PASS | PASS | PASS | PASS | PASS |
| 851×778 | PASS | PASS | PASS | PASS | PASS |
| 390×844 | PASS | PASS | PASS | PASS | PASS |

## Measured browser evidence

- All four entry links render the shared SVG guide glyph; computed font weight is `500`, letter spacing is `1.216px`, and border radius is `4.8px` at 1088px.
- The two problem-heading lines retain their approved text and separate block boxes at 1088px, 851px, and 390px.
- Teacher and student foreground layers report `object-fit: contain` at every target viewport.
- Document horizontal overflow is false at 1088px, 851px, and 390px.
- Desktop pointer movement changed 62,641 Canvas pixels to fully transparent without a mouse press; the guidance hint then disappeared.
- Pointer leave and viewport resize reset interpolation state, preventing a re-entry stroke from crossing untouched space.
- Synthetic touch verification produced no cleared pixels for a vertical-first gesture and cleared pixels after a deliberate horizontal gesture.
- Reduced-motion emulation reports `data-static="true"`, a hidden Canvas, no misleading movement hint, and usable teacher/student links.
- Browser error collection remained empty after reloads, pointer interaction, scrolling, viewport changes, and reduced-motion emulation.

## Accessibility and fallback

- Keyboard-focusable semantic entry links: PASS
- Reduced-motion static fallback: PASS
- Missing `matchMedia` / Canvas context fallback: PASS
- Background and journey image failure surfaces: PASS
- Touch vertical scrolling guard and deliberate reveal: PASS

## Visual evidence

- `screenshots/home-feedback-1440-before.png`
- `screenshots/home-feedback-1440-after.png`
- `screenshots/home-feedback-1088-pain.png`
- `screenshots/home-feedback-851-journey.png`
- `screenshots/home-feedback-390-hero.png`
- `screenshots/home-feedback-390-pain.png`
- `screenshots/home-feedback-390-journey.png`

## Runtime

- Demo URL: http://127.0.0.1:5173/
- Vite listener: active
- Browser console errors: none
