<script setup>
const props = defineProps({
  name: { type: String, required: true } // swallow | flourish-tl | flourish-tr | flourish-bl | flourish-br | divider-flower
})
</script>

<template>
  <span class="vintage-ornament" :class="`is-${name}`" aria-hidden="true">
    <svg v-if="name === 'swallow'" viewBox="0 0 48 32">
      <path d="M24 18c-6 4-12 10-20 12 4-6 8-12 16-16-4-2-8-2-12 0 6-6 12-8 18-6 2-6 4-8 6-8s4 4 4 8c6-2 12 0 18 6-4-2-8-2-12 0 8 4 12 10 16 16-8-2-14-8-20-12-2 4-4 6-6 6s-4-2-6-6z" fill="currentColor" />
    </svg>

    <svg v-else-if="name === 'flourish-tl'" viewBox="0 0 32 32">
      <path d="M2 18c6-2 10-6 12-12M2 18c2 6 6 10 12 12M2 18c6 2 10 6 12 12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>

    <svg v-else-if="name === 'flourish-tr'" viewBox="0 0 32 32">
      <path d="M30 18c-6-2-10-6-12-12M30 18c-2 6-6 10-12 12M30 18c-6 2-10 6-12 12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>

    <svg v-else-if="name === 'flourish-bl'" viewBox="0 0 32 32">
      <path d="M2 14c6 2 10 6 12 12M2 14c2-6 6-10 12-12M2 14c6-2 10-6 12-12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>

    <svg v-else-if="name === 'flourish-br'" viewBox="0 0 32 32">
      <path d="M30 14c-6 2-10 6-12 12M30 14c-2-6-6-10-12-12M30 14c-6-2-10-6-12-12" fill="none" stroke="currentColor" stroke-width="1.2" />
    </svg>

    <svg v-else-if="name === 'divider-flower'" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1" />
      <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="0.8" />
    </svg>
  </span>
</template>

<style scoped>
.vintage-ornament {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #8b6f47;
  opacity: 0.65;
}

.vintage-ornament.is-swallow {
  width: 48px;
  height: 32px;
}

.vintage-ornament.is-swallow svg {
  width: 100%;
  height: 100%;
}

.vintage-ornament[class*="flourish"] {
  width: 28px;
  height: 28px;
}

.vintage-ornament.is-divider-flower {
  width: 20px;
  height: 20px;
}
</style>
