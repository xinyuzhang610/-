<script setup>
defineProps({
  role: {
    type: String,
    required: true,
    validator: value => ['teacher', 'student'].includes(value)
  },
  label: {
    type: String,
    required: true
  },
  to: {
    type: [String, Object],
    required: true
  },
  testId: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <RouterLink
    class="entry-link"
    :class="`entry-link--${role}`"
    :to="to"
    :data-testid="testId || undefined"
  >
    <span class="entry-link__frame">
      <span class="entry-link__label">{{ label }}</span>
      <svg
        class="entry-link__glyph"
        viewBox="0 0 42 12"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M1 6h34M29 1l7 5-7 5" />
      </svg>
    </span>
  </RouterLink>
</template>

<style scoped>
.entry-link {
  display: inline-flex;
  min-height: 3rem;
  padding: .2rem;
  border: 1px solid var(--gold-400);
  border-radius: .3rem;
  color: var(--moon-50);
  font-family: var(--font-body);
  font-size: .95rem;
  font-weight: 500;
  letter-spacing: .08em;
  line-height: 1;
  text-decoration: none;
}

.entry-link__frame {
  display: inline-flex;
  min-width: 11rem;
  min-height: calc(3rem - .4rem);
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: .55rem 1rem;
  border: 1px solid rgb(213 166 79 / 48%);
  border-radius: .12rem;
}

.entry-link--teacher {
  background: var(--ink-950);
  color: var(--gold-200);
}

.entry-link--student {
  border-color: var(--gold-300);
  background: var(--jade-700);
  color: var(--gold-200);
}

.entry-link--student .entry-link__frame {
  border-color: rgb(244 211 139 / 52%);
}

.entry-link__glyph {
  width: 2.625rem;
  height: .75rem;
  flex: 0 0 auto;
  fill: none;
  stroke: currentcolor;
  stroke-linecap: square;
  stroke-linejoin: miter;
  stroke-width: 1;
  transition: transform var(--duration-fast, 180ms) ease;
}

.entry-link:hover .entry-link__glyph {
  transform: translateX(.25rem);
}

.entry-link:focus-visible {
  outline: 2px solid var(--moon-50);
  outline-offset: .25rem;
}

@media (prefers-reduced-motion: reduce) {
  .entry-link__glyph {
    transition: none;
  }

  .entry-link:hover .entry-link__glyph {
    transform: none;
  }
}
</style>
