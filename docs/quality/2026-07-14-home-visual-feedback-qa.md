# Home Visual Feedback QA — 2026-07-14

## Automated verification

- Vitest: PASS — 14 files, 71 tests
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
- The living-ink Canvas uses the approved `8px → 128px` radius range, `520ms` lifetime, `12px` path sampling, and a 160-stamp cap.
- At `1088×778`, the active reveal center measured Canvas alpha `28`; after `750ms` without movement it returned to alpha `255`, proving the same area closes instead of remaining erased.
- The active browser frame exposed the generated jade-and-gold mountain artwork beneath an irregular ink edge; the closed frame returned to a continuous deep-ink surface.
- Pointer leave, resize, and sampling gaps longer than `80ms` reset interpolation state, preventing distant positions from being joined by a stale reveal trail.
- Desktop checks at `1440×900`, `1088×778`, and `851×778` showed no horizontal overflow and kept both entry links visible.
- Teacher and student entries were clicked in the browser and reached `/login?role=teacher` and `/student/guidance` respectively.
- Reduced-motion emulation reports `data-static="true"`, a hidden Canvas, no misleading movement hint, and usable teacher/student links.
- Browser error collection remained empty after reloads, pointer interaction, scrolling, viewport changes, and reduced-motion emulation.

## Accessibility and fallback

- Keyboard-focusable semantic entry links: PASS
- Reduced-motion static fallback: PASS
- Missing `matchMedia` / Canvas context fallback: PASS
- Background and journey image failure surfaces: PASS
- Touch/no-hover full-art fallback: PASS

## Living-ink visual sequence

- Untouched: continuous deep-ink mask with no background leak.
- Active: localized irregular bloom reveals the generated knowledge-core landscape around the current pointer position.
- Closed: the bloom is no longer visible after `750ms`; the surrounding content and CTA positions remain unchanged.

## Runtime

- Demo URL: http://127.0.0.1:5173/
- Vite listener: active
- Browser console errors: none
